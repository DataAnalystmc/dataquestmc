#!/usr/bin/env python
# coding: utf-8

# In[2]:


import csv

# Function to explore data
def explore_data(dataset, start=0, end=5):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')  # adds a new (empty) line after each row

# Load Apple Store dataset
apple_store_file = 'AppleStore.csv'
with open(apple_store_file, encoding='utf8') as f:
    reader = csv.reader(f)
    apple_data = list(reader)

# Load Google Play Store dataset
google_play_file = 'googleplaystore.csv'
with open(google_play_file, encoding='utf8') as f:
    reader = csv.reader(f)
    google_data = list(reader)

# Explore first few rows of Apple Store dataset
print("Apple Store dataset:")
explore_data(apple_data[1:], 0, 3)  # Skipping header row

# Explore first few rows of Google Play Store dataset
print("Google Play Store dataset:")
explore_data(google_data[1:], 0, 3)  # Skipping header row

# Number of rows and columns in each dataset
num_rows_apple = len(apple_data) - 1  # Exclude header row
num_columns_apple = len(apple_data[0])
num_rows_google = len(google_data) - 1  # Exclude header row
num_columns_google = len(google_data[0])

(num_rows_apple, num_columns_apple), (num_rows_google, num_columns_google), apple_data[0], google_data[0]


# In[6]:


# Function to find rows with incorrect length
def find_incorrect_rows(dataset, expected_length):
    incorrect_rows = []
    for i, row in enumerate(dataset):
        if len(row) != expected_length:
            incorrect_rows.append((i, row))
    return incorrect_rows

# ... (Your existing code for loading the datasets and exploring them)

# Check for incorrect rows
expected_length_apple = len(apple_data[0])
incorrect_rows_apple = find_incorrect_rows(apple_data[1:], expected_length_apple)  # Exclude header

expected_length_google = len(google_data[0])
incorrect_rows_google = find_incorrect_rows(google_data[1:], expected_length_google)  # Exclude header

# Remove the incorrect row from Google Play dataset
if incorrect_rows_google:
    del google_data[incorrect_rows_google[0][0] + 1]  # +1 to account for the header row

# Verify if the row has been removed
incorrect_rows_google_after = find_incorrect_rows(google_data[1:], expected_length_google)

# Print results
print("Incorrect rows in Apple dataset:", incorrect_rows_apple)
print("Incorrect rows in Google dataset after removal:", incorrect_rows_google_after)


# In[7]:


# Re-load the Google Play dataset for comparison
with open(google_play_file, encoding='utf8') as f:
    reader = csv.reader(f)
    google_data_original = list(reader)

# Row at index 10472 in the original dataset before removal
incorrect_row_before = google_data_original[10472 + 1]  # +1 to account for the header row

# Row at index 10472 in the dataset after removal
incorrect_row_after = google_data[10472]  # We've already removed the header in this list

incorrect_row_before, incorrect_row_after


# In[9]:


# Full code to identify and count duplicate entries in the Google Play dataset

# Initialize empty lists to hold unique and duplicate app names
unique_apps = []
duplicate_apps = []

# Loop through the Google Play dataset to identify duplicates
for row in google_data[1:]:  # Skip the header row
    app_name = row[0]
    if app_name in unique_apps:
        duplicate_apps.append(app_name)
    else:
        unique_apps.append(app_name)

# Print some duplicate app names and count the total number of duplicates
duplicate_examples = duplicate_apps[:5]
duplicate_count = len(duplicate_apps)

# Print the results
print(f"Examples of duplicate apps: {duplicate_examples}")
print(f"Total number of duplicate apps: {duplicate_count}")


# In[10]:


# Step 1: Create a dictionary where each key is a unique app name and the corresponding value is the highest number of reviews of that app

# Initialize an empty dictionary named reviews_max
reviews_max = {}

# Loop through the Google Play data set to populate reviews_max
for row in google_data[1:]:  # Skip the header row
    name = row[0]
    n_reviews = float(row[3])  # The number of reviews is in the 4th column (index 3)
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

