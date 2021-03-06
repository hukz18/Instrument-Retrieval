from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import numpy as np
import warnings
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from sklearn import manifold


def pca_plot(X):  # 画PCA的拐点图，差不多选前3个或者前2的变量没啥问题
    PCA_model = PCA(n_components=10)
    PCA_model.fit(X)
    PCA_var = PCA_model.explained_variance_
    plt.plot(np.arange(0, 10), PCA_var)
    plt.show()

# 矩阵X大小=[n_count*n_centers , 40 ]
# n是PCA降维到n=3或者2
# picshow=1说明要画图，=0不画图
def pca_decomposition(X, n, labels, n_count=100, picshow=0):  # 撒豆子警告
    warnings.filterwarnings('ignore')
    sns.set()
    PCA_model = PCA(n_components=n)
    PCA_model.fit(X)
    X_new = PCA_model.fit_transform(X)
    fig = plt.figure(figsize=(15, 10))
    if n == 3 and picshow:
        colors = sns.color_palette("Spectral", len(labels))
        # colors=["#9E0142","#D53E4F","#F46D43","#FDAE61", "#FEE08B","#FFFFBF","#E6F598","#ABDDA4","#66C2A5","#3288BD","#5E4FA2"]
        ax = fig.add_subplot(111, projection='3d')
        for i in range(0, len(labels)):
            x = X_new[i * n_count:(i + 1) * n_count, 0]
            y = X_new[i * n_count:(i + 1) * n_count, 1]
            z = X_new[i * n_count:(i + 1) * n_count, 2]
            ax.scatter(x, y, z, c=colors[i], marker='o', label=labels[i], s=10)
        plt.legend()
        plt.show()

    if n == 2 & picshow:
        colors = sns.color_palette("Spectral", len(labels))
        for i in range(0, len(labels)):
            x = X_new[i * n_count:(i + 1) * n_count, 0]
            y = X_new[i * n_count:(i + 1) * n_count, 1]
            plt.scatter(x, y, c=colors[i], marker='o', label=labels[i], s=10)
        print("plot 2d")
        plt.legend()
        plt.show()

    return X_new


def outcome_print(Y_predict, labels, n_count=100):  # 聚类结果可视化
    count_martix = np.zeros([len(labels), max(Y_predict) + 1], dtype=int)
    for i in range(0, len(labels)):
        label_count = np.bincount(Y_predict[i * n_count:(i + 1) * n_count])
        count_martix[i, 0:len(label_count)] = label_count
        # print(labels[i], "| max class =", np.argmax(label_count), "| count =", label_count[np.argmax(label_count)])
        # print(labels[i],np.argmax(label_count),label_count)
    ax1 = sns.heatmap(count_martix, cmap='rainbow', annot=True,)
    ax1.set_yticklabels(labels)
    return count_martix


def gmm_predict(X, n_centers=11, type="diag"):  # 高斯混合模型
    """
    :param n_centers: 聚类数目
    :param type: 表现最好的方法
    :return:
    """
    gmm = GaussianMixture(n_components=n_centers, covariance_type=type).fit(X)
    Y_predict = GaussianMixture.predict(gmm, X)  # predict_proba
    return Y_predict


def hierarchical_predict(X, n_centers=30, linkage="ward"):  # 层次聚类
    ac = AgglomerativeClustering(n_clusters=n_centers, affinity='euclidean', linkage=linkage)
    # {"ward", "complete", "average", "single"}
    ac.fit(X)
    Y_predict = ac.fit_predict(X)
    return Y_predict


def t_SNE2(X):
    print("Computing t-SNE embedding")
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    X_tsne = tsne.fit_transform(X)
    return X_tsne


def get_tsne():
    """
    获取数据点的tsne聚类
    :return: 聚类后各点的坐标
    TODO:带标签聚类并可视化
    """
    X = np.loadtxt("read_mfcc.txt", dtype=int, delimiter=" ")
    X_tsne = unsuperivesd.t_SNE2(X)
    return X_tsne
