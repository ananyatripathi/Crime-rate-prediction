import random 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans 
from sklearn.datasets import make_blobs 
from sklearn.preprocessing import StandardScaler
import csv

import pandas as pd
cust_df = pd.read_csv("kmean_total.csv")

X = cust_df.values[:,1:] #column 1 contains numbers therefore we are ignoring it
# print(X)
X = np.nan_to_num(X) #NumPy NAN stands for not a number and is defined as a substitute for declaring value which are numerical values that are missing values in an array
Clus_dataSet = StandardScaler().fit_transform(X)
# print(Clus_dataSet)
clusterNum = 4
k_means = KMeans(init = "k-means++", n_clusters = clusterNum, n_init = 12)
k_means.fit(X)
labels = k_means.labels_
print(labels)

rate = []
rate_name = ['medium','high',"low","very high"]

def crime_rate():
    with open('kmean_total.csv', 'r') as csvfile:
      dis = [1,3,4,6]
      csvreader = csv.reader(csvfile)
      
      f = [row for idx, row in enumerate(csvreader) if idx in (dis[0],dis[1],dis[2],dis[3])]
      print(f)
      for d in f:  
        j = k_means.predict([[d[1]]])
        rate.append(int(str(j)[1:-1]))
    return rate

print(crime_rate())