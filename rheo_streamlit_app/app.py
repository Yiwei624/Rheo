from __future__ import annotations

import io
import shutil
import zipfile
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from rheo import db as rdb


APP_TITLE = "RheoDB — 流变实验数据库 & 自动分析"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
SCHEMA_PATH = BASE_DIR / "rheo" / "schema.sql"

DATA_DIR.mkdir(exist_ok=True, parents=True)
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

GEOMETRY_LABELS = {
    "cone_plate": "cone_plate",
    "cup_bob": "cup and bob",
    "vane_cup": "vane in cup",
}

Y_LABELS = {
    "shear_stress_Pa": "Shear Stress τ (Pa)",
    "viscosity_Pa_s": "Viscosity η (Pa·s)",
}


def _mm_to_m(x_mm: Optional[float]) -> Optional[float]:
    if x_mm is None:
        return None
    try:
        return float(x_mm) / 1000.0
    except Exception:
        return None


def _m_to_mm(x_m: object, default: float = 0.0) -> float:
    try:
        if x_m is None or (isinstance(x_m, float) and pd.isna(x_m)):
            return default
        return float(x_m) * 1000.0
    except Exception:
        return default


def _format_mm(x_m: object) -> str:
    try:
        if x_m is None or (isinstance(x_m, float) and pd.isna(x_m)):
            return "—"
        return f"{float(x_m) * 1000.0:.4g}"
    except Exception:
        return "—"


def _db_path_from_state() -> Path:
    name = st.session_state.get("db_name", "rheo.sqlite")
    if not isinstance(name, str) or not name.strip():
        name = "rheo.sqlite"
    name = name.strip().replace("/", "_").replace("\\", "_")
    if not name.lower().endswith((".sqlite", ".db")):
        name = name + ".sqlite"
    return DATA_DIR / name


def _ensure_db(db_path: Path) -> None:
    rdb.init_db(db_path, SCHEMA_PATH)


def _bytes_download_button(label: str, data: bytes, file_name: str, mime: str) -> None:
    st.download_button(label=label, data=data, file_name=file_name, mime=mime)


def _zip_dir_bytes(folder: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(folder.rglob("*")):
            if p.is_file():
                zf.write(p, arcname=p.relative_to(folder))
    return buf.getvalue()


def _load_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text()
        except Exception:
            return ""


def _geometry_params_text(row: pd.Series) -> str:
    geom = str(row.get("geometry") or "")
    if geom == "cone_plate":
        return f"gap={_format_mm(row.get('gap_m'))} mm"
    r1 = row.get("r1_m")
    r2 = row.get("r2_m")
    try:
        ratio = float(r2) / float(r1) if r1 is not None and r2 is not None and float(r1) > 0 else float("nan")
        ratio_txt = f"{ratio:.3g}" if np.isfinite(ratio) else "—"
    except Exception:
        ratio_txt = "—"
    return f"r1={_format_mm(r1)} mm, r2={_format_mm(r2)} mm, r2/r1={ratio_txt}"


def _render_geometry_schematic(geometry: str, r1_mm: Optional[float], r2_mm: Optional[float], *, title: str) -> None:
    if geometry not in {"vane_cup", "cup_bob"}:
        return
    try:
        r1 = float(r1_mm) if r1_mm is not None else float("nan")
        r2 = float(r2_mm) if r2_mm is not None else float("nan")
    except Exception:
        st.info("请输入有效的 r1 / r2。")
        return

    if not (np.isfinite(r1) and np.isfinite(r2) and r1 > 0 and r2 > 0):
        st.info("填写 r1 和 r2 后，这里会自动显示几何示意图。")
        return
    if r2 <= r1:
        st.warning("需要满足 r2 > r1，才能画出 cup / bob（或 vane / cup）示意图。")
        return

    info_col, fig_col = st.columns([0.9, 1.1])
    with info_col:
        st.markdown("#### 几何参数示意")
        st.write(
            {
                "geometry": GEOMETRY_LABELS.get(geometry, geometry),
                "r1 (mm)": f"{r1:.3f}",
                "r2 (mm)": f"{r2:.3f}",
                "gap (mm)": f"{(r2 - r1):.3f}",
                "r2/r1": f"{r2 / r1:.3f}",
            }
        )
        st.caption("图中按真实半径比绘制：外圈是 cup，内圈是 bob / vane 包络。")
    with fig_col:
        try:
            fig = rdb.make_geometry_schematic(geometry, r1 / 1000.0, r2 / 1000.0, title=title)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        except Exception as e:
            st.warning("几何示意图生成失败。")
            st.exception(e)


def _label_row(row: pd.Series) -> str:
    sid = int(row["id"])
    sname = str(row.get("sample_name") or "")
    geom = GEOMETRY_LABELS.get(str(row.get("geometry") or ""), str(row.get("geometry") or ""))
    ts = str(row.get("created_at") or "")
    return f"{sid} | {sname} | {geom} | {ts}"


def _get_segment_df(df: pd.DataFrame, seg: str) -> pd.DataFrame:
    if seg == "all":
        return df.copy()
    parts = rdb.split_up_down(df)
    if seg in parts:
        return parts[seg].copy()
    return parts.get("all", df).copy()


def _prepare_xy(
    df0: pd.DataFrame,
    *,
    seg: str,
    y_col: str,
    x_min: Optional[float],
    x_max: Optional[float],
) -> tuple[np.ndarray, np.ndarray]:
    d = _get_segment_df(df0, seg)
    x = pd.to_numeric(d["shear_rate_1_s"], errors="coerce").to_numpy(dtype=float)
    y = pd.to_numeric(d[y_col], errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0)
    x = x[mask]
    y = y[mask]
    if x.size == 0:
        return x, y
    order = np.argsort(x)
    x = x[order]
    y = y[order]
    tmp = pd.DataFrame({"x": x, "y": y}).groupby("x", as_index=False).mean()
    x = tmp["x"].to_numpy(dtype=float)
    y = tmp["y"].to_numpy(dtype=float)

    if x_min is not None:
        keep = x >= float(x_min)
        x = x[keep]
        y = y[keep]
    if x_max is not None:
        keep = x <= float(x_max)
        x = x[keep]
        y = y[keep]
    return x, y


def _interp_to_grid(x: np.ndarray, y: np.ndarray, xg: np.ndarray, mode: str) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xg = np.asarray(xg, dtype=float)
    yout = np.full_like(xg, np.nan, dtype=float)
    if x.size < 2:
        return yout

    if not np.all(np.diff(x) >= 0):
        order = np.argsort(x)
        x = x[order]
        y = y[order]

    in_range = (xg >= np.min(x)) & (xg <= np.max(x)) & np.isfinite(xg)
    if not np.any(in_range):
        return yout

    use_logx = mode.startswith("log")
    if use_logx:
        xt = np.log10(x)
        xgt = np.log10(xg[in_range])
    else:
        xt = x
        xgt = xg[in_range]

    use_logy = mode == "log-log（推荐）"
    if use_logy:
        if np.all(y > 0) and np.all(np.isfinite(y)):
            yt = np.log10(y)
            ygt = np.interp(xgt, xt, yt)
            yout[in_range] = np.power(10.0, ygt)
            return yout

    ygt = np.interp(xgt, xt, y)
    yout[in_range] = ygt
    return yout


def _trend_fit_curve(
    x: np.ndarray,
    y: np.ndarray,
    *,
    use_logx: bool,
    use_logy: bool,
    n_points: int = 200,
) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0)
    if use_logy:
        mask &= y > 0
    x = x[mask]
    y = y[mask]
    if x.size < 2:
        return np.array([]), np.array([])

    order = np.argsort(x)
    x = x[order]
    y = y[order]

    if use_logx and use_logy:
        xt = np.log10(x)
        yt = np.log10(y)
        if xt.size < 2:
            return np.array([]), np.array([])
        slope, intercept = np.polyfit(xt, yt, 1)
        xf = np.logspace(np.log10(x.min()), np.log10(x.max()), n_points)
        yf = np.power(10.0, intercept + slope * np.log10(xf))
        return xf, yf

    if use_logx:
        xt = np.log10(x)
        slope, intercept = np.polyfit(xt, y, 1)
        xf = np.logspace(np.log10(x.min()), np.log10(x.max()), n_points)
        yf = intercept + slope * np.log10(xf)
        return xf, yf

    slope, intercept = np.polyfit(x, y, 1)
    xf = np.linspace(x.min(), x.max(), n_points)
    yf = intercept + slope * xf
    return xf, yf


