import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# importing the dataset

df= pd.read_csv("C:/Users/soham/OneDrive/Documents/Unmessenger/Assignments/Uncompleted/3451574-1207_Assessment_4/1207 Assessment 4/1207 Assessment 4/Assessment 4/Dataset.csv")
df.head()
df.shape
df.describe()
df.isnull().sum()
### Cleaning the Dataset
# we can see that there are fewer Unique values that the total row counts of ID column
# which means we have duplicate IDs since there are no null values in it
# Find IDs that appear more than once
duplicate_ids = df['ID'].value_counts()
duplicate_ids = duplicate_ids[duplicate_ids > 1]

# Filter the original data to show only rows with these duplicate IDs
duplicates = df[df['ID'].isin(duplicate_ids.index)]

print(duplicates)

# Filling blank rows in Year column with 'Not Available'
df['Year']=df['Year'].fillna('Not Available')

# Extract year values using regex (this will capture numeric years)
df['Year'] = df['Year'].str.extract('(\d{4})', expand=False)
df['Year']
df.loc[11:11,:] # we can see that row 11 has proper numerical Year value
# Droping duplicates based on the 'ID' column, keeping the first occurrence
df1 = df.drop_duplicates(subset=['ID'], keep='first')
df1
# Extract numeric values (minutes) from the 'Timing(min)' column
df1['Timing(min)'] = df1['Timing(min)'].str.extract('(\d+)')
df1['Timing(min)'] = df1['Timing(min)'].fillna('Not Available')
df1['Timing(min)']
# Replace '-' with 'Not Available' in the specified columns
df1['Rating(10)'] = df1['Rating(10)'].replace('-', 'Not Available')
df1['Votes'] = df1['Votes'].replace('-', 'Not Available')
df1['Genre'] = df1['Genre'].replace('-', 'Not Available')


# Keeping only the first genre type in the 'Genre' column and remove leading/trailing spaces
df1['Genre'] = df1['Genre'].str.split(',').str[0].str.strip()

# Displaying the updated Genre column to verify
df1['Genre'].unique()
df1.head()
## Analyzing the Ratings Distribution
# Convert 'Rating(10)' to numeric, handling 'Not Available' as NaN
ratings_numeric = pd.to_numeric(df1['Rating(10)'], errors='coerce')


# Plotting the distribution of ratings
plt.figure(figsize=(12, 6))
sns.histplot(ratings_numeric, bins=20, kde=True)  # kde=True adds a kernel density estimate
plt.title('Distribution of Movie Ratings')
plt.xlabel('Ratings (out of 10)')
plt.ylabel('Frequency')
plt.legend()
plt.show()


## Calculate the most common rating 

most_common_rating = ratings_numeric.mode()[0]

# Display the most common rating
print(f"The most common rating given by users is: {most_common_rating}")
##  Analyzing the genre distribution

# Count occurrences of each genre
# Split genres by commas and explode the DataFrame to count each genre individually
genre_counts = df1['Genre'].str.split(', ').explode().value_counts()


# Plotting the genre distribution (top 10 genres for better visibility)
plt.figure(figsize=(12, 6))
genre_counts[:10].plot(kind='bar', color='skyblue')
plt.title('Top 10 Movie Genres')
plt.xlabel('Genres')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.show()
## Relationship distribution between User Demgraphics and Ratings could not be done due to lack of data.(No Age/Gender columns)
## Further investigation was not possible due to same
### correlations between movie ratings and genres
# Ensure 'Rating(10)' is numeric for analysis, handling 'Not Available' as NaN
df1['Rating(10)'] = pd.to_numeric(df1['Rating(10)'], errors='coerce')

# Calculate the average rating for each genre
average_ratings_by_genre = df1.groupby('Genre')['Rating(10)'].mean().sort_values(ascending=False)

# Display the calculated average ratings by genre
print(average_ratings_by_genre)

