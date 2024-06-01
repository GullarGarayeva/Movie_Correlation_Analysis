#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing Libreries

import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure

get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['figure.figsize'] = (12,8)


# In[8]:


#Reading the Data

df = pd.read_csv(r'C:\Users\Gullar\Downloads\movies.csv')


# In[10]:


#Looking the Data
df.head(10)


# In[11]:


#First Summary Info about the data 

print(df.info())


# In[12]:


#Identifying Missing Data

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))


# In[14]:


# Solving Missing Data Problems 
df=df.dropna()


# In[15]:


#Checking Duplicate datas
num_duplicates = df.duplicated().sum()
print(f"\nNumber of duplicate rows: {num_duplicates}")


# In[16]:


# Checking Data Types for our columns

print(df.dtypes)


# In[17]:


#Changing Data types

df['budget']=df['budget'].astype('int64')
df['gross']=df['gross'].astype('int64')
df['votes']=df['votes'].astype('int64')


# In[44]:


# Extracting the year from the "released date" column
df['correct-year'] = df['released'].str.extract(pat = '([0-9]{4})').astype(int)


# In[45]:


df.head()


# In[46]:


#Small correction
df.drop(columns=['correct_year'], inplace=True)


# In[47]:


#Sorting the data
df=df.sort_values(by=['gross'], inplace=False, ascending=False)


# In[48]:


# Scatter plot with budget vs gross

plt.scatter(x=df['budget'], y=df['gross'])
plt.title('Budget vs Gross Earnings')
plt.xlabel('Gross Earnings')
plt.ylabel('Film Budget')
plt.show()


# In[49]:


df.head()


# In[66]:


#Data is clealy formatted and Cleaned
#It is time to identify Correlations
#Correlation between budget and gross

sns.regplot(x='budget', y='gross', data=df, scatter_kws={"color": "red"}, line_kws={"color": "blue"})


# In[51]:


# Time to identify Correlation

df.corr()


# # High Correllation between budget and gross

# In[53]:


correlation_matrix = df.corr(method='pearson')

sns.heatmap(correlation_matrix, annot = True)

plt.title("Correlation matrix for Numeric Features")

plt.xlabel("Movie features")

plt.ylabel("Movie features")

plt.show()


# In[55]:


#Correlation between votes and gross revenue

sns.regplot(x='votes',y='gross',data=df,scatter_kws={'color': 'orange'},line_kws={'color' : 'blue'})
plt.title('Correlation between votes and gross revenue')
plt.xlabel('Votes')
plt.ylabel('Gross revenue')


# In[65]:


#Correlation between IMDb scores and gross revenue

sns.regplot(x='score',y='gross',data=df,scatter_kws={'color': 'purple'},line_kws={'color' : 'blue'})
plt.title('Correlation between IMDb scores and gross revenue')
plt.xlabel('IMDb score')
plt.ylabel('Gross revenue')


# In[91]:


correlation_mat = df.apply(lambda x: x.factorize()[0]).corr()

corr_pairs = correlation_mat.unstack()

print(corr_pairs)


# In[92]:


sorted_pairs = corr_pairs.sort_values(kind="quicksort")

print(sorted_pairs)


# In[93]:


# Sorting the ones that have a high correlation (> 0.5)

strong_pairs = sorted_pairs[abs(sorted_pairs) > 0.5]

print(strong_pairs)


# # Result!!
# 
# #Votes and Budget have highest correlation
# 
# #Company has the lowest correlation 

# In[95]:


# Top ten companies with higest gross revenue 

gross_by_comp = df.groupby('company')[['gross']].sum()
top_10_companies= rev_by_comp.sort_values('gross', ascending = False)[:10]
top_10_companies


# In[96]:


#Top 10 Companies by Gross

comp_df = pd.DataFrame({'gross': top_10_companies['gross']}).reset_index()
plt.figure(figsize=(12, 6))
plt.bar(comp_df['company'], comp_df['gross'], color='skyblue')
plt.xticks(rotation=45, ha='right', fontsize=8) 
plt.xlabel('Company Names')
plt.ylabel('Gross revenue (Billions)')
plt.title('Top 10 Companies by Gross ')


# In[97]:


df.groupby(['company', 'year'])[["gross"]].sum()


# In[98]:


CompanyGrossSum = df.groupby(['company', 'year'])[["gross"]].sum()

CompanyGrossSumSorted = CompanyGrossSum.sort_values(['gross','company','year'], ascending = False)[:15]

CompanyGrossSumSorted = CompanyGrossSumSorted['gross'].astype('int64') 

CompanyGrossSumSorted


# In[99]:


#Budget vs Gross Earnings

plt.scatter(x=df['budget'], y=df['gross'], alpha=0.5)
plt.title('Budget vs Gross Earnings')
plt.xlabel('Gross Earnings')
plt.ylabel('Budget for Film')
plt.show()


# In[105]:


#Gross revenue over the years

rev_by_year = df.groupby('correct-year')[['gross']].sum()
year_rev = rev_by_year.sort_values('correct-year', ascending = True)
year_rev.head(10)


# In[114]:


#Movie Revenue Trend Over Years

year_df = pd.DataFrame({'gross': year_rev['gross']}).reset_index()
year_df = year_df[year_df['correct-year'] != 2020]
plt.figure(figsize=(10, 6))

#!!!the data for 2020 only covers up to September. So I drop it from this data frame.

# Plot the line chart over years
plt.plot(year_df['correct-year'], year_df['gross'] / 1e9, marker='o', color='blue', linestyle='-')
plt.xlabel('Year')
plt.ylabel('Total Movie Revenue (Billions)')
plt.title('Movie Revenue Trend Over Years')

plt.tight_layout()
plt.show()


# In[ ]:




