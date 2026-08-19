# IDXExchange Data Scientist
# California Home Price Prediction

Predicts single-family home sale prices in California using monthly MLS sales data.

## Dataset

- **Source:** CRMLS (California Regional MLS) monthly sold-listing exports, one CSV per month (`CRMLSSold{YYYY}{MM}.csv`), covering **Jan 2024 – Jun 2026**.
- Records are filtered to `PropertyType == "Residential"` and `PropertySubType == "SingleFamilyResidence"`.
- Final modeling set: ~333K rows, ~29 columns after feature engineering.

## Preprocessing

1. **`week1.py`** — loads all monthly CSVs, filters to single-family residential, saves `cleaned_single_family_sales.csv` + a column dictionary.
2. **`01_exploration.ipynb`** — checks distributions and correlations of core numeric features (price, living area, beds, baths, lot size).
3. **`02_preprocessing.ipynb`** — selects modeling columns, standardizes categorical dtypes, drops impossible rows (price ≤ 0, negative beds/baths, duplicates), adds missingness indicator flags, saves `cleaned_single_family_sales_preprocessed.csv`.
4. A feature-engineering step (not included in this upload) adds `BedBathRatio`, `PropertyAge`, and a `DistrictName` field, producing `cleaned_single_family_sales_engineered.csv`, which is the input to the later notebooks.

Imputation, encoding, and scaling are **not** done here — they're fit only on each model's training window (inside a scikit-learn `Pipeline`) to avoid leaking validation/test data into preprocessing decisions.

## Models Tested

All models use a chronological train/validation/test split (test = last complete month, validation = prior month), CV-safe target encoding for high-cardinality categoricals (e.g. `City`), and a training-window length tuned on the validation month only.

| Model | Test R² | Notes |
|---|---|---|
| Linear Regression (baseline) | 0.767 | Interpretable, smallest overfit gap |
| Decision Tree | 0.813 | Captures nonlinearity, higher variance |
| Random Forest | 0.840 | Best of the tree ensembles pre-boosting |
| **XGBoost (gradient boosting)** | **0.870** | Best overall; light hyperparameter search (`max_depth` 7–9, `learning_rate` 0.03–0.1) |

## Best Result (XGBoost, `max_depth=9`, `learning_rate=0.05`, 622 trees)

- **R²:** 0.870
- **MAPE:** 15.05% | **MdAPE:** 9.86% | **MAE:** $189,284
- Accuracy is best in the mid-price range (~$575K–$800K, MdAPE 7.7%) and worst at the high end (>$1.65M, MdAPE 13.3%), where prices are more volatile and harder to predict.
- Top predictive features: target-encoded `City`, `LivingArea`, `Bathrooms`.

## How to Re-Run

**Requirements:** `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`, `seaborn`

```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn
```

**Data layout:** place monthly source CSVs in a `california/` folder next to `week1.py`, named `CRMLSSold{YYYY}{MM}.csv`.

**Run in order** (each step reads the previous step's output CSV):

1. `python week1.py`
2. `01_exploration.ipynb`
3. `02_preprocessing.ipynb`
4. (feature engineering step → `cleaned_single_family_sales_engineered.csv`)
5. `03_baseline_model.ipynb`
6. `04_model_comparison.ipynb`
7. `05_advanced_models.ipynb`
8. `06_evaluation.ipynb`

Launch notebooks with:
```bash
jupyter notebook
```
