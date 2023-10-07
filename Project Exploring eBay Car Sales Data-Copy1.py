#!/usr/bin/env python
# coding: utf-8

# In[3]:


#This project focuses on cleaning and analyzing a dataset of used car listings from eBay Kleinanzeigen, a section of the German eBay website. The dataset has been modified to include 50,000 data points and introduces some noise to simulate a scraped dataset. Using Python libraries like pandas and NumPy, the objective is to clean this data for a meaningful analysis. Key features of interest include car price, vehicle type, brand, and other attributes that could influence the buying decision.


# In[9]:


import pandas as pd

# Read the CSV file into a DataFrame
autos = pd.read_csv('autos.csv', encoding='Latin-1')

# Display existing column names
existing_columns = autos.columns
existing_columns


# In[23]:


# Rename the columns based on the instructions
new_columns = [
    'date_crawled', 'name', 'seller', 'offer_type', 'price', 'ab_test',
    'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
    'odometer_km', 'registration_month', 'fuel_type', 'brand',
    'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
    'last_seen'
]

# Assign the new column names back to the DataFrame
autos.columns = new_columns

# Display first few rows to verify changes
autos.head()




# In[24]:


# Use DataFrame.describe() to look at descriptive statistics for all columns
autos.describe(include='all')


# In[25]:


# Convert 'price' and 'odometer_km' to numeric types after removing non-numeric characters
# Already converted in this data, but here's how you could do it:

# autos['price'] = autos['price'].str.replace('$','').str.replace(',','').astype(int)
# autos['odometer_km'] = autos['odometer_km'].str.replace('km','').str.replace(',','').astype(int)

# Check the data again to confirm changes
autos.describe(include='all')


# In[35]:


import pandas as pd

# Assuming the autos.csv file is already loaded into the DataFrame 'autos'
# If not, uncomment the next line
# autos = pd.read_csv('/mnt/data/autos.csv', encoding='Latin-1')

# Explore odometer_km
unique_odometer = autos['odometer_km'].unique().shape
describe_odometer = autos['odometer_km'].describe()
value_counts_odometer = autos['odometer_km'].value_counts().sort_index(ascending=True).head()

# Explore price
unique_price = autos['price'].unique().shape
describe_price = autos['price'].describe()
value_counts_price = autos['price'].value_counts().sort_index(ascending=True).head()

unique_odometer, describe_odometer, value_counts_odometer, unique_price, describe_price, value_counts_price



# In[38]:


# Sample DataFrame for demonstration
sample_data = {
    'date_crawled': ['2016-03-26 17:47:46', '2016-04-04 13:38:56', '2016-03-26 18:57:24', '2016-03-12 16:58:10', '2016-04-01 14:38:50'],
    'ad_created': ['2016-03-26 00:00:00', '2016-04-04 00:00:00', '2016-03-26 00:00:00', '2016-03-12 00:00:00', '2016-04-01 00:00:00'],
    'last_seen': ['2016-04-06 06:45:54', '2016-04-06 14:45:08', '2016-04-06 20:15:37', '2016-03-15 03:16:28', '2016-04-01 14:38:50']
}

sample_df = pd.DataFrame(sample_data)

# Extract first 10 characters for each date column
sample_df['date_crawled'] = sample_df['date_crawled'].str[:10]
sample_df['ad_created'] = sample_df['ad_created'].str[:10]
sample_df['last_seen'] = sample_df['last_seen'].str[:10]

# Calculate the distribution of values as percentages
date_crawled_dist = sample_df['date_crawled'].value_counts(normalize=True, dropna=False).sort_index()
ad_created_dist = sample_df['ad_created'].value_counts(normalize=True, dropna=False).sort_index()
last_seen_dist = sample_df['last_seen'].value_counts(normalize=True, dropna=False).sort_index()

date_crawled_dist, ad_created_dist, last_seen_dist



# In[39]:


# Sample data for demonstration
registration_year_data = [1900, 1950, 2000, 2010, 2015, 2020, 3000, 9999]

# Count the number of listings that fall outside the 1900 - 2016 interval
out_of_bounds = [year for year in registration_year_data if year < 1900 or year > 2016]
percentage_out_of_bounds = len(out_of_bounds) / len(registration_year_data) * 100

out_of_bounds, percentage_out_of_bounds


# In[40]:


# Sample data after removing outliers
filtered_registration_year_data = [year for year in registration_year_data if 1900 <= year <= 2016]

# Calculate the distribution of the remaining values
from collections import Counter

distribution = Counter(filtered_registration_year_data)
normalized_distribution = {k: v / len(filtered_registration_year_data) for k, v in distribution.items()}

normalized_distribution


# In[48]:


# First, let's load the cleaned dataset
import pandas as pd

# Load the dataset
autos_path = 'autos.csv'
autos = pd.read_csv(autos_path, encoding='latin-1')

# Cleaning 'price' column
autos['price'] = autos['price'].str.replace('$', '').str.replace(',', '').astype(int)

# Cleaning 'odometer' column
autos['odometer'] = autos['odometer'].str.replace('km', '').str.replace(',', '').astype(int)
autos.rename(columns={'odometer': 'odometer_km'}, inplace=True)

# Show the first few rows to confirm
autos.head()

# Explore the unique values in the 'brand' column and their frequencies
brand_counts = autos['brand'].value_counts(normalize=True) * 100

# Display the brands and their percentages in the dataset
brand_counts

# Brands to aggregate by (those that make up at least 5% of the dataset)
selected_brands = brand_counts[brand_counts > 5].index

# Create an empty dictionary to hold aggregate data
brand_mean_price = {}

# Loop over selected brands to calculate mean price
for brand in selected_brands:
    mean_price = autos.loc[autos['brand'] == brand, 'price'].mean()
    brand_mean_price[brand] = round(mean_price, 2)

# Display the dictionary of aggregate data
brand_mean_price




# In[54]:


# Recalculate mean mileage for each of the top brands using the correct column name
brand_mean_mileage = {}

for brand in selected_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_mileage = brand_only["odometer_km"].mean()  # Corrected here
    brand_mean_mileage[brand] = mean_mileage

# Convert both dictionaries to series objects
mean_mileage_series = pd.Series(brand_mean_mileage).sort_values(ascending=False)
mean_prices_series = pd.Series(brand_mean_price).sort_values(ascending=False)  # Assuming brand_mean_price is already calculated

# Create a dataframe from the first series object
brand_info_df = pd.DataFrame(mean_prices_series, columns=['mean_price'])

# Assign the other series as a new column in this dataframe
brand_info_df['mean_mileage'] = mean_mileage_series

brand_info_df


# In[56]:





# In[ ]:




