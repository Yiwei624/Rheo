# RheoDB (Streamlit)

一个用于 **流变（steady shear / flow-curve）实验数据**的轻量级数据库 + 自动分析工具。

你可以：
- 导入 rheometer 导出的 **CSV / XLSX**（包含 shear rate / shear stress / viscosity 等列）
- 存入 SQLite 数据库
- 自动识别 **up/down sweep**（如果存在）
- 自动输出：
  - Fig1: τ vs γ̇
  - Fig2: η vs γ̇
  - Fig3: τ vs γ̇ + **partial yield** 判据标注（需要 r1,r2 + HB 拟合 τy）
  - Fig4: r0/r2 vs γ̇（需要 r1,r2 + HB 拟合 τy）
- 自动拟合并生成表格：
  - Power law（up/down 分开拟合；没有 up/down 则整体拟合）
  - Bingham（同上）
  - Herschel–Bulkley（同上；τy 初值来自你导入时输入的 yield0）
  - Hysteresis Area（仅在 up/down 同时存在时计算）

---

## 目录结构

- `app.py`：Streamlit 主程序
- `rheo/`：核心逻辑（SQLite + 拟合 + 出图）
- `assets/`：CSV/XLSX 模板、示例数据
- `docs/`：你上传的文档（用于“为什么 12-blade 更好”页面）
- `data/`：默认数据库目录（本地使用）
- `outputs/`：分析输出（图 + 表）
- `uploads/`：临时保存上传的原始文件

> 注意：`.gitignore` 默认忽略 `data/ outputs/ uploads/`，避免把实验数据直接推到 GitHub。

---

## 本地运行

```bash
# 1) 创建虚拟环境（可选但推荐）
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate

# 2) 安装依赖
pip install -r requirements.txt

# 3) 启动
streamlit run app.py
```

打开页面后：
1. 左侧初始化数据库
2. 去“① 导入实验”上传 CSV/XLSX
3. 去“② 实验浏览 & 分析”选择 experiment_id，一键分析与下载

你也可以去 **“③ 多实验对比分析”**：
- 多选已经入库的实验
- 手动指定 shear rate 的 x 区间
- 选择一个 reference 实验
- 自动计算其它实验相对 reference 的误差（MAPE / Max APE / RMSE 等）并导出 Excel

---

## 部署到 Streamlit Community Cloud

- 把整个仓库推到 GitHub
- Streamlit Cloud 选择你的 repo，并把 **入口文件**设为 `app.py`

> 说明：Streamlit Cloud 的文件系统通常是临时的；如果你希望长期保存数据库，请在侧边栏定期下载 `.sqlite` 备份，或者把数据库存到外部持久化存储（如 S3 / Drive / 数据库服务）。

---

## 数据列要求

程序会尽量自动匹配列名（大小写/空格/单位符号不敏感）。常见列名：

- Shear Rate 1/s
- Shear Stress Pa
- Viscosity Pas
- Target Shear Rate 1/s
- Percentage Deviation %
- Temperature ℃
- Time s
- Thrust g
- Accumulated Time s
- Torque Nm
- Angular Velocity rad/s
- Notes

---

## 重要物理假设

本工具在 partial-yield 判断与 r0/r2 计算里默认：
- 导出的 **Shear Stress (Pa)** 视作内壁应力 \(\tau_1\)

如果你的仪器软件导出的应力不是 \(\tau_1\)，需要你在 `rheo/db.py -> compute_partial_yield()` 内替换定义。
