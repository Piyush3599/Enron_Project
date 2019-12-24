#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 01:16:27 2019

@author: bhupendrabanothe
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

with open('/Users/..../word_data_unix.pkl', 'rb') as f:
    sal_data = pickle.load(f)
sal_data = pd.DataFrame.from_dict(sal_data, orient='index', dtype=None)
sal_data.head()
sal_data.replace(to_replace='NaN', value=np.nan, inplace=True)
data1 = sal_data.apply(lambda x: pd.to_numeric(x, errors='ignore')).fillna(0)
data1.head()
data1.shape
len(sal_data[sal_data['poi']==1]['poi'])
print ("Kenneth Lay -> ", sal_data['total_payments']['LAY KENNETH L'])
print ("Jeffrey Skilling -> ", sal_data['total_payments']['SKILLING JEFFREY K'])
print ("Andrew Fastow -> ", sal_data['total_payments']['FASTOW ANDREW S'])
data1['total_payments']
data1.sort_values("salary", ascending = False) 
data1.head()
fig, ax = plt.subplots(1,1, figsize=(8,8))
plt = plt.scatter(x='salary', y='bonus', data=data1)
ax.set_title("Salary VS. Bonus BEFORE REMOVING 'TOTAL' OUTLIER")
ax.set_xlabel("Salary")
ax.set_ylabel("Bonus")
sal_data=data1.drop('TOTAL')
fig, ax = plt.subplots(1,1, figsize=(8, 8))
plt = plt.scatter(x='salary', y='bonus', data=sal_data, color='c')
ax.set_title("Salary VS. Bonus after Removing 'TOTAL' Outlier")
ax.set_xlabel("Salary")
ax.set_ylabel("Bonus")
print ("THE EMPLOYEES WITH SALARY OVER 1 MILLION DOLLARS:")
for i in range(len(sal_data['salary'])):
    if sal_data['salary'][i] >= 1000000:
        print (sal_data.index.values[i], " | ", sal_data['salary'][i])
print ("THE EMPLOYEES WITH BONUSES OVER 5 MILLION DOLLARS:")
for i in range(len(sal_data['bonus'])):
    if sal_data['bonus'][i] >= 5000000:
        print (sal_data.index.values[i], " | ", sal_data['bonus'][i])
def HowManyPOI(df, col_name):
    not_zero = 0
    num_poi = 0
    for i in range(len(df[col_name])):
        if df[col_name][i] != 0.0: 
            not_zero += 1
        if df[col_name][i] != 0.0 and df['poi'][i] == True:
            num_poi += 1
    print (col_name, " ->", num_poi, "POI out of", not_zero , "in total (non-zero)")

for col_name in list(sal_data.columns.values):
    if col_name == "email_address":
        continue
    HowManyPOI(sal_data, col_name)
sal_data_2 = sal_data.drop(['restricted_stock_deferred','director_fees','loan_advances'], axis=1)
sal_data_2 = sal_data_2.drop(['LOCKHART EUGENE E'])
fig, ax = plt.subplots(1,1, figsize=(8, 8))
plt = plt.scatter(x='from_poi_to_this_person', y='from_this_person_to_poi', data=sal_data_2, color='g')
ax.set_title("From POI VS. to POI E-mail Counts")
ax.set_xlabel("From POI")
ax.set_ylabel("To POI")
fig.savefig("/Users/bhupendrabanothe/Development/Enron_Project/from_poi_to_poi_emails.png")
print ("More than 300 E-mails from POI to These People:")
for i in range(len(sal_data_2['from_poi_to_this_person'])):
    if sal_data['from_poi_to_this_person'][i] >= 300:
        print( sal_data.index.values[i], " | ", sal_data_2['from_poi_to_this_person'][i])
print ("More than 300 E-mails from Others to POI:")
for i in range(len(sal_data_2['from_this_person_to_poi'])):
    if sal_data['from_this_person_to_poi'][i] >= 300:
        print (sal_data.index.values[i], " | ", sal_data_2['from_this_person_to_poi'][i])
fig, ax = plt.subplots(1,1, figsize=(8, 8))
plt = plt.scatter(x='salary', y='deferral_payments', data=sal_data_2, color='g')
ax.set_title("Salary VS. Deferral Payments")
ax.set_xlabel("Salary")
ax.set_ylabel("Deferral Payments")
fig.savefig("/Users/bhupendrabanothe/Enron_Project/salary_deferral_pay.png")
print ("More than 5 Million in Deferral Payments:")
for i in range(len(sal_data_2['deferral_payments'])):
    if sal_data_2['deferral_payments'][i] >= 6000000:
        print (sal_data_2.index.values[i], " | ", sal_data_2['deferral_payments'][i])
sal_data_2['fraction_from_poi'] = ""
sal_data_2['fraction_to_poi'] = ""


for i in range(len(sal_data_2['to_messages'])):
    if sal_data_2['to_messages'][i] != 0.0:
        v = float(sal_data_2['from_poi_to_this_person'][i]) / float(sal_data_2['to_messages'][i])
        sal_data_2.set_value(sal_data_2.index[i], 'fraction_from_poi', v)
        
    if sal_data_2['to_messages'][i] == 0.0 and sal_data_2['from_poi_to_this_person'][i] == 0.0:
        sal_data_2.set_value(sal_data_2.index[i], 'fraction_from_poi', 0.0)

    if sal_data_2['from_messages'][i] != 0.0:
        v = float(sal_data_2['from_this_person_to_poi'][i]) / float(sal_data_2['from_messages'][i])
        sal_data_2.set_value(sal_data_2.index[i], 'fraction_to_poi', v)
        
    if sal_data_2['from_messages'][i] == 0.0 and sal_data_2['from_this_person_to_poi'][i] == 0.0:
        sal_data_2.set_value(sal_data_2.index[i], 'fraction_to_poi', 0.0)
fig, ax = plt.subplots(1,1, figsize=(8, 8))
plt = plt.scatter(x='fraction_from_poi', y='fraction_to_poi', data=sal_data_2, color='g')
ax.set_title("Fraction of E-mails to/from POI")
ax.set_xlabel("From POI")
ax.set_ylabel("To POI")
fig.savefig("/Users/bhupendrabanothe/Development/Enron_Project/emails_to_from_poi.png")
print ("More than 0.15 of Emails are from POI to This Person:")
for i in range(len(sal_data_2['fraction_from_poi'])):
    if sal_data_2['fraction_from_poi'][i] >= 0.15:
        print (sal_data_2.index.values[i], " | ", sal_data_2['fraction_from_poi'][i])
print ("More than 0.8 of Emails are from This Person to POI:")
for i in range(len(sal_data_2['fraction_to_poi'])):
    if sal_data_2['fraction_to_poi'][i] >= 0.8:
        print (sal_data_2.index.values[i], " | ", sal_data_2['fraction_to_poi'][i])

