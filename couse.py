import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("online_courses_uses.csv")

df.head()

df.info()

df.isna().sum()

df.describe()

# Numbers Of Courses 

num_course = df['Course_ID'].nunique()  
print('Number of unique courses is ' + str(num_course))

# Maximum Duration

max_dur = df['Duration (hours)'].max()  
course_name = df[df['Duration (hours)'] == max_dur]['Course_Name'].values[0]
print("Max course duration is: " + str(max_dur))
print("Course with max duration is: " + course_name) 

# Minimum Duration

min_dur = df['Duration (hours)'].min()  
course_name = df[df['Duration (hours)'] == min_dur]['Course_Name'].values[0]
print("min course duration is: " + str(min_dur))
print("Course with min duration is: " + course_name)

# No of platforms

platforms = df['Platform'].nunique()
print("Number of platforms: " + str(platforms))

# Most common platform

most_common_platform = df['Platform'].value_counts().idxmax()  
print("The most commonly used platform is: " + most_common_platform)

# Least common platform

least_common_platform = df['Platform'].value_counts().idxmin() 
print("The least commonly used platform is: " + least_common_platform)

# Top rated Course 

top_rating = df['Rating (out of 5)'].max()  # Get the highest rating
top_rated_course = df[df['Rating (out of 5)'] == top_rating]['Course_Name'].values[0]  # Get the course name with the highest rating
print("The top-rated course is: " + top_rated_course)

# Least rated course

least_rating = df['Rating (out of 5)'].min()  # Get the least rating
least_rated_course = df[df['Rating (out of 5)'] == least_rating]['Course_Name'].values[0]  # Get the course name with the highest rating
print("The least-rated course is: " + least_rated_course)

# Top Five course

top_5_courses = df.sort_values(by='Price ($)', ascending=False).head(5) 
top_5_courses_names = top_5_courses['Course_Name'].values
print("Top 5 highest cost courses are: ")
for course in top_5_courses_names:
    print(course)


# least Five course

least_5_courses = df.sort_values(by='Price ($)', ascending=True).head(5) 
least_5_courses_names = least_5_courses['Course_Name'].values
print("least 5 highest cost courses are: ")
for course in least_5_courses_names:
    print(course)

# Average price for each platform

avg_price_per_platform = df.groupby('Platform')['Price ($)'].mean().reset_index()
plt.figure(figsize=(6,4))  
sns.barplot(x='Platform', y='Price ($)', data=avg_price_per_platform)
plt.title('Average Course Price per Platform', fontsize=16)
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Average Price ($)', fontsize=12)
plt.xticks(rotation=45) 
plt.show()

# Distribution of course prices

