#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing the needed libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


netflix = pd.read_csv('netflix_titles.csv')
netflix.head() # Exploring the first few rows of the data


# In[ ]:


# Dropping the show_id column
netflix = netflix.drop(columns=('show_id'))
netflix.head(10)


# In[ ]:


netflix.info() # exploring an overview of the data


# In[ ]:


netflix.describe()


# In[ ]:


netflix.isnull().sum() # examining the missing values in the dataset


# In[ ]:


# dropping the few null rows
netflix = netflix.dropna(subset=['date_added', 'rating', 'duration'])


# In[ ]:


# filling the null rows in the director column
netflix['director'] = netflix['director'].fillna('None Specified')


# In[ ]:


netflix['cast'] = netflix['cast'].fillna('Not Listed')


# In[ ]:


netflix['country'] = netflix['country'].fillna('Not Specified')


# In[ ]:


# Ensuring there are no missing values
netflix.isnull().sum()


# In[ ]:


# Converting the duration to an interger
netflix['duration'] = netflix['duration'].str.strip('min')
netflix['duration'] = netflix['duration'].str.strip('Seasons')
netflix['duration'] = netflix['duration'].str.strip('Seaso')


# In[ ]:


netflix['duration'].value_counts()


# In[ ]:


# removing the extra whiite spaces and converting to an integer
netflix['duration'] = netflix['duration'].str.strip(' ').astype('int')


# In[ ]:


netflix['duration'].value_counts()


# In[ ]:


netflix['type'].value_counts() 


# ## Distribution of  Movies and Series

# In[ ]:


plt.pie(netflix['type'].value_counts(), 
        labels=netflix['type'].value_counts().index,
        colors=['skyblue', 'orange'], startangle=90
        
       )
plt.legend();


# In[ ]:


# This pie chart shows that there are a lot more movies produced than tv shows


# ## Movie subset

# In[ ]:


# subset the data to only include movies
netflix_movie = netflix[netflix['type'] == 'Movie']
netflix_movie.head()


# ## Top directors

# In[ ]:


# getting the counts of directors in the dataset
netflix['director'].value_counts()


# In[ ]:


# Split the movie directors to only include 1 name
movie_directors = netflix_movie['director'].str.split(',', expand=True).stack()
# convert to a dataframe
movie_directors = pd.DataFrame(movie_directors)
movie_directors.head() # view the first few rows


# In[ ]:


# name the column
movie_directors.columns = ['Directors']


# In[ ]:


# only selecting the known directors
movie_directors = movie_directors[movie_directors['Directors'] != 'None Specified']

movie_directors = movie_directors.groupby(['Directors']).size().reset_index(name='Total Movies')


# In[ ]:


top_directors = pd.DataFrame(movie_directors.sort_values(by=['Total Movies'], ascending=False)).head(10)
top_directors


# In[ ]:


# Visualising the top movie directors
sns.barplot(y='Directors', x='Total Movies', data=top_directors, color='turquoise')
plt.title('Top movie directors');


# In[ ]:


# This shows that the top movie director is Rajiv Chilaka


# ## Movie durations distribution

# In[ ]:


netflix_movie['duration'].hist(bins=30)
plt.xlabel('Duration in minutes')
plt.ylabel('Count')
plt.title('Distribution showing the most common movie durations');


# In[ ]:


# to show the outliers in the durations column
sns.boxplot(x='duration', data=netflix_movie)
plt.xlabel('Duration in minutes');


# In[ ]:


#These plots show that most movies are between 80 to 100 minutes long


# ## Top movie countries

# In[ ]:


# Expanding the countries to only include one country 
countries = netflix_movie['country'].str.split(',', expand=True).stack()
# removing the white sapces before and after country names to avoid duplicates
countries = countries.str.strip(' ')


# In[ ]:


countries.value_counts()


# In[ ]:


top_countries = countries.value_counts().head(15)


# In[ ]:


top_countries = pd.DataFrame(top_countries)
# renaming the column
top_countries.columns = ['Movies count']
top_countries


# In[ ]:


# A bar plot to show the top movie producing countries
plt.figure(figsize=(17, 10))
sns.barplot(x=top_countries.index, y=top_countries['Movies count'], data=top_countries, color='royalblue')
plt.xlabel('Countries')
plt.title('Top movie producing countries');


# In[ ]:


# This bar chart shows that United States is the largest movie producing country


# ## Top movie actors

# In[ ]:


actors = netflix_movie['cast'].str.split(',', expand=True).stack()
actors = pd.DataFrame(actors)
actors.head()


