### Hi, I'm Carolina Lievanos 👋

Data scientist working on **machine learning and GenAI in fintech**, with an MSc in **Chemical Engineering**. I build models that hold up under the questions a risk committee, a regulator or a plant operator would ask: *Is it calibrated? Is it fair? What does it cost when it's wrong? Would it have worked last year?*

📍 Mexico · 🇪🇸 Spanish / 🇬🇧 English

---

#### 📂 Featured projects

| Project | What it shows | Stack |
|---|---|---|
| [**Financial RAG, evaluated**](https://github.com/c4r0l13/financial-rag-eval) | RAG over 84 SEC filings (12k pages), scored against FinanceBench's analyst-labelled evidence pages. Metadata filtering + domain query rewriting raise top-5 recall from 13% to 63%. Includes prompt-injection filtering and citation verification. | Python · BM25/LSA hybrid · Claude/OpenAI · PyMuPDF |
| [**Credit risk scorecard**](https://github.com/c4r0l13/credit-risk-scorecard) | WoE scorecard vs monotonic LightGBM, with calibration, fairness audit (four-fifths rule, equal opportunity) and TreeSHAP adverse-action reasons. Approves 5 more applicants per 100 at the same 12% risk appetite. | LightGBM · scikit-learn · SHAP |
| [**Credit risk API**](https://github.com/c4r0l13/credit-risk-api) | The scorecard's champion model in production: FastAPI, Docker, CI quality gates that block weaker models, Prometheus metrics and live PSI drift monitoring, stress-tested on a simulated downturn. | FastAPI · Docker · GitHub Actions · Prometheus |
| [**Card fraud detection**](https://github.com/c4r0l13/fraud-detection) | Leak-free velocity features, time-based validation and an alert threshold chosen by dollars rather than F1. Evaluated per attack pattern (card testing, account takeover, point of compromise). | LightGBM · MLflow |
| [**USD/MXN volatility & VaR**](https://github.com/c4r0l13/usdmxn-volatility-var) | 16-year walk-forward study: the exchange rate can't be forecast (and ML is significantly worse), volatility can, and only filtered historical simulation passes Kupiec and Christoffersen VaR backtests. | arch (GARCH/GJR) · statsmodels-style tests |
| [**Chemical process fault detection**](https://github.com/c4r0l13/tep-fault-detection) | Tennessee Eastman benchmark: PCA/DPCA control charts with calibrated limits (0.3% false alarms), contribution plots that recover the physical root cause, and a 21-fault LightGBM classifier. | PCA · LightGBM · SPC |

#### 🛠️ Toolbox

`Python` `pandas` `scikit-learn` `LightGBM` `SHAP` `arch` · `FastAPI` `Docker` `GitHub Actions` `MLflow` `Prometheus` · `RAG` `LLM evaluation` `Claude API` `OpenAI API` · `SQL`

#### 🎓 Background

- MSc in Chemical Engineering
- Diplomas in Artificial Intelligence and Data Science

<!-- Optional: add your LinkedIn and email -->
<!-- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/YOUR_HANDLE) -->