# Measure the length of the dictionary
len_reviews_max = len(reviews_max)

# Step 2: Use the reviews_max dictionary to remove duplicate rows

# Initialize two empty lists
android_clean = []  # To store the new cleaned data set
already_added = []  # To store app names that have already been added

# Loop through the Google Play dataset to populate android_clean and already_added
for row in google_data[1:]:  # Skip the header row
    name = row[0]
    n_reviews = float(row[3])
    
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(row)
        already_added.append(name)

# Measure the length of the cleaned dataset
len_android_clean = len(android_clean)

len_reviews_max, len_android_clean


# In[11]:


# Function to check if a string contains only common English characters
def is_english(string):
    for character in string:
        if ord(character) > 127:
            return False
    return True

# Test the function with example app names
test_names = ['Instagram', '爱奇艺PPS -《欢乐颂2》电视剧热播', 'Docs To Go™ Free Office Suite', 'Instachat 😜']
test_results = {name: is_english(name) for name in test_names}

test_results


# In[12]:


# Modified function to allow up to 3 non-ASCII characters
def is_english(string):
    non_ascii_count = 0
    for character in string:
        if ord(character) > 127:
            non_ascii_count += 1
        if non_ascii_count > 3:
            return False
    return True

# Test the modified function with example app names
test_names_modified = ['Docs To Go™ Free Office Suite', 'Instachat 😜', '爱奇艺PPS -《欢乐颂2》电视剧热播']
test_results_modified = {name: is_english(name) for name in test_names_modified}

# Filter out non-English apps from both datasets
english_apps_google = [app for app in android_clean if is_english(app[0])]
english_apps_apple = [app for app in apple_data[1:] if is_english(app[1])]  # App name is in the 2nd column for Apple dataset

# Check the number of rows remaining for each dataset
len_english_apps_google = len(english_apps_google)
len_english_apps_apple = len(english_apps_apple)

test_results_modified, len_english_apps_google, len_english_apps_apple


# In[13]:


# Function to convert price string to float
def price_to_float(price_str):
    return float(price_str.replace("$", ""))

# Initialize lists to store free apps
free_apps_google = []
free_apps_apple = []

# Loop through Google Play dataset to isolate free apps
for app in english_apps_google:
    price = app[7]  # Price is in the 8th column for Google dataset
    if price == '0':
        free_apps_google.append(app)

# Loop through Apple App Store dataset to isolate free apps
for app in english_apps_apple:
    price = app[4]  # Price is in the 5th column for Apple dataset
    if price_to_float(price) == 0.0:
        free_apps_apple.append(app)

# Check the number of free apps remaining in each dataset
len_free_apps_google = len(free_apps_google)
len_free_apps_apple = len(free_apps_apple)

len_free_apps_google, len_free_apps_apple


# In[16]:


# Combine the frequency table generation and organization into a single block of code

# Function to generate a frequency table for a given column index in a dataset
def freq_table(dataset, index):
    table = Counter()
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        table[value] += 1
    
    # Convert the frequency table to percentages
    table_percentages = {key: (value / total) * 100 for key, value in table.items()}
    
    return sorted(table_percentages.items(), key=lambda x: x[1], reverse=True)[:5]

# Generate and organize the top 5 categories/genres from both datasets into a single dictionary
organized_results_one_block = {
    "Top 5 Categories": {
        "Google Play Store (By Category)": freq_table(free_apps_google, 1),
        "Google Play Store (By Genres)": freq_table(free_apps_google, 9),
        "Apple App Store": freq_table(free_apps_apple, 11)
    }
}

organized_results_one_block



# In[17]:


