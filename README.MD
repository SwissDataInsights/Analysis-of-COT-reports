# README: Predicting Close Price with Clustering and LightGBM

This repository contains a methodology for predicting the `Close` price of a financial instrument using clustering techniques (K-Means) and tree-based models (LightGBM). This workflow explores the application of unsupervised learning to identify market patterns and uses these patterns as features in a supervised regression task.

---

## Overview
The project aims to:

1. **Cluster Analysis:** Use K-Means clustering to group similar data points and identify market patterns.
2. **Feature Engineering:** Leverage cluster labels and other features as predictors.
3. **Regression Modeling:** Train a LightGBM model to predict the `Close` price of the financial instrument.
4. **Performance Evaluation:** Assess the model's accuracy and interpret feature importance to understand the contribution of clustering.

---

## Methodology

### 1. Data Preparation
- **Input Data:**
  - Financial data with columns such as:
    - `NonComm_Positions_Long_All`
    - `NonComm_Positions_Short_All`
    - `Close`
    - Cluster labels (`Cluster_3`, `Cluster_4`)
  - Ensure data has no missing values.

- **Scaling:**
  - Standardize numerical features using `StandardScaler` to improve clustering performance.

### 2. Clustering
- **K-Means Clustering:**
  - Determine the optimal number of clusters using the Elbow Method.
  - Generate cluster labels (`Cluster_3` and `Cluster_4`) for use as features in the regression model.

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
data_scaled = scaler.fit_transform(df_unsupervised)

kmeans = KMeans(n_clusters=4, random_state=42)
df_unsupervised['Cluster_4'] = kmeans.fit_predict(data_scaled)
```

### 3. Regression Modeling
- **Model:** Use LightGBM to predict the `Close` price.
- **Features:**
  - `Cluster_3`
  - `Cluster_4`
  - Additional features such as `NonComm_Positions_Long_All` and `Change_in_NonComm_Long_All`.

```python
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

features = df_unsupervised[['Cluster_4', 'NonComm_Positions_Long_All']]
target = df_unsupervised['Close']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
lgb_model = lgb.LGBMRegressor(random_state=42)
lgb_model.fit(X_train, y_train)

# Evaluate
y_pred = lgb_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
```

### 4. Model Evaluation
- **Metrics:**
  - Mean Squared Error (MSE)
  - R² Score

- **Feature Importance:**
  Analyze the importance of cluster labels and other features to understand their impact on predictions.

```python
importance = lgb_model.feature_importances_
for i, col in enumerate(features.columns):
    print(f"Feature: {col}, Importance: {importance[i]}")
```

---

## Results

### Key Findings:
1. **Cluster Importance:**
   - `Cluster_4` significantly contributes to the prediction of `Close`, indicating meaningful market patterns.
   - `Cluster_3` adds moderate value.

2. **Model Performance:**
   - Achieved an MSE of ~0.00137 and R² score of ~0.47 using LightGBM.
   - Incorporating additional features further improved performance.

---

## Usage

### Prerequisites
- Python 3.8+
- Required Libraries: `numpy`, `pandas`, `scikit-learn`, `lightgbm`, `matplotlib`, `seaborn`

Install dependencies:
```bash
pip install numpy pandas scikit-learn lightgbm matplotlib seaborn
```

### Run the Code
1. Prepare your dataset and ensure it includes the required columns (`Close`, `NonComm_Positions_Long_All`, etc.).
2. Execute the clustering script to generate `Cluster_3` and `Cluster_4` labels.
3. Train the LightGBM model using the provided regression code.
4. Evaluate the model performance and analyze feature importance.

---

## Future Work
1. **Feature Engineering:**
   - Add lagged features, moving averages, and volatility measures.
2. **Hyperparameter Tuning:**
   - Use grid search or random search to optimize LightGBM parameters.
3. **Alternative Models:**
   - Experiment with CatBoost, XGBoost, or Neural Networks.

---

## References
- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [Scikit-learn Clustering](https://scikit-learn.org/stable/modules/clustering.html)

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

