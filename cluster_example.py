import dataimporter
import pandas as pd
import numpy as np
import sklearn.cluster as cls

def load_data():

    [members, rxdata, medicaldata] = dataimporter.import_members_rx_medical_full()    # Import datafiles
    return [members, rxdata, medicaldata]

def prepare_data(members):

    dummy = members

    # Remove variables we don't want for clustering
    dummy = dummy.drop('targetcost', 1)
    dummy = dummy.drop('targetrxcost', 1)
    dummy = dummy.drop('targetmedicalcost', 1)
    dummy = dummy.drop('year_of_birth', 1)
    dummy = dummy.drop('STATE', 1)
    dummy = dummy.drop('prediag_rxcost', 1)
    dummy = dummy.drop('postdiag_rxcost', 1)
    dummy = dummy.drop('prediag_medicalcost', 1)
    dummy = dummy.drop('postdiag_medicalcost', 1)
    dummy = dummy.drop('prediag_dailyrxcost', 1)
    dummy = dummy.drop('postdiag_dailyrxcost', 1)
    dummy = dummy.drop('prediag_dailymedcost', 1)
    dummy = dummy.drop('postdiag_dailymedcost', 1)
    dummy = dummy.drop('dailyrxcost', 1)
    dummy = dummy.drop('dailymedicalcost', 1)
    dummy = dummy.drop('dailytotalcost', 1)
    dummy = dummy.drop('prediag_dailytotalcost', 1)
    dummy = dummy.drop('postdiag_dailytotalcost', 1)
    dummy = dummy.drop('minmedicalday', 1)
    dummy = dummy.drop('maxmedicalday', 1)
    dummy = dummy.drop('minrxday', 1)
    dummy = dummy.drop('maxrxday', 1)

    # Remove these because they have null values coming from the calculation of minrxday, etc.
    dummy = dummy.drop('prediag_days', 1)
    dummy = dummy.drop('postdiag_days', 1)

    # Rescale totalcost by median value to avoid clusters forming based only on differences in totalcost
    median_totalcost = dummy['totalcost'].median()

    dummy['rxcost'] = dummy['rxcost'] / median_totalcost
    dummy['medicalcost'] = dummy['medicalcost'] / median_totalcost
    dummy['prediag_totalcost'] = dummy['prediag_totalcost'] / median_totalcost
    dummy['postdiag_totalcost'] = dummy['postdiag_totalcost'] / median_totalcost
    dummy['totalcost'] = dummy['totalcost'] / median_totalcost

    # Create dummy variables for categorical variables
    dummy = pd.get_dummies(dummy)

    return dummy

def cluster_example(members):
    
    # Initialize KMeans from scikit learn package. In this case we will be doing K-means (default clustering) with 50 clusters
    km = cls.KMeans(n_clusters = 50)

    # Perform clustering. (Not exactly sure what each line is doing, but second puts cluster labels for each member into an array called prediction)
    km.fit(members)
    prediction = km.predict(members)

    # Add cluster labels to new column of members data
    members['predicted_cluster'] = pd.Series(prediction, index=members.index)

    return members

def output_results(members):

    # First, we will print the size of each cluster
    members['cluster_counter'] = 1             # Dummy variable for summing to give size of clusters
    print members.groupby('predicted_cluster')['cluster_counter'].sum()   # Group patients by cluster, and then sum up the "1" in 'cluster_counter' for each patient in the cluster


    # Next, see what the clusters actually look like by checking the mean of all variables within a cluster
    print members.groupby('predicted_cluster').mean()
