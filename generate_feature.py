import os
import jieba.analyse
from common import *

# 自定义字典
jieba.add_word('林雷', 15, 'n')

# 若特征数据集文件不存在，那么创建一个
if not os.path.exists(train_data_filename):
    with open(train_data_filename, 'w'):
        pass

# 遍历主题词段落
for w, line in ThemeLineIterator(text_filename):
    # 触发成功
    # 构造特征向量
    feature = [line.count(feature_tag) for feature_tag in feature_tag_list]
    if not any(feature[:-1]):
        continue

    # 输出这句话
    print(line)

    # 输出关键词
    print('Top 10 key:')
    tags = jieba.analyse.extract_tags(line, topK=10)
    print(','.join(tags))

    print('Feature:')
    print(feature)

    # 构造特征数据集
    # 构造特征向量，存入本地
    label = input("请输入事件类别编号（1-%d），或者留空跳过：" % len(event_type))
    if label.strip() != '' and label.strip().isdigit() and int(label) in range(1, len(event_type) + 1):
        # 是预定事件类别
        label = int(label)
        feature.append(label)
        print('Feature && label:')
        print(feature)
        print('')
        with open(train_data_filename, 'a') as ft:
            ft.write('%s\n' % ','.join(map(str, feature)))
    else:
        print('跳过此条数据')

