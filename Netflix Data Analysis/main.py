import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('mymoviedb.csv', lineterminator='\n')

print(df.head())
print(df.info())
print(df['Genre'].head())

print(df.duplicated().sum())

print(df.describe())

# we have a dataframe consisting of 9827 rows and 9 columns
#our dataset looks bit tidy with no Nans nor duplicated values
# Release date column need to be casted into date time and to extract only the year value
# overview , original_language and poster-url wouldn't be so useful during analysis, so we drop them
# there is noticable outliers in popularity column
# vote_avg better be categorized for proper analysis
# genre column has comma saperated values and white spaces that need to handle and casted into category.Exploration Summary

df['Release_Date'] = pd.to_datetime(df['Release_Date'])

print(df['Release_Date'])

df['Release_Date'] = df['Release_Date'].dt.year
print(df['Release_Date']) 

print(df.head())

# dropping the columns

clos = ['Overview','Original_Language','Poster_Url']

df.drop(clos, axis = 1, inplace=True)
print(df.columns)
print(df.head())

# below here we create user define function for give labels to a specific columns

def categorize_col(df, col, labels):
    edges = [df[col].describe()['min'],
             df[col].describe()['25%'],
             df[col].describe()['50%'],
             df[col].describe()['75%'],
             df[col].describe()['max']]
    df[col] = pd.cut(df[col], edges, labels= labels, duplicates='drop')
    return df

labels = ['not_popular','below_avg','average','popular']

categorize_col(df, 'Vote_Average', labels)

df['Vote_Average'].unique()

print(df.head())

print(df['Vote_Average'].value_counts())

df.dropna(inplace=True)
print(df.isna().sum())

# for removing white space from genre and also separate each word in new line

df['Genre'] = df['Genre'].str.split(', ')

df = df.explode('Genre').reset_index(drop = True)

print(df.head())

# casting column into category

df['Genre'] = df['Genre'].astype('category')
print(df['Genre'].dtypes)

# DATA VISUALIZATION

sns.set_style('whitegrid')

# question: what is the most frequent genre of movies released on netflix?

print(df['Genre'].describe())

# for visualise

sns.catplot(y = 'Genre', data = df , kind = 'count',
            order = df['Genre'].value_counts().index,
            color = '#4287f5')
plt.title("Genre column distribution")
plt.show()

# question: which has highest votes in vote avg column?

sns.catplot(y= 'Vote_Average', data= df, kind='count',
             order= df['Vote_Average'].value_counts().index,
             color='#808080')
plt.title("Vote Average Column")
plt.show()

# question: which movie got highest popularity? what's its genre?

print(df[df['Popularity'] == df['Popularity'].max()])

# question: which movie got lowest popularity? what's its genre?

print(df[df['Popularity'] == df['Popularity'].min()])

# question: which year has the most filmed movies?

df['Release_Date'].hist()
plt.title("Release Date column distribution")
plt.show()
