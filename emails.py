#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 19:41:06 2019

@author: bhupendrabanothe
"""

import  email
import seaborn as sns

import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("/Users/..../Enron_Project/emails.csv")
print(df.shape)
def get_text_from_email(msg):
    parts = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain': 
            parts.append(part.get_payload())
    return ''.join(parts)

def split_email_adds(line):
    if line:
        addrs = line.split(',')
        addrs = frozenset(map(lambda x : x.strip(), addrs))
    else:
        addrs = None
    return addrs
msgs = list(map(email.message_from_string, df['message']))
df.drop('message', axis=1, inplace=True) 

fields = msgs[0].keys()
for field in fields:
    df[field] = [doc[field] for doc in msgs]
    

df['content'] = list(map(get_text_from_email, msgs))

df['From'] = df['From'].map(split_email_adds)
df['To'] = df['To'].map(split_email_adds)


df['user'] = df['file'].map(lambda x:x.split('/')[0])
del msgs

df.head()
print(df.shape)
for col in df.columns:
    print(col, df[col].nunique())
df = df.set_index('Message-ID')
df.drop(['file','Mime-Version','Content-Type', 'Content-Transfer-Encoding'], axis=1)
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True)
df.dtypes
userList = []
userList = df['user'].unique()
count = []
counter = 0 
for l in userList:
    for user in df['user']:
        if user == l:
            counter += 1
    count.append(counter)
    counter = 0
new_list = sorted(list(zip(count, userList)), reverse = True)[:20] 
print(new_list)
num, mailer = zip(*new_list)
mail = range(len(new_list))
plt.bar(mail, num, align = 'center', color ='green', alpha=0.8)
plt.xticks(mail, mailer, rotation='vertical')
plt.show()
newdf = pd.read_csv('/Users/bhupendrabanothe/Development/Enron_Project/part.csv')
print(newdf.shape)
newdf.head()
user = newdf["user"]
year = newdf[" year"]
emails = newdf[" emails"]
listnew = sorted(list(zip(emails, user, year)), reverse = True)[:21] 
dframe = pd.DataFrame(listnew)
dframe.columns = ['emails', 'user', 'year']
dframe.head()



fig, ax = plt.subplots()
fig.set_size_inches(10, 5)
sns.barplot(x='user', y='emails', hue='year', data=dframe, saturation=0.5)
sns.despine()
plt.xticks(rotation=45)
plt.legend(loc='upper right')
fig.savefig('/Users/bhupendrabanothe/Development/Enron_Project/years vs emails.png')
plt.xlabel('Users')
plt.ylabel('Number of emails')