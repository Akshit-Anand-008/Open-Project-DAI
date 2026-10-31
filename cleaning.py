import pandas as pd

# 1. Load your dataset (assuming you're using your dataframe)
df = pd.read_csv('dataAnalystJobsIndia.csv')

# 2. Define a list of major Tier-1 tech hubs in India
tier_1_hubs = ['bengaluru', 'bangalore', 'hyderabad', 'pune', 'mumbai', 'delhi', 'ncr', 'gurugram', 'chennai']

# 3. Create a categorization function
def categorize_location(loc):
    if pd.isna(loc):
        return 'Unknown'
    # Convert to lowercase to ensure matching works regardless of capitalization
    loc_lower = str(loc).lower()
    
    # Check if any Tier-1 hub name is inside the location string
    for hub in tier_1_hubs:
        if hub in loc_lower:
            return 'Tier-1 Tech Hub'

    # Otherwise, classify it as Non-Metro or Other
    return 'Non-Metro / Other'

# 4. Generate the new 'location_category' column
df['location_category'] = df['location'].apply(categorize_location)

df['min_salary_lpa'] = df['base salary'] / 100000


#5. Write it to new file
df.to_csv('cleaned_data.csv', index=False)
