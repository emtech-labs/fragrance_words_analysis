from collections import defaultdict, Counter

from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

import numpy as np

class ClustarGenerator:

    # クラスタリング設定
    def train_cluster(self, n_clusters: int, vectors_list: list, batch_size=None):
        if batch_size:
            kmeans_model = MiniBatchKMeans(n_clusters=n_clusters,
                                           init='k-means++',
                                           verbose=1,
                                           random_state=10,
                                           max_iter=3,
                                           batch_size=batch_size)
        else:
            kmeans_model = KMeans(n_clusters=n_clusters,
                                  init='k-means++',
                                  verbose=0,
                                  random_state=10,
                                  max_iter=10)
        # クラスタリング実行
        kmeans_model.fit(vectors_list)

        # クラスタリングデータにラベル付け
        labels = kmeans_model.labels_

        return labels


    def dimensionality_reduction(self, vec_list: list, vec_size):
        pca = TruncatedSVD(n_components=vec_size)
        # モデルのパラメータをfitして取得しPCAオブジェクトへ格納
        # fitで取得したパラメータを参考にXを変換する
        pca_X = pca.fit_transform(vec_list)

        return pca_X

    def make_plot(self, vector_list,cluster_result):
        # 可視化処理
        n_cluster = len(set(cluster_result))
        cmap = plt.get_cmap("tab20")
        plot_dim = self.dimensionality_reduction(vector_list, 2)
        for i in range(n_cluster):
            plt.scatter(plot_dim[cluster_result == i][:, 0],
                        plot_dim[cluster_result == i][:, 1],
                        color=cmap(i), label="cluster {}".format(i))
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

    def generate(self, title_list: list, vector_list, vector_size=100, n_cluster=10):

        if vector_list.shape[1] >= vector_size:
            vector_list = self.dimensionality_reduction(vec_list=vector_list, vec_size=vector_size)
        result = self.train_cluster(n_clusters=n_cluster, vectors_list=vector_list)

        cluster_result = defaultdict(list)
        for doc_id, cluster_id in enumerate(result):
            cluster_result[cluster_id].append(title_list[doc_id])
        self.make_plot(vector_list, result)
        return cluster_result
