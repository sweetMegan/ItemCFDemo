# encoding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('u.data', sep='\t', names=['user_id', 'item_id', 'rating', 'titmestamp'])
print ("u.data")
print (df.head())
movie_titles = pd.read_csv('movies.csv')
print ("titiles")
print (movie_titles.head())
df = pd.merge(df, movie_titles, on='item_id')
print ("合并")
print (df.head())
print ("概述")
print (df.describe())
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
print ("按标题对数据集分组,并计算平均分")
print (ratings.head())
ratings['num_of_ratings'] = df.groupby('title')['rating'].count()
print ("按标题对数据集分组,添加评分次数字段")
print (ratings.head())
#绘制图表
# ratings['rating'].hist(bins=50)
# plt.show()
# print ("=====")
# print (ratings.sort_values(by='num_of_ratings', ascending=False).head())
# ratings['num_of_ratings'].hist(bins=3)
# plt.show()
# sns.jointplot(x='rating', y='num_of_ratings', data=ratings)
# plt.show()
#创建userid-movie评分 矩阵
movie_matrix = df.pivot_table(index='user_id', columns='title', values='rating')
print ('创建userid-movie评分 矩阵')
print (movie_matrix.head())
print ('电影名称数据集分组 按评分次数降序排列')
print (ratings.sort_values('num_of_ratings', ascending=False).head())
#给观看过Air Force One (1997)和Contact (1997)的用户推荐电影
#1. 找出所有Air Force One (1997)的评分
#2. 找出所有Contact (1997)的评分
AFO_user_rating = movie_matrix['Air Force One (1997)']
Contact_user_rating = movie_matrix['Arrival, The (1996)']
print ("找出所有Air Force One (1997)的评分")
print (AFO_user_rating.head())
print ("找出所有Contact (1997)的评分")
print (Contact_user_rating.head())
# 3. 计算矩阵中的电影与Air Force One (1997)的相关性
similar_to_air_force_one = movie_matrix.corrwith(AFO_user_rating)
print ("计算矩阵中的电影与Air Force One (1997)的相关性")
print (similar_to_air_force_one.head())
# 4. 计算矩阵中的电影与Contact (1997)的相关性
similar_to_contact = movie_matrix.corrwith(Contact_user_rating)
print ("计算矩阵中的电影与Contact (1997)的相关性")
print (similar_to_contact.head())
# 删除null值
print ('与Air Force One (1997)相关的新电影')
corr_AFO = pd.DataFrame(similar_to_air_force_one, columns=['correlation'])
corr_AFO.dropna(inplace=True)
print (corr_AFO.head())
print ('与Contact (1997)相关的新电影')
corr_contact = pd.DataFrame(similar_to_contact, columns=['correlation'])
corr_contact.dropna(inplace=True)
print (corr_contact.head())
print ("添加阈值，加入num_of_ratings字段")
corr_AFO = corr_AFO.join(ratings['num_of_ratings'])
corr_contact = corr_contact.join(ratings['num_of_ratings'])
print (corr_AFO.head())
print (corr_contact.head())
print ("最终结果")
print ("与Air Force One (1997)相关的电影")
print (corr_AFO[corr_AFO['num_of_ratings']>100].sort_values(by='correlation', ascending=False).head(10))
print ("与Contact (1997)相关的电影")
print (corr_contact[corr_contact['num_of_ratings']>100].sort_values(by='correlation', ascending=False).head(10))