plt.figure(figsize=(6,4))
sns.histplot(df['Price ($)'], kde=True, bins=20)
plt.title('Distribution of Course Prices', fontsize=16)
plt.xlabel('Price ($)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.show()

# course Rating Distribution Per platform

plt.figure(figsize=(6,4))
sns.boxplot(x='Platform', y='Rating (out of 5)', data=df)
plt.title('Course Rating Distribution per Platform', fontsize=16)
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Rating (out of 5)', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Correlation between Price , Duration And Rating

plt.figure(figsize=(8,6))
sns.heatmap(df[['Price ($)', 'Duration (hours)', 'Rating (out of 5)']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation between Price, Duration, and Rating', fontsize=10)
plt.show()

# Number of courses per platform

plt.figure(figsize=(6,4))
sns.countplot(x='Platform', data=df)
plt.title('Number of Courses per Platform', fontsize=16)
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Number of Courses', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Top Five Enrolled courses

top_5_enrolled_courses = df.sort_values(by='Enrolled_Students', ascending=False).head(5)
top_5_course_names = top_5_enrolled_courses[['Course_Name', 'Enrolled_Students']]

print("Top 5 courses by enrolled students: ")
print(top_5_course_names)

# Number of courses in each price range

bins = [0, 50, 100, 150, 200, float('inf')]
labels = ['$0-$50', '$50-$100', '$100-$150', '$150-$200', '$200+']
df['Price Range'] = pd.cut(df['Price ($)'], bins=bins, labels=labels)

course_count_by_price_range = df['Price Range'].value_counts()
print("Number of courses in each price range:")
print(course_count_by_price_range)

# Plot the bar chart

plt.figure(figsize=(6,4))
sns.barplot(x=course_count_by_price_range.index, y=course_count_by_price_range.values, palette='viridis')
plt.title('Number of Courses in Each Price Range', fontsize=16)
plt.xlabel('Price Range', fontsize=12)
plt.ylabel('Number of Courses', fontsize=12)
plt.xticks(rotation=45)  
plt.show()

# Average Competition rate for each platform

avg_completion_rate_per_platform = df.groupby('Platform')['Completion_Rate (%)'].mean().reset_index()
print("Average completion rate for each platform:")
print(avg_completion_rate_per_platform)

# Average competition rate by platform

plt.figure(figsize=(8,6))
sns.barplot(x='Platform', y='Completion_Rate (%)', data=avg_completion_rate_per_platform)
plt.title('Average Completion Rate by Platform')
plt.ylabel('Average Completion Rate (%)')
plt.xlabel('Platform')
plt.show()

# Average course duration by platform

avg_duration_per_platform = df.groupby('Platform')['Duration (hours)'].mean().reset_index()
plt.figure(figsize=(6,4))
sns.barplot(x='Platform', y='Duration (hours)', data=avg_duration_per_platform, palette='viridis')
plt.title('Average Course Duration by Platform')
plt.xlabel('Platform')
plt.ylabel('Average Duration (hours)')
plt.xticks(rotation=45)
plt.show()

# Top 5 most expensive courses by platforms

top_expensive_courses_by_platform = df.sort_values(by=['Platform', 'Price ($)'], ascending=[True, False]).drop_duplicates(subset=['Course_Name','Platform']).groupby('Platform').head(5)
print("Top 5 most expensive courses by Platform:")
print(top_expensive_courses_by_platform[['Platform', 'Course_Name', 'Price ($)']])

# Ratings and enrollments correlate with course price

plt.figure(figsize=(10,6))
sns.scatterplot(x='Price ($)', y='Rating (out of 5)', data=df, hue='Enrolled_Students', size='Enrolled_Students', sizes=(20, 200))
plt.title('Price vs Rating (size represents enrollment)')
plt.xlabel('Price ($)')
plt.ylabel('Rating (out of 5)')
plt.show()

#Average Duration

plt.figure(figsize=(6,4))
sns.histplot(x='Duration (hours)', data=df, bins=20, kde=True)
# Calculate and plot the average duration
mean_duration = df['Duration (hours)'].mean()
plt.axvline(mean_duration, color='red', linestyle='--', label=f'Average Duration: {mean_duration:.2f} hours')
plt.title('Distribution of Course Duration')
plt.xlabel('Duration (hours)')
plt.ylabel('Count')
plt.show()

#Course Distribution category wise

df['Category'].value_counts().plot(kind='pie', autopct='%.2f%%', figsize=(6,6), startangle=90, colormap='Set3')
plt.ylabel(None)
plt.title('Course Distribution by Category')
plt.show()

# Completion Rate 

plt.figure(figsize=(4,2))
sns.boxplot(x='Category', y='Completion_Rate (%)', data=df, palette='dark')
plt.title('Completion_Rate (%) by Category')
plt.xlabel('Category')
plt.ylabel('Completion_Rate (%)')
plt.xticks(rotation=45)
plt.show()

# Number of courses BY category

course_count_by_category = df['Category'].value_counts()
plt.figure(figsize=(6,4))
sns.barplot(x=course_count_by_category.index, y=course_count_by_category.values, palette='viridis')
plt.title('Number of Courses by Category', fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Number of Courses', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Number of Courses per Platform // Average Ratings by Platform

platform_counts = df['Platform'].value_counts()
avg_ratings = df.groupby('Platform')['Rating (out of 5)'].mean()
avg_prices = df.groupby('Platform')['Price ($)'].mean()

plt.figure(figsize=(6,4))
sns.barplot(x=platform_counts.index, y=platform_counts.values, palette='viridis')
plt.title('Number of Courses per Platform')
plt.xlabel('Platform')
plt.ylabel('Number of Courses')
plt.xticks(rotation=45)
plt.show()
print('Average Ratings by Platform:')
print(avg_ratings)

print('Average Prices by Platform:')
print(avg_prices)

# Average Enrollments by Category

avg_enrollments = df.groupby('Category')['Enrolled_Students'].mean()
plt.figure(figsize=(6,4))
sns.barplot(x=avg_enrollments.index, y=avg_enrollments.values, palette='viridis')
plt.title('Average Enrollments by Category')
plt.xlabel('Category')
plt.ylabel('Average Enrollments')
plt.xticks(rotation=45)
plt.show()

# duration of courses duration by Category 
plt.figure(figsize=(6,4))
sns.histplot(data=df, x='Duration (hours)', hue='Category', multiple='stack', bins=10)
plt.title('Distribution of Course Duration by Category')
plt.xlabel('Duration (hours)')
plt.ylabel('Count')
plt.show()

# Completion_Rate (%) by Price ($)

bins = [0, 50, 100, 150, 200, float('inf')]
labels = ['$0-$50', '$50-$100', '$100-$150', '$150-$200', '$200+']
df['Price ($) '] = pd.cut(df['Price ($)'], bins=bins, labels=labels)

plt.figure(figsize=(6,4))
sns.boxplot(x='Price ($) ', y='Completion_Rate (%)', data=df, palette='viridis')
plt.title('Completion_Rate (%) by Price ($) ')
plt.xlabel('Price ($) ')
plt.ylabel('Completion_Rate (%)')
plt.xticks(rotation=45)
plt.show()