# In[ ]:


actors.columns = ['cast']


# In[ ]:


actors = actors[actors['cast'] != 'Not Listed']
actors.head()


# In[ ]:


# Selecting the top 15 actors
top_actors = actors.value_counts().head(10)
top_actors


# In[ ]:


top_actors = pd.DataFrame(top_actors)
# renaming the column
top_actors.columns = ['Movies acted']
top_actors


# In[ ]:


# A horizontal bar chart to show the top movie actors
top_actors.plot(kind='barh')
plt.xlabel('Count of movies')
plt.ylabel('Actors')
plt.title('Top actors');


# In[ ]:


# This bar plot shows that the top actor is Anupam Kher


# ## Release year

# In[ ]:


netflix['release_year'].value_counts()


# In[ ]:


# Selecting two columns to perform a bi-variate analysis
netflix_release = netflix[['type','release_year']]
# Selecting the last 10 years
last_10_years = netflix_release[netflix['release_year'] >= 2012]
last_10_years


# In[ ]:


# A bar plot showing the counts of movies and series produced in the last 10 years
#hue can also be depicted as legend
plt.figure(figsize=(15, 8))
sns.countplot(x='release_year', data=last_10_years, hue='type', palette='viridis')
plt.title('Count of releases in the past 10 years');


# In[ ]:


# this bar plot hows that the highest number of movies produced were in the years 2017 and 2018
# It also shows that the highest number of tv shows were produced in 2020


# In[ ]:


# A count plot showing the total movies and Tv shows released
plt.figure(figsize=(14, 8))
sns.countplot(x='release_year', data=last_10_years, palette='viridis')
plt.title('Total Content Released');


# In[ ]:


#This count plot shows that the year 2018 had the most content produced


# ## Directors with the longest movies

# In[ ]:


longest_movies = netflix_movie[['director','duration']]
longest_movies= longest_movies[longest_movies['director'] != 'None Specified']


# In[ ]:


directors_longest = longest_movies[longest_movies['duration'] > 210]


# In[ ]:


directors_longest = directors_longest.set_index(['director'])


# In[ ]:


directors_longest.plot(kind='barh')
plt.xlabel('Duration')
plt.ylabel('Directors')
plt.title('Directors that have produced the longest movies');


# In[ ]:


# This plot shows the directors that have produced the longest movies


# ##  Ratings

# In[ ]:


netflix['rating'].unique()


# In[ ]:


netflix['rating'].value_counts()


# In[ ]:


# creating a dictionary to reorganise the ratings
new_categories = {
    'TV-PG': 'Parental Guidance',
    'TV-MA': 'Mature Audience',
    'TV-Y7-FV': 'Teens',
    'TV-Y7': 'Teens',
    'TV-14': 'Teens',
    'R': 'Mature Audience',
    'TV-Y': 'General Audience',
    'NR': 'Mature Audience',
    'PG-13': 'Teens',
    'TV-G': 'General Audience',
    'PG': 'Teens',
    'G': 'General Audience',
    'UR': 'Mature Audience',
    'NC-17': 'Mature Audience'
}
netflix["rating"] = netflix['rating'].replace(new_categories)
netflix['rating'].value_counts()


# In[ ]:


plt.figure(figsize=(12,8))
sns.countplot(x="rating", data=netflix, palette="viridis")
plt.title("Count of Rating by Movie and Shows");


# In[ ]:


# This shows that most of the content released are for mature audiences


# ## Longest movie ratings

# In[ ]:


ratings = netflix[['rating', 'duration']]
ratings.value_counts()


# In[ ]:


# subsetting to only include the ratings with more than 210 minutes
longest_ratings = ratings[ratings['duration'] > 210]
# setting the index to the rating column
longest_ratings = longest_ratings.set_index(['rating'])
longest_ratings


# In[ ]:


longest_ratings['duration'].plot(kind='bar')
plt.ylabel('Duration')
plt.title('Show ratings duration');


# In[ ]:


# This shows that mature audience rating has the longest movies


# ## Most popular genres

# In[ ]:


# converting the column to a dataframe
#netflix['listed_in']  = pd.DataFrame(netflix['listed_in'])
# Splitting each genre to allow for accurate counting
genres = netflix['listed_in'].str.split(',', expand=True).stack()
# Sorting the values and picking the top 15
popular = genres.value_counts().sort_values(ascending=False).iloc[:15]
popular


# In[ ]:


popular.plot(kind='barh')
plt.xlabel('Total')
plt.title('Most popular genres');
# This shows that the genre international movies is the most popular

