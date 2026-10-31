import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.optimize import curve_fit


# Load dataset
df_clean = pd.read_csv('/content/cleaned_data.csv')
df_clean.columns = df_clean.columns.str.replace(' ', '_')

## 1) Using Analysis of Covariance(ANOVA) to figure out f and p statistics and find the possible covariance relationship value
def bin_experience(exp):
    if exp <= 3:
        return '0-3 Yrs'
    elif exp <= 6:
        return '4-6 Yrs'
    else:
        return '7+ Yrs'

df_clean['exp_group'] = df_clean['min_exp'].apply(bin_experience)

groups = [group['base_salary'].dropna().values for name, group in df_clean.groupby('exp_group')]

f_val, p_val = stats.f_oneway(*groups)
print(f"ANOVA F-statistic: {f_val:.4f}")
print(f"ANOVA p-value: {p_val:.4e}")

# covariance matrix between Experience and Salary
cov_matrix = df_clean[['min_exp', 'base_salary']].cov()
print("Covariance Matrix:")
display(cov_matrix)

# covariance value
cov_value = cov_matrix.loc['min_exp', 'base_salary']
print(f"\nDirect Covariance between Experience and Salary: {cov_value:,.2f}")


## 2) Using Regression to fit the curve/line and find relationship between salary growth and experience

# Clean Data
regression_data = df_clean[['min_exp', 'base_salary']].dropna()
x_data = regression_data['min_exp'].values
y_data = regression_data['base_salary'].values

# Segmented Regression Function
def segmented_model(x, b0, beta1, beta2):
    return np.where(x <= 6.5, b0 + beta1 * x, b0 + beta1 * 6.5 + beta2 * (x - 6.5))

# Fit Curve
popt, pcov = curve_fit(segmented_model, x_data, y_data)
perr = np.sqrt(np.diag(pcov))

param_names = ["Intercept (b0)", "Slope <= 6.5 (Beta 1)", "Slope > 6.5 (Beta 2)"]
for name, param, err in zip(param_names, popt, perr):
    print(f"{name}: {param:.2f} ± {err:.2f}")

# Plotting the Segmented Fit
plt.figure(figsize=(8, 5))
sns.scatterplot(x=x_data, y=y_data, alpha=0.4, label='Data Points')
x_plot = np.linspace(0, x_data.max(), 500)
y_plot = segmented_model(x_plot, *popt)
plt.plot(x_plot, y_plot, color='purple', linewidth=3, label='Segmented Fit (Cutoff = 6.5)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.title('Segmented Regression: Experience Return on Salary')
plt.legend()
plt.show()
