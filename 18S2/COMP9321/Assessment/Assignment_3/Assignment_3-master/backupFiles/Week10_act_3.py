'''
Description: Using AgglomerativeClustering split the diet dataset into 3 clusters based on the diet types
Steps:
1,Load the diet dataset
2,Drop the 'Diet' column; this is required because clustering is an unsupervised method
3, Use AgglomerativeClustering to cluster the data into 3 clusters; because we know that there are 3 different types of diet in this dataset
4, Plot the clusters based on whtat you have learnt in Visualisation Lab, Plot a scatter chart using x='pre.weight', y='weight6weeks' for each cluster
5, Label each data point with the true label of diet
6, Change the Clustering algorithm to KMeans; which one is better for this problem ?
'''

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.utils import shuffle

def load_iris(iris_path):
    df = pd.read_csv(iris_path)

    df = shuffle(df)
    df_without_label = df.drop('Diet', axis=1)
    return df, df_without_label

if __name__ == '__main__':
    csv_file = 'diet.csv'

    # Split the data into test and train parts
    df, df_without_label = load_iris(csv_file)
    # Fit a k-means estimator
    estimator = AgglomerativeClustering(n_clusters=3)
    estimator.fit(df_without_label)
    # estimator = KMeans(n_clusters=3)
    # estimator.fit(df_without_label)
    # Clusters are given in the labels_attribute
    labels = estimator.labels_
    df['cluster'] = pd.Series(labels, index=df.index)

    print(labels)
    # divide the dataset into three datafrmes based on the species
    cluster_0_df = df.query('cluster == 0')
    cluster_1_df = df.query('cluster == 1')
    cluster_2_df = df.query('cluster == 2')

    fig,axes = plt.subplots(nrows=1,ncols=1)
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout()

    ax = cluster_0_df.plot.scatter(x='pre.weight', y='weight6weeks', label='Cluster-0', color='blue', ax=axes)
    ax = cluster_1_df.plot.scatter(x='pre.weight', y='weight6weeks', label='Cluster-1', color='red', ax=ax)
    ax = cluster_2_df.plot.scatter(x='pre.weight', y='weight6weeks', label='Cluster-2', color='green', ax=ax)

    for i, label in enumerate(df['Diet']):

        label = 'Diet_' + str(label)
        ax.annotate(label, (list(df['pre.weight'])[i], list(df['weight6weeks'])[i]), color='gray', fontSize=9,horizontalalignment='left', verticalalignment='bottom')
    plt.title('Activity_3 using KMeans',fontsize='large',color = 'green')
    plt.show()