# Function to display a frequency table in descending order
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = [(str(round(value, 2)) + '%', key) for key, value in table]
    table_sorted = sorted(table_display, reverse=True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

# Display frequency tables for the required columns
print("Frequency Table for Apple App Store (prime_genre):")
display_table(free_apps_apple, 11)  # 'prime_genre' is in the 12th column for Apple dataset
print("\nFrequency Table for Google Play Store (Genres):")
display_table(free_apps_google, 9)  # 'Genres' is in the 10th column for Google dataset
print("\nFrequency Table for Google Play Store (Category):")
display_table(free_apps_google, 1)  # 'Category' is in the 2nd column for Google dataset


# In[18]:


Based on the frequency tables, the App Store is heavily skewed towards entertainment apps, predominantly games. In contrast, Google Play shows a more balanced distribution between practical and entertainment apps, with a notable presence in the 'Family' and 'Tools' categories. A strategic approach might be to develop a family-friendly educational game, targeting both markets. However, it's important to note that a high number of apps in a given category doesn't necessarily equate to high user engagement or profitability. Further analysis on metrics like user reviews and download counts is advised for a more comprehensive strategy.
   


# In[19]:


# Generate frequency table for the 'prime_genre' column to get unique app genres in Apple App Store
unique_genres_apple = [genre for genre, _ in freq_table(free_apps_apple, 11)]

# Initialize an empty dictionary to store average user ratings for each genre
avg_user_ratings_apple = {}

# Loop over unique genres in Apple App Store
for genre in unique_genres_apple:
    total = 0  # Store the sum of user ratings for each genre
    len_genre = 0  # Store the number of apps specific to each genre
    
    # Loop over the App Store dataset
    for app in free_apps_apple:
        genre_app = app[11]  # App genre
        
        # Check if the app's genre matches the current genre in the loop
        if genre_app == genre:
            user_ratings = float(app[5])  # Number of user ratings
            total += user_ratings  # Add up the number of user ratings
            len_genre += 1  # Increment the number of apps for this genre
    
    # Compute the average number of user ratings for the genre
    avg_user_ratings = total / len_genre if len_genre else 0
    avg_user_ratings_apple[genre] = avg_user_ratings

# Sort the genres by average number of user ratings in descending order
sorted_avg_user_ratings_apple = sorted(avg_user_ratings_apple.items(), key=lambda x: x[1], reverse=True)

sorted_avg_user_ratings_apple


# In[26]:


Based on the data, Social Networking and Photo & Video apps get the most attention in the Apple App Store, judging by the average user ratings. Games are popular too, but they don't engage users as much as the top two. Even though these genres are getting high ratings, it doesn't automatically mean they're the most profitable. So, if I were to develop an app for the Apple App Store, I'd consider diving into the Social Networking or Photo & Video space, but I'd also dig deeper into other metrics like in-app purchases and user retention to get the full picture.


# In[27]:


# Generate frequency table for the 'Category' column to get unique app genres in Google Play Store
unique_categories_google = [category for category, _ in freq_table(free_apps_google, 1)]

# Initialize an empty dictionary to store average number of installs for each category
avg_installs_google = {}

# Loop over unique categories in Google Play Store
for category in unique_categories_google:
    total = 0  # Store the sum of installs for each category
    len_category = 0  # Store the number of apps specific to each category
    
    # Loop over the Google Play Store dataset
    for app in free_apps_google:
        category_app = app[1]  # App category
        
        # Check if the app's category matches the current category in the loop
        if category_app == category:
            # Remove any '+' or ',' character, and then convert the string to a float
            installs = float(app[5].replace('+', '').replace(',', ''))
            total += installs  # Add up the number of installs
            len_category += 1  # Increment the number of apps for this category
    
    # Compute the average number of installs for the category
    avg_installs = total / len_category if len_category else 0
    avg_installs_google[category] = avg_installs

# Sort the categories by average number of installs in descending order
sorted_avg_installs_google = sorted(avg_installs_google.items(), key=lambda x: x[1], reverse=True)

sorted_avg_installs_google


# In[28]:


Considering these numbers alongside the earlier analysis of the Apple App Store, developing a game app could potentially be profitable on both platforms. Notably, Tools and Family categories are also prominent on Google Play, aligning with earlier observations. Therefore, creating an app within the Game or Tools categories, or potentially a family-friendly game, could be a strategic move. However, the high number of installs doesn't automatically signify profitability, so a deeper analysis on other metrics is advisable for a complete strategy.


# In[ ]:




