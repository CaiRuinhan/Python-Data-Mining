# -*- coding: utf-8 -*-

"""
功能：实现聚类离散化，最后的result的格式为：
      1           2           3           4
A     0    0.178698    0.257724    0.351843
An  240  356.000000  281.000000   53.000000
即(0, 0.178698]有240个，(0.178698, 0.257724]有356个，依此类推。
"""


from __future__ import print_function
import pandas as pd
from sklearn.cluster import KMeans  # 导入K均值聚类算法


def cluster_data(datafile, processedfile, typelabel):
    # 读取数据并进行聚类分析
    data = pd.read_excel(datafile)  # 读取数据
    keys = list(typelabel.keys())
    result = pd.DataFrame()

    for i in range(len(keys)):
        # 调用k-means算法，进行聚类离散化
        print(u'正在进行“%s”的聚类...' % keys[i])
        k = 4  # 需要进行的聚类类别数
        kmodel = KMeans(n_clusters=k, n_jobs=4)  # n_jobs是并行数，一般等于CPU数较好
        kmodel.fit(data[[keys[i]]].values)  # 训练模型

        r1 = pd.DataFrame(kmodel.cluster_centers_, columns=[typelabel[keys[i]]])  # 聚类中心
        r2 = pd.Series(kmodel.labels_).value_counts()  # 分类统计

        r2 = pd.DataFrame(r2, columns=[typelabel[keys[i]] + 'n'])  # 转为DataFrame，记录各个类别的数目
        r = pd.concat([r1, r2], axis=1).sort_values(typelabel[keys[i]])  # 匹配聚类中心和类别数目
        r.index = [1, 2, 3, 4]

        r[typelabel[keys[i]]] = r[typelabel[keys[i]]].rolling(2).mean()  # rolling_mean()用来计算相邻2列的均值，以此作为边界点。
        r[typelabel[keys[i]]][1] = 0.0  # 0为范围的起点。
        result = result.append(r.T)

    result.to_excel(processedfile)


if __name__ == '__main__':
    datafile = '../data/data.xls'  # 待聚类的数据文件
    processedfile = '../tmp/data_processed.xls'  # 数据处理后文件
    typelabel = {u'肝气郁结证型系数': 'A',
                 u'热毒蕴结证型系数': 'B',
                 u'冲任失调证型系数': 'C',
                 u'气血两虚证型系数': 'D',
                 u'脾胃虚弱证型系数': 'E',
                 u'肝肾阴虚证型系数': 'F'}
    cluster_data(datafile, processedfile, typelabel)