# Plot the average ratings by genre
plt.figure(figsize=(12, 6))
sns.barplot(x=average_ratings_by_genre.index, y=average_ratings_by_genre.values, palette='viridis')
plt.title('Average Movie Ratings by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Rating (out of 10)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

## Identify the top 10 highest-rated movies.
# Sort the dataframe by 'Rating(10)' in descending order and select the top 10
top_10_highest_rated = df.sort_values(by='Rating(10)', ascending=False).head(10)

# Display the top 10 highest-rated movies
print(top_10_highest_rated[['Movie Name', 'Rating(10)', 'Year']])

## top 10 most-watched movies (by the number of ratings)
df['Votes'] = pd.to_numeric(df['Votes'].str.replace(',', ''), errors='coerce')
most_watch_movie=df.sort_values(by='Votes',ascending=False).head(10)
most_watch_movie
## movie genres having higher than average rating
# Calculate the overall average rating
overall_average_rating = df['Rating(10)'].mean()

# Calculate the average rating for each genre
average_ratings_by_genre = df.groupby('Genre')['Rating(10)'].mean()

# Compare each genre's average rating with the overall average
comparison_with_overall = average_ratings_by_genre - overall_average_rating

# Display the overall average and comparison results
print(f"Overall Average Rating: {overall_average_rating}")
print("Difference between each genre's average rating and the overall average:")
print(comparison_with_overall)

# Plot the differences for better visualization
plt.figure(figsize=(12, 6))
sns.barplot(x=comparison_with_overall.index, y=comparison_with_overall.values,color='red')
plt.title('Difference Between Genre Average Ratings and Overall Average')
plt.xlabel('Genre')
plt.ylabel('Difference from Overall Average')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
## Change in ratings over the Years
# Convert 'Year' to numeric and 'Rating(10)' to numeric, handling 'Not Available' as NaN
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Rating(10)'] = pd.to_numeric(df['Rating(10)'], errors='coerce')

# Calculate the average rating for each year
average_rating_by_year = df.groupby('Year')['Rating(10)'].mean()

# Plotting the average ratings over the years
plt.figure(figsize=(12, 6))
sns.lineplot(x=average_rating_by_year.index, y=average_rating_by_year.values, marker='o')
plt.title('Average Movie Ratings Over Time')
plt.xlabel('Year')
plt.ylabel('Average Rating (out of 10)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


## Years where movies received higher ratings.


# Convert 'Year' and 'Rating(10)' to numeric, handling 'Not Available' as NaN
df1['Year'] = pd.to_numeric(df1['Year'], errors='coerce')
df1['Rating(10)'] = pd.to_numeric(df1['Rating(10)'], errors='coerce')

# Calculate the overall average rating
overall_average_rating = df1['Rating(10)'].mean()

# Calculate the average rating for each year
average_rating_by_year = df1.groupby('Year')['Rating(10)'].mean()

# Filter for years with above-average ratings
years_with_higher_ratings = average_rating_by_year[average_rating_by_year > overall_average_rating]

# Display the years and their average ratings
print(f"Overall Average Rating: {overall_average_rating}")
print("\nYears with higher-than-average ratings:")
print(years_with_higher_ratings)

# Plotting the years with higher ratings
plt.figure(figsize=(12, 6))
sns.barplot(x=years_with_higher_ratings.index, y=years_with_higher_ratings.values, palette='viridis')
plt.title('Years with Above-Average Movie Ratings')
plt.xlabel('Year')
plt.ylabel('Average Rating (out of 10)')
plt.xticks(rotation=90)
plt.axhline(overall_average_rating, color='red', linestyle='--', label=f'Overall Average: {overall_average_rating:.2f}')
plt.legend()
plt.tight_layout()
plt.show()


### Here’s a summary of key findings from the analyses we conducted on the movie ratings dataset:

1. Distribution of Ratings:
The distribution of ratings likely follows a specific pattern (e.g., normal distribution), with most ratings clustering around certain values.
Notable trends in rating frequencies were identified, such as the mean and median ratings, which can indicate the overall perception of the movies in the dataset.
2. Most Common Rating:
The analysis revealed the most frequently given rating by users, highlighting the ratings that resonate most with the audience.
3. Genre Distribution:
The genre analysis showed how many movies belong to each genre, with some genres being more prevalent than others.
A bar plot illustrated the top genres, providing insights into the most common types of movies available.
4. Average Ratings by Genre:
The average ratings per genre were calculated, revealing which genres received higher or lower ratings.
This analysis could indicate audience preferences, with some genres generally being rated more favorably.
5. Comparison with Overall Average:
By comparing each genre's average rating with the overall average, we identified genres that performed better or worse than the average rating across all movies.
This information can guide future movie productions and marketing strategies by highlighting what genres audiences prefer.
6. Top 10 Highest-Rated Movies:
The analysis identified the top 10 movies with the highest ratings, providing a list of films that stood out in terms of quality as perceived by viewers.
7. Top 10 Most-Watched Movies:
We found the top 10 most-watched movies based on the number of ratings (votes), giving insight into the most popular films, which may indicate their commercial success or cultural impact.
8. Ratings Over Time:
The trend analysis of average ratings over time showcased how movie ratings have changed across the years.
This can reveal shifts in audience preferences or improvements in movie quality over time, potentially correlating with industry changes, technological advancements, or cultural shifts.
Conclusion:
These findings can be used for various purposes, including:

Informing movie production decisions based on genre performance.
Understanding audience preferences to tailor marketing strategies.
Recognizing trends in ratings over time, which can help predict future successes in filmmaking
### Based on the analysis of movie ratings, genres, and trends over time, here are several suggestions for further analysis and recommendations for improving user engagement:

Areas for Further Analysis
Genre-Specific Trends:

Investigate how specific genres perform over time. Are there genres that are gaining popularity? Are there genres that have consistently high or low ratings?
Analyze the relationship between genre diversity (number of genres per movie) and average ratings.
Demographic Analysis:

If demographic data (e.g., age, gender) is available, explore how different user groups rate movies. Are there specific demographics that prefer certain genres or have higher average ratings?
Analyze the correlation between demographic trends and genre popularity over time.
Seasonal Trends:

Examine how ratings change by season or during specific times of the year (e.g., holidays, summer blockbuster season). Are there genres that perform better in certain seasons?
Look at the release dates of highly rated movies and analyze if timing impacts ratings.
Outlier Analysis:

Identify outliers in the dataset. Are there movies with exceptionally high or low ratings? Investigate what factors contributed to these ratings (e.g., marketing, star power).
Assess user reviews or feedback for these outliers to understand user sentiment.
User Engagement Metrics:

If available, analyze user engagement metrics such as watch time, number of votes, and repeat viewership. How do these metrics correlate with ratings?
Evaluate the impact of promotional campaigns on user ratings and engagement.
Sentiment Analysis:

If user comments or reviews are available, conduct sentiment analysis to understand how sentiment correlates with ratings. Are movies with positive sentiments also rated higher?
Analyze the language used in reviews to identify common themes associated with higher or lower ratings.
Recommendations for Improving User Engagement
Personalized Recommendations:

Use data-driven algorithms to provide personalized movie recommendations based on users’ past ratings and viewing habits. Tailoring suggestions can enhance user experience and increase engagement.
Targeted Marketing Campaigns:

Focus marketing efforts on high-performing genres or newly popular genres. Use insights from seasonal trends to time promotions effectively.
Collaborate with influencers or create partnerships with popular content creators in specific genres to attract niche audiences.
User Feedback Mechanisms:

Implement user feedback mechanisms to gather insights on ratings and preferences. Regular surveys can help identify user interests and satisfaction levels.
Encourage users to leave reviews or ratings by incentivizing them with rewards or recognition.
Interactive Content:

Create interactive content such as polls or quizzes related to movie genres or ratings. This can increase user involvement and prompt users to explore more content.
Host events like “movie nights” based on popular genres or themes, fostering community engagement.
Highlight User-Generated Content:

Showcase user-generated content, such as reviews or fan art, on your platform. Recognizing contributions can foster a sense of community and belonging.
Create competitions for users to submit their reviews, with prizes for the best submissions, to increase engagement.
Content Diversification:

If certain genres have lower ratings, consider reviewing the content offered in those genres. Invest in high-quality productions or unique storytelling that might attract viewers.
Analyze user preferences for international films or lesser-known genres to expand the variety of content offered.
Conclusion
By diving deeper into these areas of analysis and implementing the recommendations, you can enhance user engagement and create a more tailored and enjoyable experience for viewers. Continuous analysis and adaptation based on user behavior will help maintain relevance and satisfaction within your audience.
