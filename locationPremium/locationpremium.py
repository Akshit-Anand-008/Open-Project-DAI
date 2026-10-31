import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_data.csv')
# ==============
# Stats to file
# ==============
summary_stats = df.groupby('location_category', observed=True)['min_salary_lpa'].agg(
    Job_Count='count',
    Mean_Salary_LPA='mean',
    Median_Salary_LPA='median',
    Std_Deviation='std'
).reset_index()

summary_stats.to_csv('hypothesis1_summary_stats.csv', index=False)

# =====
# Graph
# =====
df_plot = df.dropna(subset=['min_salary_lpa', 'min exp', 'location_category']).copy()
plt.figure(figsize=(10, 6))

# Separate data into Tier-1 Tech Hubs vs. Non-Metro / Other Cities
tier1 = df_plot[df_plot['location_category'] == 'Tier-1 Tech Hub']
non_metro = df_plot[df_plot['location_category'] != 'Tier-1 Tech Hub']

# Plot Tier-1 Tech Hubs (Blue points)
plt.scatter(
    tier1['min exp'], tier1['min_salary_lpa'], 
    color='#1f77b4', alpha=0.7, 
    label='Tier-1 Tech Hubs (Bengaluru, Hyd, etc.)', 
    edgecolors='black', s=60
)

# Plot Non-Metro / Other Cities (Orange points)
plt.scatter(
    non_metro['min exp'], non_metro['min_salary_lpa'], 
    color='#ff7f0e', alpha=0.7, 
    label='Non-Metro / Other Cities', 
    edgecolors='black', s=60
)


plt.title("Testing H1: Salary vs. Experience across Location Categories", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Minimum Required Experience (Years)", fontsize=12)
plt.ylabel("Minimum Base Salary (LPA)", fontsize=12)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save the chart
output_filename = 'hypothesis1_location_premium.png'
plt.savefig(output_filename, dpi=300)
plt.close()
