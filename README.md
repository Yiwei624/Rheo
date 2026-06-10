# RheoDB — HB / Cross / Ellis 版本

这个版本已按要求只保留三个拟合模型：

- Herschel–Bulkley: `τ = τy + K γ̇^n`
- Cross: `η = η∞ + (η0 - η∞)/(1 + (τ/σc)^m)`
- Ellis: `η = η0/(1 + (τ/σc)^m)`

已移除分析流程中的 Power law 和 Bingham 拟合；新的 `fit_results` 表和导出表格会显示 HB 的 `tau_y_Pa, K, n`，以及 Cross/Ellis 的 `eta0_Pa_s, eta_inf_Pa_s, sigma_c_Pa, m`。

运行：

```bash
pip install -r requirements.txt
streamlit run app.py
```
