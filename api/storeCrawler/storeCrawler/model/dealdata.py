import json
import csv
import numpy as npy
import pandas as pda
import matplotlib.pyplot as plt
# 调用python关于机器学习sklearn库中的KMeans
from sklearn.cluster import KMeans

# 读取.json文件
dic = []
f = open("../Data/package.txt", 'r',
         encoding='utf-8')  # 这里为.json文件路径
for line in f.readlines():
    dic.append(json.loads(line))
# 对爬取到的数据作处理，将价格和评论数由字符串处理为数字
tmp = ''
name, price, comnum, link = [], [], [], []
for i in range(0, 860):
    dic[i]['price'] = tmp + dic[i]['price'][1:]
    dic[i]['comnum'] = dic[i]['comnum'][:-3] + tmp
    price.append(float(dic[i]['price']))
    comnum.append(int(dic[i]['comnum']))
    name.append(dic[i]['name'])
    link.append(dic[i]['link'])
data = npy.array([name, price, comnum, link]).T
# print(data)

# 要存储.csv文件的路径
csvFile = open('C:/Users/DELL/PycharmProjects/pythonProject1/api/storeCrawler/storeCrawler/Data/bookdata.csv',
               'w')
writer = csv.writer(csvFile)
writer.writerow(['name', 'price', 'comment_num', 'link'])
for i in range(0, 860):
    writer.writerow(data[i])
csvFile.close()

# 将数据缺失值处理None---->0
# 读取.csv文件数据
data = pda.read_csv(
    "C:/Users/DELL/PycharmProjects/pythonProject1/api/storeCrawler/storeCrawler/Data/bookdata.csv",
    encoding="gbk")
# 发现缺失值，将评论数为0的值转为None
# data_deal = data.copy()
# print(type(data_deal))
# print(data_deal)
# data_deal.loc[:, data_deal.loc[:,"comment_num"] == 0] = None
# data["comment_num"][(data["comment_num"] == 0)] = None
# 均值填充处理
data.fillna(value=data["comment_num"].mean(), inplace=True)
# 删除处理,data1为缺失值处理后的数据
data_dealed = data.dropna(axis=0, subset=["comment_num"])

# 画散点图（横轴：价格，纵轴：评论数）
# 设置图框大小
fig = plt.figure(figsize=(10, 6))
plt.plot(data['price'], data['comment_num'], "o")
# 展示x，y轴标签
plt.xlabel('price')
plt.ylabel('comment_num')
plt.show()

"""
可以看到有部分数据评论数过高，
或许为热销商品或者存在刷评论，还有一部分数据价格过高，
甚至高达700，而一般书籍价格不会高过￥150。
对于这些异常值我们在作数据分析时一般不会考虑，删除或者改动这些异常值即可。
再看看数据的箱型图观察分布情况：
"""
fig = plt.figure(figsize=(10, 6))
# 初始化两个子图，分布为一行两列
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
# 绘制箱型图
ax1.boxplot(data['price'].values)
ax1.set_xlabel('price')
ax2.boxplot(data['comment_num'].values)
ax2.set_xlabel('comment_num')
# 设置x，y轴取值范围
ax1.set_ylim(0, 150)
ax2.set_ylim(0, 1000)
plt.show()

"""
价格的箱型图中黄线表示中位数，大概为￥50，
箱型图上下分别为上四分位和下四分位，分别为￥40到￥70，
上下界分别为￥110和￥0，最上方的圆点都是离群点。
可以看到评论数中位数分布点较低。
离群点的数值明显偏离其余观测值，会对分析结果产生不良影响，
所以我们将价格￥120以上，评论数700以上的离群点删除，不作考虑.
"""
# 删除价格￥120以上，评论数700以上的数据
data2 = data[data['price'] < 120]
data3 = data2[data2['comment_num'] < 700]
# data3为异常值处理后的数据
fig = plt.figure(figsize=(10, 6))
plt.plot(data3['price'], data3['comment_num'], "o")
plt.xlabel('price')
plt.ylabel('comment_num')
plt.show()

"""
对数据做可视化分析了，
可以对价格及评论数做直方图，
分析数据分布情况。
"""
# print(data3.loc[:,"comment_num"])
# #求最值
pricemax = max(data3.loc[:, "comment_num"])
# print(pricemax)
pricemin = min(data3.loc[:, "comment_num"])
commentmax = max(data3.loc[:, "price"])
commentmin = min(data3.loc[:, "price"])
##计算极差
pricerg = pricemax - pricemin
commentrg = commentmax - commentmin
# 组距=极差/组数
pricedst = pricerg / 13
commentdst = commentrg / 13
fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
# 绘制价格直方图
# numpy.arrange(最小,最大,组距)
pricesty = npy.arange(pricemin, pricemax, pricedst)
ax1.hist(data3.loc[:, "comment_num"], pricesty, rwidth=0.8)
ax1.set_title('price')
# 绘制评论数直方图
commentsty = npy.arange(commentmin, commentmax, commentdst)
ax2.hist(data3.loc[:, "price"], commentsty, rwidth=0.8)
ax2.set_title('comment_num')
plt.show()
"""
从直方图中可以观察到：
1、书的价格大致呈正态分布，￥40左右的书籍比较多，说明python书籍基本定价在￥40左右
2、评论数在50条以下的书籍商品最多（200多本），随着评论数递增，商品数量逐渐减少，
说明大部分商品销量一般
"""

"""
最后对数据作聚类分析，这里采用了机器学习算法——K-Means聚类算法，K-Means聚类算法是机器学习中的一个无监督学习算法，简单，快速，适合常规数据集，具体的算法执行步骤如下：
1、初始化聚类中心
2、计算样本点到各个聚类中心的距离，选择距离小的，进行聚类
3、计算新的聚类中心，改变新的聚类中心
4、重复2-3步，直到聚类中心不发生改变
通过调用Python的机器学习库sklearn，可利用此算法实现对商品的分类
"""
# 转换数据格式
tmp = npy.array([data3['price'], data3['comment_num']]).T
# 设置分为3类，并训练数据
kms = KMeans(n_clusters=3)
y = kms.fit_predict(tmp)
# 将分类结果以散点图形式展示
fig = plt.figure(figsize=(10, 6))
plt.xlabel('price')
plt.ylabel('comment_num')
for i in range(0, len(y)):
    if y[i] == 0:
        plt.plot(tmp[i, 0], tmp[i, 1], "*r")
    elif y[i] == 1:
        plt.plot(tmp[i, 0], tmp[i, 1], "sy")
    elif y[i] == 2:
        plt.plot(tmp[i, 0], tmp[i, 1], "pb")
plt.show()
"""
从聚类结果中可以看到，K-Means聚类算法将评论数100以下的分为了一类，评论数大致从100到350的分为一类，
评论数大致在350以上的分为了一类，基本按照书籍是否畅销分成了三类，
从图中可明显看出聚类效果
"""
