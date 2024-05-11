# 使用SVM训练保存的特征向量，生成分类器
import os
from sklearn import svm
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt  # 导入Matplotlib库
from common import *


# 训练分类器
# 读取原始词频特征向量
data = np.loadtxt(train_data_filename, dtype=float, delimiter=',')

# 提取特征向量和标签
X, y = np.split(data, (16,), axis=1)

# 对特征向量归一化处理
x = MaxMinNormalization(X, np.max(X), np.min(X))

# 分割为训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)

# 训练svm分类器
# clf = svm.SVC(C=0.1, kernel='linear', decision_function_shape='ovr')
clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr', probability=True)
clf.fit(x_train, y_train.ravel())

# 计算svc分类器的准确率
print('Train accuracy:')
print(clf.score(x_train, y_train))  # 精度
y_hat = clf.predict(x_train)
# show_accuracy(y_hat, y_train, '训练集')
print(clf.score(x_test, y_test))
# print(x_test)
y_hat = clf.predict(x_test)
# print('Predict ans:')
# print(y_hat)
# show_accuracy(y_hat, y_test, '测试集')




# 使用分类器预测
# 遍历主题词段落
for w, line in ThemeLineIterator(text_filename):
    # 触发成功
    # 构造特征向量
    feature = [line.count(feature_tag) for feature_tag in feature_tag_list]
    if not any(feature):
        continue
    feature = np.array([[float(x) for x in feature]])

    # 特征向量归一化处理
    feature = MaxMinNormalization(feature, np.max(X), np.min(X))

    # 筛掉预测率低于70%的结果
    proba_list = clf.predict_proba(feature)
    if not (any([x>0.7 for x in proba_list[0]])):
        # pass
        continue 

    # 输出预测信息
    # isTrigger[w] = True
    y_hat = clf.predict(feature)
    predict_event_type = event_type[int(y_hat[0])]

    filename_temp = '%s.txt' % (predict_event_type)
    if not os.path.exists(filename_temp):
        with open(filename_temp, 'w', encoding='utf-8') as ft:
            pass  # 创建空文件
    with open(filename_temp, 'a', encoding='utf-8') as ft:
        ft.write(line)
        ft.write('\n\n')
   
ft.close()