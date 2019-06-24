import pandas as pd
import numpy as np
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

def find_metric_groups(data_set_path='',group_corr_thresh=0.5,save=True):

    # Load data
    score_save_path = data_set_path.replace('.csv', '_scores.csv')
    churn_data = pd.read_csv(score_save_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    churn_data.drop('is_churn',axis=1,inplace=True)
    metric_columns = list(churn_data.columns.values)

    # Find the clusters
    corr = churn_data.corr()
    dissimilarity = 1.0 - corr
    hierarchy = linkage(squareform(dissimilarity), method='single')
    thresh = 1.0 - group_corr_thresh
    labels = fcluster(hierarchy, thresh, criterion='distance')
    clusters = set(labels) # The unique list of the group labels

    # Relabel the clusters so the cluster with the most columns is first
    cluster_count = Counter(labels)
    cluster_order = {cluster[0]: idx for idx, cluster in enumerate(cluster_count.most_common())}
    relabeled_clusters = [cluster_order[l] for l in labels]
    relabeled_count = Counter(relabeled_clusters)

    labeled_columns = pd.DataFrame({'group': relabeled_clusters, 'column': metric_columns}).sort_values(
        ['group', 'column'], ascending=[True, True])

    load_mat = np.zeros((len(metric_columns), len(clusters)))
    for row in labeled_columns.iterrows():
        orig_col = metric_columns.index(row[1][1])
        load_mat[orig_col, row[1][0]] = 1.0 / np.sqrt(relabeled_count[row[1][0]])

    loadmat_df = pd.DataFrame(load_mat, index=metric_columns, columns=[d for d in range(0, load_mat.shape[1])])
    loadmat_df['name'] = loadmat_df.index
    sort_cols = list(loadmat_df.columns.values)
    sort_order = [False] * loadmat_df.shape[1]
    sort_order[-1] = True
    loadmat_df = loadmat_df.sort_values(sort_cols, ascending=sort_order)

    if save:
        print('saving loadings')
        loadmat_df = loadmat_df.drop('name', axis=1)
        loadmat_df.to_csv(data_set_path.replace('.csv', '_load_mat.csv'))

    return loadmat_df
