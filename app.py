import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv("online_courses_uses.csv")

# Check columns
st.write("Columns in the dataset:", df.columns)

# Create Recommended
if 'Recommended' not in df.columns:
    df['Recommended'] = (df['Rating (out of 5)'] >= 4.0).astype(int)


st.title("Online Courses Analysis and Recommendation Dashboard")

# Displaying basic information
st.subheader("Dataset Overview")
st.write(df.head())

# Dataset information
st.subheader("Dataset Information")
st.write(df.info())

# Display missing values
st.subheader("Missing Values")
st.write(df.isna().sum())

# Statistical Summary
st.subheader("Statistical Summary")
st.write(df.describe())

# Preprocess the data for modeling
# Encode categorical variables
df['Category'] = LabelEncoder().fit_transform(df['Category'])
df['Platform'] = LabelEncoder().fit_transform(df['Platform'])

# Define features and target variable
X = df[['Price ($)', 'Duration (hours)', 'Rating (out of 5)', 'Category']]
y = df['Recommended']  # This column should now exist

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Function to recommend courses based on user preferences
def recommend_courses(user_preferences):
    user_df = pd.DataFrame(user_preferences)
    predictions = model.predict(user_df)  # Predict for the single instance
    recommended_courses = df[df['Recommended'] == 1]  # Get all courses marked as recommended
    return recommended_courses

# User input for preferences
st.sidebar.header("User Preferences")
price = st.sidebar.slider("Max Price ($)", 0, 500, 100)
duration = st.sidebar.slider("Max Duration (hours)", 0, 100, 10)
rating = st.sidebar.slider("Min Rating (out of 5)", 0.0, 5.0, 4.0)
category = st.sidebar.selectbox("Category", options=df['Category'].unique())

user_preferences = {
    'Price ($)': [price],
    'Duration (hours)': [duration],
    'Rating (out of 5)': [rating],
    'Category': [category]
}

# Initialize a variable to store recommendations
recommended_courses = pd.DataFrame()  # Empty DataFrame

# Button to generate recommendations
if st.sidebar.button("Recommend Courses"):
    recommended_courses = recommend_courses(user_preferences)

# Display recommendations at the top
if not recommended_courses.empty:
    st.subheader("Recommended Courses")
    # Sort recommended courses by Rating (or any other criterion)
    sorted_courses = recommended_courses.sort_values(by='Rating (out of 5)', ascending=False)
    st.write(sorted_courses[['Course_Name', 'Price ($)', 'Rating (out of 5)']])
else:
    st.write("No courses found based on your preferences.")


st.subheader("Average Course Price per Platform")
avg_price_per_platform = df.groupby('Platform')['Price ($)'].mean().reset_index()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x='Platform', y='Price ($)', data=avg_price_per_platform, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

