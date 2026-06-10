# RheoDB — HB / Cross / Ellis + Cross Partial Yield 版本

这个版本保留三个拟合模型：

- Herschel–Bulkley: `τ = τy + K γ̇^n`
- Cross: `η = η∞ + (η0 - η∞)/(1 + (τ/σc)^m)`
- Ellis: `η = η0/(1 + (τ/σc)^m)`

并新增 **Fig7：Cross-informed partial-yield map**。

Fig7 把 Cross 模型得到的临界应力 `σc,Cross` 当作 apparent yield stress，再代入 partial yield 理论：

```text
τ1,c,Cross = σc,Cross · (r2/r1)^2
r0,Cross/r2 = min[1, (r1/r2) · sqrt(τ1/σc,Cross)]
```

输出内容包括：

- `fig5_hb_fit_tau_vs_gammadot.png`
- `fig6_model_comparison_eta_vs_tau.png`
- `fig7_cross_partial_yield_map.png`
- `fit_summary.csv`
- `results_overview.xlsx`

`results_overview.xlsx` 的 derived metrics 中新增：

- `sigma_c_cross_up/down/all_Pa`
- `tau1c_cross_up/down/all_Pa`
- `cross_partial_fraction_up/down/all`

运行：

```bash
pip install -r requirements.txt
streamlit run app.py
```
