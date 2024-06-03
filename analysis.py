import pandas as pd
from collections import Counter

# Load the scraped data
data = pd.read_csv('smart_locks.csv')

# Inspect data for missing or inconsistent values
print(data.info())
print(data.describe())

# Handle missing values if any (e.g., drop or impute)
data = data.dropna()

# Ensure correct data types
data['Price'] = data['Price'].astype(int)
data['Rating'] = data['Rating'].astype(float)
data['Rating count'] = data['Rating count'].astype(int)
data['Review count'] = data['Review count'].astype(int)
data['Ranking'] = data['Ranking'].astype(int)

print(data.head())

# Analysis
# Number of brands in the segment
num_brands = data['Brand name'].nunique()
print(f"Number of brands: {num_brands}")

# Count of SKUs per brand
skus_per_brand = data['Brand name'].value_counts()
print(skus_per_brand)

# Relative ranking calculation
def relative_ranking(df):
    brand_ranks = df.groupby('Brand name')['Ranking'].apply(list)
    relative_ranks = {brand: sum(ranks)/len(ranks) for brand, ranks in brand_ranks.items()}
    return relative_ranks

relative_ranks = relative_ranking(data)
print(relative_ranks)

# Relative rating calculation
def relative_rating(df):
    brand_ratings = df.groupby('Brand name')['Rating'].apply(list)
    relative_ratings = {brand: sum(ratings)/len(ratings) for brand, ratings in brand_ratings.items()}
    return relative_ratings

relative_ratings = relative_rating(data)
print(relative_ratings)

# Price distribution of SKUs
price_bins = [0, 3000, 5000, 10000, 15000, 20000, float('inf')]
price_labels = ['<INR 3000', 'INR 3000-4999', 'INR 5000-9999', 'INR 10000-14999', 'INR 15000-19999', '>INR 20000']
data['Price Band'] = pd.cut(data['Price'], bins=price_bins, labels=price_labels)

price_distribution = data['Price Band'].value_counts().sort_index()
print(price_distribution)

# Save analysis results to CSV
analysis_results = {
    'Number of Brands': num_brands,
    'SKUs per Brand': skus_per_brand.to_dict(),
    'Relative Ranks': relative_ranks,
    'Relative Ratings': relative_ratings,
    'Price Distribution': price_distribution.to_dict()
}

analysis_df = pd.DataFrame(list(analysis_results.items()), columns=['Metric', 'Value'])
analysis_df.to_csv('analysis_results.csv', index=False)