st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

with st.sidebar:
    st.header("数据库")
    st.caption("默认数据库保存在仓库的 data/ 目录。")
    st.info(
        "⚠️ Streamlit Community Cloud 不保证本地文件持久化：应用重启/休眠/重新部署后，data/ 里的 SQLite 可能会被清空。\n\n"
        "✅ 如果你在 Cloud 上用：每次导入后请立刻点『下载当前数据库』备份；下次打开再用『上传已有数据库』恢复。"
    )

    if "db_name" not in st.session_state:
        st.session_state["db_name"] = "rheo.sqlite"
    st.text_input("数据库文件名", key="db_name")
    raw_name = st.session_state.get("db_name", "rheo.sqlite")
    db_path = _db_path_from_state()
    if isinstance(raw_name, str) and db_path.name != raw_name.strip():
        st.caption(f"实际使用文件名：{db_path.name}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("初始化/更新表结构", use_container_width=True):
            _ensure_db(db_path)
            st.success(f"OK: {db_path.name}")
    with c2:
        if st.button("刷新页面数据", use_container_width=True):
            st.rerun()

    uploaded_db = st.file_uploader(
        "上传已有数据库（.sqlite/.db）",
        type=["sqlite", "db"],
        help="上传后会覆盖当前 data/ 下同名数据库。",
    )
    if uploaded_db is not None:
        db_path.write_bytes(uploaded_db.getvalue())
        st.success(f"已导入数据库: {db_path.name}")

    if db_path.exists():
        _bytes_download_button(
            "下载当前数据库",
            data=db_path.read_bytes(),
            file_name=db_path.name,
            mime="application/x-sqlite3",
        )
    else:
        st.info("数据库文件不存在：请先点击『初始化/更新表结构』，或上传已有数据库。")

    with st.expander("危险操作：删除数据", expanded=False):
        st.warning("这些操作会永久删除数据。建议先下载数据库备份。")

        del_outputs_all = st.checkbox(
            "同时删除 outputs/ 目录下的所有分析输出文件",
            value=False,
            help="只影响当前运行目录，不影响你已经下载到本地的文件。",
        )
        confirm_all = st.text_input("输入 DELETE_ALL 确认『清空所有实验』", key="confirm_delete_all")
        if st.button(
            "清空所有实验（保留数据库结构）",
            use_container_width=True,
            disabled=(confirm_all.strip() != "DELETE_ALL"),
        ):
            try:
                if db_path.exists():
                    rdb.delete_all_experiments(db_path)
                if del_outputs_all and OUTPUT_DIR.exists():
                    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
                    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
                st.success("已清空所有实验 ✅")
                st.rerun()
            except Exception as e:
                st.exception(e)

        st.divider()

        confirm_db = st.text_input("输入 DELETE_DB 确认『删除数据库文件』", key="confirm_delete_db")
        if st.button(
            "删除数据库文件（会清空全部）",
            use_container_width=True,
            disabled=(confirm_db.strip() != "DELETE_DB"),
        ):
            try:
                if db_path.exists():
                    db_path.unlink()
                st.success("数据库文件已删除 ✅")
                st.rerun()
            except Exception as e:
                st.exception(e)

    st.divider()
    st.subheader("快速导航")
    st.markdown(
        "- 导入实验 → 自动入库\n"
        "- 单个实验 → 一键分析 / 出图 / 拟合\n"
        "- 多实验对比 → 选区间 + reference + 误差表 + bar chart\n"
        "- 为什么 12-blade 更好 → 文档总结页"
    )

if db_path.exists():
    _ensure_db(db_path)

TAB_IMPORT, TAB_BROWSE, TAB_COMPARE, TAB_WHY12, TAB_THEORY = st.tabs(
    [
        "① 导入实验",
        "② 实验浏览 & 分析",
        "③ 多实验对比分析",
        "④ 为什么 12-blade 更好（你的文档总结）",
        "⑤ Theory / Partial Yield 公式",
    ]
)


with TAB_IMPORT:
    st.subheader("导入：样本信息 + 几何参数 + 原始数据文件")

    st.markdown("#### 下载模板 / 示例数据")
    t1, t2, t3 = st.columns(3)
    template_csv = BASE_DIR / "assets" / "template_export.csv"
    template_xlsx = BASE_DIR / "assets" / "template_export.xlsx"
    example_csv = BASE_DIR / "assets" / "example_data.csv"
    with t1:
        if template_csv.exists():
            _bytes_download_button("下载 template_export.csv", template_csv.read_bytes(), template_csv.name, "text/csv")
    with t2:
        if template_xlsx.exists():
            _bytes_download_button(
                "下载 template_export.xlsx",
                template_xlsx.read_bytes(),
                template_xlsx.name,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    with t3:
        if example_csv.exists():
            _bytes_download_button("下载 example_data.csv", example_csv.read_bytes(), example_csv.name, "text/csv")

    st.markdown("---")
    st.markdown("#### 1) 填写元数据")

    c_meta1, c_meta2, c_meta3 = st.columns([1.25, 1.0, 1.0])
    with c_meta1:
        sample_name = st.text_input("样本名字 (sample_name)", value="")
        notes = st.text_area("备注 (notes)", value="", height=100)

    with c_meta2:
        geometry = st.selectbox(
            "几何 (geometry)",
            options=["cone_plate", "cup_bob", "vane_cup"],
            format_func=lambda x: GEOMETRY_LABELS.get(x, x),
            help="cone&plate: 填 gap；cup and bob / vane in cup: 填 r1(内半径) 和 r2(cup 半径)",
        )
        yield0 = st.number_input(
            "HB 拟合 τy 初始值 (Pa)",
            value=0.0,
            min_value=0.0,
            help="你原本的 yield stress（用于 Herschel–Bulkley 拟合的初值）。",
        )

    with c_meta3:
        if geometry == "cone_plate":
            gap_mm = st.number_input("gap (mm)", value=0.0, min_value=0.0)
            st.caption("cone & plate：只需要 gap（不需要 r1 / r2）。")
            r1_mm = None
            r2_mm = None
        else:
            gap_mm = None
            r1_mm = st.number_input("r1 (mm) — vane / bob 半径", value=0.0, min_value=0.0)
            r2_mm = st.number_input("r2 (mm) — cup 半径", value=0.0, min_value=0.0)
            st.caption("vane in cup / cup and bob：需要 r1（内几何半径）与 r2（cup 半径）。")

    if geometry in {"vane_cup", "cup_bob"}:
        _render_geometry_schematic(
            geometry,
            r1_mm,
            r2_mm,
            title=f"{GEOMETRY_LABELS.get(geometry, geometry)} schematic",
        )

    st.markdown("---")
    st.markdown("#### 2) 上传数据文件")
    up_file = st.file_uploader(
        "上传实验导出文件（CSV / XLSX / TXT）",
        type=["csv", "xlsx", "xls", "txt"],
        help="如果导出是 .txt（常见为 tab 分隔），也可以直接上传。",
    )

    sheet_arg: str | int | None = 0
    if up_file is not None and Path(up_file.name).suffix.lower() in [".xlsx", ".xls"]:
        try:
            xls = pd.ExcelFile(io.BytesIO(up_file.getvalue()))
            if xls.sheet_names:
                sheet_arg = st.selectbox("选择 Excel sheet", options=xls.sheet_names, index=0)
            else:
                sheet_arg = 0
        except Exception:
            sheet_name_txt = st.text_input("Excel sheet（可选，默认 0）", value="0")
            s = sheet_name_txt.strip()
            if s == "":
                sheet_arg = 0
            else:
                try:
                    sheet_arg = int(s)
                except Exception:
                    sheet_arg = s

    run_analysis = st.checkbox("导入后立刻分析并出图", value=True)

    if up_file is not None:
        with st.expander("预览上传的数据（前 30 行）", expanded=True):
            try:
                suffix = Path(up_file.name).suffix.lower()
                if suffix in [".xlsx", ".xls"]:
                    raw_preview = pd.read_excel(io.BytesIO(up_file.getvalue()), sheet_name=sheet_arg)
                else:
                    raw_preview = pd.read_csv(io.BytesIO(up_file.getvalue()), sep=None, engine="python")

                st.caption("原始列名（raw headers）：")
                st.write(list(raw_preview.columns))
                st.dataframe(raw_preview.head(30), use_container_width=True)

                norm_preview = rdb.normalize_columns(raw_preview)
                st.caption("本软件识别到的标准列（normalized）：")
                st.write(list(norm_preview.columns))
                st.dataframe(norm_preview.head(30), use_container_width=True)

                n_sr = int(norm_preview["shear_rate_1_s"].notna().sum())
                n_ss = int(norm_preview["shear_stress_Pa"].notna().sum())
                st.info(f"识别到 shear_rate 有效点数：{n_sr}；shear_stress 有效点数：{n_ss}")
                if n_sr < 3 or n_ss < 3:
                    st.warning("⚠️ 关键列有效点太少。请检查表头是否包含 Shear Rate / Shear Stress，或导出文件前面是否有说明行。")
            except Exception as e:
                st.warning("预览失败（不影响导入）。你可以直接点击导入；若失败，下方会显示报错。")
                st.exception(e)

    st.markdown("---")
    if st.button("导入到数据库", use_container_width=True, type="primary"):
        if not sample_name.strip():
            st.error("请填写样本名字。")
        elif up_file is None:
            st.error("请先上传 CSV / XLSX / TXT 原始数据文件。")
        else:
            try:
                _ensure_db(db_path)
                safe_name = up_file.name.replace("/", "_").replace("\\", "_")
                dest = UPLOAD_DIR / f"{pd.Timestamp.utcnow().strftime('%Y%m%d_%H%M%S')}_{safe_name}"
                dest.write_bytes(up_file.getvalue())

                exp_id = rdb.import_experiment(
                    db_path=db_path,
                    schema_path=SCHEMA_PATH,
                    sample_name=sample_name.strip(),
                    geometry=geometry,
                    data_file=dest,
                    gap_m=_mm_to_m(gap_mm) if gap_mm is not None else None,
                    r1_m=_mm_to_m(r1_mm) if r1_mm is not None else None,
                    r2_m=_mm_to_m(r2_mm) if r2_mm is not None else None,
                    yield_stress0_Pa=float(yield0) if yield0 is not None else None,
                    notes=notes.strip() if notes else None,
                    sheet_name=sheet_arg,
                )

                st.success(f"导入成功 ✅ experiment_id = {exp_id}")

                if db_path.exists():
                    st.warning("⚠️ 如果你部署在 Streamlit Community Cloud：本地文件可能会在重启 / 休眠后被清空。建议立刻下载数据库备份（.sqlite）。")
                    _bytes_download_button(
                        "立即下载数据库备份",
                        data=db_path.read_bytes(),
                        file_name=db_path.name,
                        mime="application/x-sqlite3",
                    )

                if run_analysis:
                    with st.spinner("正在分析并生成图 / 表格..."):
                        outdir = OUTPUT_DIR / f"exp_{exp_id}"
                        res = rdb.analyze_experiment(db_path=db_path, experiment_id=exp_id, outdir=outdir)

                    st.success("分析完成 ✅ 已生成图 + 拟合表")
                    st.caption(f"输出目录: {outdir}")

                    figs = [res["artifacts"].get(k) for k in ["fig1", "fig2", "fig3", "fig4"]]
                    cols = st.columns(2)
                    for i, fp in enumerate(figs):
                        if fp and Path(fp).exists():
                            with cols[i % 2]:
                                st.image(fp, caption=Path(fp).name, use_container_width=True)

                    st.markdown("### 拟合结果（fit_results）")
                    st.dataframe(rdb.fit_results_df(db_path, int(exp_id)), use_container_width=True, hide_index=True)
                    st.markdown("### Derived metrics")
                    st.dataframe(rdb.derived_metrics_df(db_path, int(exp_id)), use_container_width=True, hide_index=True)

                    if outdir.exists():
                        zbytes = _zip_dir_bytes(outdir)
                        _bytes_download_button(
                            "下载本次实验输出（zip）",
                            zbytes,
                            file_name=f"exp_{exp_id}_outputs.zip",
                            mime="application/zip",
                        )
            except Exception as e:
                st.exception(e)


with TAB_BROWSE:
    st.subheader("实验列表")

    if not db_path.exists():
        st.warning("当前数据库还没创建。请先在左侧初始化数据库或上传数据库文件。")
    else:
        exp_df = rdb.list_experiments_df(db_path)
        if exp_df.empty:
            st.info("数据库里还没有实验。请先去『① 导入实验』。")
        else:
            left, right = st.columns([1.05, 1.0])
            with left:
                show_df = exp_df.copy()
                show_df["geometry"] = show_df["geometry"].map(lambda x: GEOMETRY_LABELS.get(str(x), str(x)))
                show_df["geometry_params"] = exp_df.apply(_geometry_params_text, axis=1)
                cols = ["id", "sample_name", "geometry", "geometry_params", "yield_stress0_Pa", "created_at", "notes"]
                cols = [c for c in cols if c in show_df.columns]
                st.dataframe(show_df[cols], use_container_width=True, hide_index=True)

            with right:
                exp_ids = exp_df["id"].astype(int).tolist()
                exp_id = st.selectbox("选择 experiment_id", options=exp_ids, index=0)
                sel = exp_df.loc[exp_df["id"] == exp_id].iloc[0].to_dict()
                geom = str(sel.get("geometry") or "")

                st.markdown("#### 元数据")
                if geom == "cone_plate":
                    st.write(
                        {
                            "sample_name": sel.get("sample_name"),
                            "geometry": GEOMETRY_LABELS.get(geom, geom),
                            "gap (mm)": _format_mm(sel.get("gap_m")),
                            "HB τy initial (Pa)": sel.get("yield_stress0_Pa"),
                            "created_at": sel.get("created_at"),
                            "notes": sel.get("notes"),
                        }
                    )
                else:
                    r1m = sel.get("r1_m")
                    r2m = sel.get("r2_m")
                    try:
                        ratio = float(r2m) / float(r1m) if r1m is not None and r2m is not None and float(r1m) > 0 else float("nan")
                        ratio_txt = f"{ratio:.3g}" if np.isfinite(ratio) else "—"
                    except Exception:
                        ratio_txt = "—"
                    st.write(
                        {
                            "sample_name": sel.get("sample_name"),
                            "geometry": GEOMETRY_LABELS.get(geom, geom),
                            "r1 (mm)": _format_mm(r1m),
                            "r2 (mm)": _format_mm(r2m),
                            "r2/r1": ratio_txt,
                            "HB τy initial (Pa)": sel.get("yield_stress0_Pa"),
                            "created_at": sel.get("created_at"),
                            "notes": sel.get("notes"),
                        }
                    )
                    _render_geometry_schematic(
                        geom,
                        _m_to_mm(r1m, default=np.nan),
                        _m_to_mm(r2m, default=np.nan),
                        title=f"experiment {int(exp_id)} geometry",
                    )

                with st.expander("查看原始元数据（raw JSON）", expanded=False):
                    st.json(sel)

                with st.expander("编辑元数据（修正 gap / r1 / r2）", expanded=False):
                    new_sample = st.text_input(
                        "样本名字 (sample_name)",
                        value=str(sel.get("sample_name") or ""),
                        key=f"edit_sample_{exp_id}",
                    )
                    geom_options = ["cone_plate", "cup_bob", "vane_cup"]
                    try:
                        geom_idx = geom_options.index(str(sel.get("geometry") or "cone_plate"))
                    except Exception:
                        geom_idx = 0
                    new_geom = st.selectbox(
                        "几何 (geometry)",
                        options=geom_options,
                        index=geom_idx,
                        format_func=lambda x: GEOMETRY_LABELS.get(x, x),
                        key=f"edit_geom_{exp_id}",
                    )
                    new_yield0 = st.number_input(
                        "HB 拟合 τy 初始值 (Pa)",
                        value=float(sel.get("yield_stress0_Pa") or 0.0),
                        min_value=0.0,
                        key=f"edit_yield0_{exp_id}",
                    )
                    new_notes = st.text_area(
                        "备注 (notes)",
                        value=str(sel.get("notes") or ""),
                        height=80,
                        key=f"edit_notes_{exp_id}",
                    )

                    if new_geom == "cone_plate":
                        new_gap_mm = st.number_input(
                            "gap (mm)",
                            value=_m_to_mm(sel.get("gap_m")),
                            min_value=0.0,
                            key=f"edit_gap_{exp_id}",
                        )
                        new_r1_mm = None
                        new_r2_mm = None
                    else:
                        new_gap_mm = None
                        new_r1_mm = st.number_input(
                            "r1 (mm) — vane / bob 半径",
                            value=_m_to_mm(sel.get("r1_m")),
                            min_value=0.0,
                            key=f"edit_r1_{exp_id}",
                        )
                        new_r2_mm = st.number_input(
                            "r2 (mm) — cup 半径",
                            value=_m_to_mm(sel.get("r2_m")),
                            min_value=0.0,
                            key=f"edit_r2_{exp_id}",
                        )
                        _render_geometry_schematic(
                            new_geom,
                            new_r1_mm,
                            new_r2_mm,
                            title="preview while editing",
                        )

                    save1, save2 = st.columns([1.0, 1.0])
                    with save1:
                        if st.button("保存元数据", use_container_width=True, key=f"save_meta_{exp_id}"):
                            try:
                                rdb.update_experiment_meta(
                                    db_path,
                                    int(exp_id),
                                    sample_name=str(new_sample).strip(),
                                    geometry=str(new_geom),
                                    gap_m=_mm_to_m(new_gap_mm) if new_gap_mm is not None else None,
                                    r1_m=_mm_to_m(new_r1_mm) if new_r1_mm is not None else None,
                                    r2_m=_mm_to_m(new_r2_mm) if new_r2_mm is not None else None,
                                    yield_stress0_Pa=float(new_yield0) if new_yield0 is not None else None,
                                    notes=str(new_notes).strip() if new_notes is not None else None,
                                )
                                st.success("已保存 ✅（建议点击『运行 / 重新运行分析』更新图和拟合）")
                                st.rerun()
                            except Exception as e:
                                st.exception(e)
                    with save2:
                        st.caption("改了 r1 / r2 或 τy 后，Fig3 / Fig4 会变化；请重新运行分析。")

                outdir = OUTPUT_DIR / f"exp_{int(exp_id)}"
                run_col, dl_col = st.columns(2)
                with run_col:
                    if st.button("运行 / 重新运行分析", use_container_width=True):
                        try:
                            rdb.analyze_experiment(db_path=db_path, experiment_id=int(exp_id), outdir=outdir)
                            st.success("分析完成 ✅")
                        except Exception as e:
                            st.exception(e)
                with dl_col:
                    if outdir.exists():
                        _bytes_download_button(
                            "下载该实验输出（zip）",
                            _zip_dir_bytes(outdir),
                            file_name=f"exp_{int(exp_id)}_outputs.zip",
                            mime="application/zip",
                        )
                    else:
                        st.info("还没有输出文件。先运行分析。")

                with st.expander("删除该实验（危险操作）", expanded=False):
                    st.warning(
                        "将从数据库中永久删除该 experiment（包含 measurements / fit_results / derived_metrics / artifacts）。\n"
                        "建议先在左侧下载数据库备份。"
                    )
                    del_outputs = st.checkbox(
                        f"同时删除本地输出文件夹 outputs/exp_{int(exp_id)}",
                        value=True,
                        key=f"del_outputs_{int(exp_id)}",
                    )
                    confirm_txt = st.text_input("请输入 DELETE 确认删除", key=f"del_confirm_{int(exp_id)}")
                    if st.button(
                        "永久删除该实验",
                        use_container_width=True,
                        disabled=(confirm_txt.strip() != "DELETE"),
                        key=f"del_btn_{int(exp_id)}",
                    ):
                        try:
                            try:
                                art = rdb.artifacts_df(db_path, int(exp_id))
                                if not art.empty and "path" in art.columns:
                                    for p in art["path"].dropna().astype(str).tolist():
                                        try:
                                            Path(p).unlink(missing_ok=True)
                                        except Exception:
                                            pass
                            except Exception:
                                pass
                            if del_outputs and outdir.exists():
                                shutil.rmtree(outdir, ignore_errors=True)
                            rdb.delete_experiment(db_path, int(exp_id))
                            st.success(f"已删除 experiment_id={int(exp_id)} ✅")
                            st.rerun()
                        except Exception as e:
                            st.exception(e)

            st.markdown("---")
            st.markdown("### 原始数据预览")
            raw_df = rdb.measurements_df(db_path, int(exp_id))
            st.dataframe(raw_df.head(200), use_container_width=True)

            st.markdown("---")
            st.markdown("### 拟合结果")
            fit_df = rdb.fit_results_df(db_path, int(exp_id))
            if fit_df.empty:
                st.info("还没有拟合结果（需要先运行分析）。")
            else:
                st.dataframe(fit_df, use_container_width=True, hide_index=True)

            st.markdown("### Derived metrics")
            dm_df = rdb.derived_metrics_df(db_path, int(exp_id))
            if dm_df.empty:
                st.info("还没有 derived metrics（需要先运行分析）。")
            else:
                st.dataframe(dm_df, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("### 图像输出")
            if outdir.exists():
                fig_paths = [
                    outdir / "fig1_tau_vs_gammadot.png",
                    outdir / "fig2_eta_vs_gammadot.png",
                    outdir / "fig3_partial_yield_band.png",
                    outdir / "fig4_r0_over_r2.png",
                ]
                fig_cols = st.columns(2)
                for i, p in enumerate(fig_paths):
                    if p.exists():
                        with fig_cols[i % 2]:
                            st.image(str(p), caption=p.name, use_container_width=True)

                st.markdown("### 下载表格")
                d1, d2 = st.columns(2)
                csv_p = outdir / "fit_summary.csv"
                xlsx_p = outdir / "results_overview.xlsx"
                with d1:
                    if csv_p.exists():
                        _bytes_download_button("下载 fit_summary.csv", csv_p.read_bytes(), csv_p.name, "text/csv")
                    else:
                        st.info("fit_summary.csv 不存在")
                with d2:
                    if xlsx_p.exists():
                        _bytes_download_button(
                            "下载 results_overview.xlsx",
                            xlsx_p.read_bytes(),
                            xlsx_p.name,
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    else:
                        st.info("results_overview.xlsx 不存在")
            else:
                st.info("没有找到输出目录。先运行分析。")


with TAB_COMPARE:
    st.subheader("多实验对比分析：选区间 + reference + 误差表 + bar chart")
    st.markdown(
        "- 选多个已经上传的实验一起对比\n"
        "- 选 all / up / down\n"
        "- 自己指定 shear rate 区间\n"
        "- 选一个 reference，自动算其它实验相对它的误差\n"
        "- 除了误差表，还会给你一个误差 bar chart"
    )

    if not db_path.exists():
        st.warning("当前数据库还没创建。请先在左侧初始化数据库或上传数据库文件。")
    else:
        exp_df = rdb.list_experiments_df(db_path)
        if exp_df.empty:
            st.info("数据库里还没有实验。请先去『① 导入实验』上传数据。")
        else:
            exp_df = exp_df.copy()
            exp_df["_label"] = exp_df.apply(_label_row, axis=1)
            label_to_id = {row["_label"]: int(row["id"]) for _, row in exp_df.iterrows()}
            id_to_row = {int(row["id"]): row for _, row in exp_df.iterrows()}
            all_labels = exp_df["_label"].tolist()

            default_sel = all_labels[: min(3, len(all_labels))]
            selected_labels = st.multiselect(
                "选择要一起对比的实验（至少 2 个）",
                options=all_labels,
                default=default_sel,
            )

            if len(selected_labels) < 2:
                st.info("请选择至少 2 个实验进行对比。")
            else:
                selected_ids = [label_to_id[lbl] for lbl in selected_labels]

                c1, c2, c3 = st.columns([1.0, 1.0, 1.2])
                with c1:
                    seg_choice = st.selectbox(
                        "对比 sweep 段",
                        options=["all", "up", "down"],
                        index=0,
                        help="如果存在 up / down，会按该段对比；否则自动退回 all。",
                    )
                with c2:
                    y_choice = st.selectbox(
                        "对比变量（y 轴）",
                        options=["shear_stress_Pa", "viscosity_Pa_s"],
                        format_func=lambda x: Y_LABELS.get(x, x),
                    )
                with c3:
                    interp_mode = st.selectbox(
                        "插值方式（用于误差计算）",
                        options=["log-log（推荐）", "log-x linear-y", "linear-linear"],
                        index=0,
                        help="误差需要把不同实验插值到同一组 shear rate 点上。",
                    )

                x_ranges: dict[int, tuple[float, float]] = {}
                for eid in selected_ids:
                    df0 = rdb.measurements_df(db_path, int(eid))
                    dseg = _get_segment_df(df0, seg_choice)
                    x = pd.to_numeric(dseg["shear_rate_1_s"], errors="coerce").to_numpy(dtype=float)
                    x = x[np.isfinite(x) & (x > 0)]
                    if x.size >= 2:
                        x_ranges[eid] = (float(np.min(x)), float(np.max(x)))
                    else:
                        x_ranges[eid] = (float("nan"), float("nan"))

                mins = [v[0] for v in x_ranges.values() if np.isfinite(v[0])]
                maxs = [v[1] for v in x_ranges.values() if np.isfinite(v[1])]
                overlap_min = float(np.max(mins)) if mins else float("nan")
                overlap_max = float(np.min(maxs)) if maxs else float("nan")

                st.markdown("---")
                st.markdown("#### 选择 x 轴（shear rate）区间")
                auto_range = st.checkbox("使用所有选中实验的共同区间（推荐）", value=True)
                if auto_range and np.isfinite(overlap_min) and np.isfinite(overlap_max) and overlap_min < overlap_max:
                    x_min = overlap_min
                    x_max = overlap_max
                    st.info(f"共同区间：{x_min:.6g} ~ {x_max:.6g} 1/s")
                else:
                    if auto_range:
                        st.warning("共同区间为空或无法计算，已切换为手动输入。")
                    gmin = float(np.nanmin(mins)) if mins else 0.0
                    gmax = float(np.nanmax(maxs)) if maxs else 1.0
                    if not np.isfinite(gmin):
                        gmin = 0.0
                    if not np.isfinite(gmax) or gmax <= 0:
                        gmax = 1.0
                    xr1, xr2 = st.columns(2)
                    with xr1:
                        x_min = st.number_input(
                            "x_min (1/s)",
                            value=float(overlap_min) if np.isfinite(overlap_min) else gmin,
                            min_value=0.0,
                        )
                    with xr2:
                        x_max = st.number_input(
                            "x_max (1/s)",
                            value=float(overlap_max) if np.isfinite(overlap_max) else gmax,
                            min_value=0.0,
                        )
                    if x_max <= x_min:
                        st.error("x_max 必须大于 x_min。")

                st.markdown("---")
                ref_label = st.selectbox("reference experiment", options=selected_labels, index=0)
                ref_id = int(label_to_id[ref_label])
                grid_mode = st.radio(
                    "误差评估用的 x 网格",
                    options=["使用参考实验的 x 点（推荐）", "使用固定对数网格"],
                    index=0,
                )
                n_grid = 200
                if grid_mode == "使用固定对数网格":
                    n_grid = st.slider("网格点数", min_value=30, max_value=600, value=200, step=10)

                run_btn = st.button("运行多实验对比分析", type="primary", use_container_width=True)

                if run_btn and x_max > x_min:
                    with st.spinner("正在计算对比与误差..."):
                        curves: dict[int, dict[str, Any]] = {}
                        for eid in selected_ids:
                            df0 = rdb.measurements_df(db_path, int(eid))
                            x, y = _prepare_xy(df0, seg=seg_choice, y_col=y_choice, x_min=float(x_min), x_max=float(x_max))
                            row = id_to_row[int(eid)]
                            curves[int(eid)] = {
                                "x": x,
                                "y": y,
                                "label": _label_row(row),
                                "sample_name": str(row.get("sample_name") or ""),
                                "geometry": GEOMETRY_LABELS.get(str(row.get("geometry") or ""), str(row.get("geometry") or "")),
                            }

                        x_ref = curves[ref_id]["x"]
                        y_ref = curves[ref_id]["y"]
                        if x_ref.size < 2:
                            st.error("参考实验在该区间内没有足够的数据点。请换 reference 或调整 x 区间。")
                        else:
                            if grid_mode == "使用参考实验的 x 点（推荐）":
                                xg = x_ref.copy()
                            else:
                                xg = np.logspace(np.log10(float(x_min)), np.log10(float(x_max)), int(n_grid))

                            yref_g = _interp_to_grid(x_ref, y_ref, xg, interp_mode)
                            rows = []
                            aligned = pd.DataFrame({"shear_rate_1_s": xg, f"ref_{ref_id}": yref_g})

                            for eid in selected_ids:
                                xi = curves[eid]["x"]
                                yi = curves[eid]["y"]
                                yi_g = _interp_to_grid(xi, yi, xg, interp_mode)
                                aligned[f"exp_{eid}"] = yi_g

                                valid = np.isfinite(yi_g) & np.isfinite(yref_g)
                                valid_pct = valid & (np.abs(yref_g) > 0)
                                err = yi_g[valid] - yref_g[valid]
                                mae = float(np.nanmean(np.abs(err))) if err.size else float("nan")
                                rmse = float(np.sqrt(np.nanmean(err ** 2))) if err.size else float("nan")
                                bias = float(np.nanmean(err)) if err.size else float("nan")
                                ape = np.abs((yi_g[valid_pct] - yref_g[valid_pct]) / yref_g[valid_pct]) * 100.0
                                mape = float(np.nanmean(ape)) if ape.size else float("nan")
                                max_ape = float(np.nanmax(ape)) if ape.size else float("nan")

                                rows.append(
                                    {
                                        "experiment_id": int(eid),
                                        "is_reference": int(eid) == int(ref_id),
                                        "sample_name": curves[eid]["sample_name"],
                                        "geometry": curves[eid]["geometry"],
                                        "segment_used": seg_choice,
                                        "n_points_used": int(np.sum(valid)),
                                        "MAPE_%": 0.0 if int(eid) == int(ref_id) else mape,
                                        "Max_APE_%": 0.0 if int(eid) == int(ref_id) else max_ape,
                                        "RMSE": 0.0 if int(eid) == int(ref_id) else rmse,
                                        "MAE": 0.0 if int(eid) == int(ref_id) else mae,
                                        "Bias": 0.0 if int(eid) == int(ref_id) else bias,
                                    }
                                )

                            err_df = pd.DataFrame(rows).sort_values(["is_reference", "experiment_id"], ascending=[False, True])

                            st.markdown("### 误差表（相对 reference）")
                            st.dataframe(err_df, use_container_width=True, hide_index=True)

                            st.markdown("### 误差 bar chart（MAPE / Max APE）")
                            st.caption("bar chart 默认显示百分比误差：MAPE 和 Max APE。reference 的误差设为 0。")
                            fig_bar, ax_bar = plt.subplots(figsize=(8.2, 4.8))
                            plot_df = err_df.copy()
                            names = plot_df["experiment_id"].astype(str).tolist()
                            xpos = np.arange(len(names))
                            width = 0.36
                            ax_bar.bar(xpos - width / 2, plot_df["MAPE_%"].to_numpy(dtype=float), width=width, label="MAPE (%)")
                            ax_bar.bar(xpos + width / 2, plot_df["Max_APE_%"].to_numpy(dtype=float), width=width, label="Max APE (%)")
                            ax_bar.set_xticks(xpos)
                            ax_bar.set_xticklabels(names)
                            ax_bar.set_xlabel("Experiment ID")
                            ax_bar.set_ylabel("Percent error (%)")
                            ax_bar.set_title(f"Error summary vs reference {ref_id}")
                            ax_bar.legend()
                            fig_bar.tight_layout()
                            st.pyplot(fig_bar, use_container_width=True)
                            plt.close(fig_bar)

                            st.markdown("---")
                            st.markdown("### 多实验曲线叠加")
                            st.caption("raw 数据只显示点；reference 的趋势线是 thin solid，其他实验的趋势线是 thin dashed。")
                            fig, ax = plt.subplots(figsize=(8.2, 5.2))
                            use_logx = True
                            y_all = np.concatenate([curves[eid]["y"] for eid in selected_ids if curves[eid]["y"].size])
                            y_pos = y_all[np.isfinite(y_all) & (y_all > 0)]
                            use_logy = y_pos.size >= 2

                            for eid in selected_ids:
                                x = curves[eid]["x"]
                                y = curves[eid]["y"]
                                if x.size == 0:
                                    continue
                                label = f"{eid} (ref)" if int(eid) == int(ref_id) else str(eid)
                                sc = ax.scatter(x, y, s=22, label=label)
                                color = None
                                facecolors = sc.get_facecolors()
                                if len(facecolors) > 0:
                                    color = tuple(facecolors[0])
                                xf, yf = _trend_fit_curve(x, y, use_logx=use_logx, use_logy=use_logy)
                                if xf.size >= 2:
                                    ax.plot(
                                        xf,
                                        yf,
                                        linestyle="-" if int(eid) == int(ref_id) else "--",
                                        linewidth=1.0,
                                        color=color,
                                    )

                            try:
                                ax.set_xscale("log")
                            except Exception:
                                pass
                            if use_logy:
                                try:
                                    ax.set_yscale("log")
                                except Exception:
                                    pass

                            ax.set_xlabel("Shear rate γ̇ (1/s)")
                            ax.set_ylabel(Y_LABELS[y_choice])
                            ax.set_title("Selected experiments overlay")
                            ax.legend()
                            fig.tight_layout()
                            st.pyplot(fig, use_container_width=True)
                            plt.close(fig)

                            st.markdown("---")
                            st.markdown("### 误差分布（APE vs shear rate）")
                            st.caption("这里也改成只显示点，不再用实线把误差点连起来。")
                            fig2, ax2 = plt.subplots(figsize=(8.2, 5.0))
                            yref = aligned[f"ref_{ref_id}"].to_numpy(dtype=float)
                            for eid in selected_ids:
                                if int(eid) == int(ref_id):
                                    continue
                                yi = aligned[f"exp_{eid}"].to_numpy(dtype=float)
                                valid_pct = np.isfinite(yi) & np.isfinite(yref) & (np.abs(yref) > 0)
                                ape = np.full_like(xg, np.nan, dtype=float)
                                ape[valid_pct] = np.abs((yi[valid_pct] - yref[valid_pct]) / yref[valid_pct]) * 100.0
                                ax2.scatter(xg[valid_pct], ape[valid_pct], s=18, label=str(eid))

                            try:
                                ax2.set_xscale("log")
                            except Exception:
                                pass
                            ax2.set_xlabel("Shear rate γ̇ (1/s)")
                            ax2.set_ylabel("Absolute percent error (%)")
                            ax2.set_title(f"APE vs γ̇ (reference = {ref_id})")
                            ax2.legend()
                            fig2.tight_layout()
                            st.pyplot(fig2, use_container_width=True)
                            plt.close(fig2)

                            st.markdown("---")
                            st.markdown("### 下载对比结果")
                            out_xlsx = io.BytesIO()
                            with pd.ExcelWriter(out_xlsx, engine="openpyxl") as xw:
                                err_df.to_excel(xw, sheet_name="error_metrics", index=False)
                                aligned.to_excel(xw, sheet_name="aligned_curves", index=False)
                            _bytes_download_button(
                                "下载 compare_results.xlsx",
                                out_xlsx.getvalue(),
                                file_name="compare_results.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )

                            with st.expander("查看插值对齐后的数据表（aligned）", expanded=False):
                                st.dataframe(aligned.head(300), use_container_width=True)


with TAB_WHY12:
    st.subheader("为什么 12-blade 在你的实验里表现最好")
    st.markdown(
        """
下面这页是把你上传的 JOR Introduction 里的核心意思整理成一个软件内置说明页，方便你在 GitHub / Streamlit 上直接展示。

**在你这套实验条件下，12-blade 的优势可以概括成三点：**
- Newtonian 100 cSt 硅油标定里，12-blade 的 MAPE 和 Max APE 最低，说明它在低扭矩区的读数最稳。
- 在 weak gel / yogurt 里，低剪切几何依赖不一定只是 slip，更可能和 **partial yielding / spatial confinement** 有关。
- 从 regime-accessibility 的角度看，12-blade 更容易在可用应力窗口内进入 fully yielded / full-gap mobilization，同时又比 4-blade 更稳定。

> 这不是“12-blade 对所有材料都一定最好”的普适结论；它是你在当前 cup / vane 尺寸、材料、协议、扭矩分辨率下得到的最佳平衡。
        """
    )

    st.markdown("#### Newtonian benchmark（100 cSt）误差指标表")
    bench_df = pd.DataFrame(
        {
            "Geometry": ["12-blade", "24-blade", "4-blade", "C25 Printed", "C25 (metal)"],
            "MAPE (%)": [2.39, 9.26, 14.24, 15.28, 23.63],
            "Max APE (%)": [7.46, 16.71, 18.05, 20.81, 32.05],
        }
    )
    st.table(bench_df)

    st.markdown(
        r"""
#### 它和本软件的 Fig3 / Fig4 有什么关系？

- 本软件的 Fig3 / Fig4 使用的是 wide-gap Couette / vane-in-cup 的经典判据：
  \\(\tau_{1,c} = \tau_y (r_2/r_1)^2\\)
- 当 \\(\tau_1 < \tau_{1,c}\\) 时，即使扭矩稳定，也可能仍存在外侧未屈服环带。
- 所以真正重要的不是“扭矩稳不稳”，而是实验点有没有进入 fully mobilized regime。

在你的文档逻辑里，12-blade 被解释为在“耦合稳定性”和“更容易进入 fully yielded regime”之间给出了更好的折中。
        """
    )

    doc_path = BASE_DIR / "docs" / "JOR Introduction.docx"
    if doc_path.exists():
        _bytes_download_button(
            "下载 JOR Introduction.docx（原文）",
            data=doc_path.read_bytes(),
            file_name="JOR Introduction.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    md_path = BASE_DIR / "docs" / "JOR_Introduction.md"
    if md_path.exists():
        with st.expander("查看 JOR Introduction（文字版）", expanded=False):
            st.caption("说明：这是从 docx 自动提取的文字版；个别公式 / 排版可能与原文不完全一致。")
            st.markdown(_load_text_file(md_path))


with TAB_THEORY:
    st.subheader("Theory：partial yielding / wide-gap Couette / vane-in-cup")
    st.markdown(
        r"""
### 1) 应力分布（与本构无关）

在圆柱旋转（Couette / VIC）里，扭矩平衡给出径向应力衰减：

\[\tau(r)=\tau_1\left(\frac{r_1}{r}\right)^2\]

- \(\tau_1\)：内壁（vane / bob 表面）应力
- \(r_1\)：内半径（vane / bob）
- \(r_2\)：外半径（cup）

### 2) 全间隙动员（fully yielded）的几何判据

外壁应力：
\[\tau_2=\tau_1\left(\frac{r_1}{r_2}\right)^2\]

对 yield-stress 材料，如果 \(\tau_2 < \tau_y\)，则外侧可以保持未屈服：
\[\tau_1 < \tau_{1,c}\quad,\quad \tau_{1,c}=\tau_y\left(\frac{r_2}{r_1}\right)^2\]

本软件在 **Fig3** 中把 \(\tau_1 < \tau_{1,c}\) 的点标注为 “partial-yield compatible”。

### 3) 屈服半径 \(r_0\) 与 Fig4 的 \(r_0/r_2\)

定义屈服界面 \(r_0\) 满足 \(\tau(r_0)=\tau_y\)，则
\[r_0 = r_1\sqrt{\frac{\tau_1}{\tau_y}}\]

如果已经全屈服，则 \(r_0\) 不会超过 \(r_2\)，所以软件里做了截断：
\[r_0 = \min\left(r_2,\ r_1\sqrt{\frac{\tau_1}{\tau_y}}\right)\]

然后绘制 **Fig4：\(r_0/r_2\) vs shear rate**。

---

### 重要备注
本软件默认把导出的 **Shear Stress (Pa)** 当作 \(\tau_1\)（内壁应力）。如果你的仪器导出应力不是内壁应力，而是某种等效 / 换算量，需要在 `rheo/db.py -> compute_partial_yield()` 里把 \(\tau_1\) 的来源替换成你真正要用的定义。
        """
    )
