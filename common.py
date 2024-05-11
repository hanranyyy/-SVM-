# 放置公共变量和类
import jieba.posseg as pseg

# 特征向量 描述文本中可能出现的一些特征或关键词
feature_tag_list = [
    '腰部', '发酸', '锻炼', '修炼', '酸痛', '歇息', '打熬',
    '说道', '笑道', '询问', '感到', '高兴', '心中', '忐忑', '心底', '坚定'
]

# 主题
theme = ['林雷']

event_type = {
    1: '修炼',
    2: '对话',
    3: '心理活动'
}

text_filename = '《盘龙》.txt'
train_data_filename = 'feature.txt'

# 输入值进行最大最小归一化处理，将其映射到0到1之间的范围内
def MaxMinNormalization(x, Max, Min):  
    return (x - Min) / (Max - Min)

# 迭代处理文件中的文本行
class ThemeLineIterator:
    def __init__(self, filename, flags=None):
        self.fp = open(filename, 'r', encoding='utf-8')
        self.flags = flags
        self.word = 'None'

    def __iter__(self):
        return self

# 读取文件的下一行，并根据条件判断是否应该返回该行
    def __next__(self):
        while True:
            line = next(self.fp)
            # 如果 flags 为空或未提供，则直接返回当前行（去除了首尾空白字符）
            if self.flags is None or len(self.flags) == 0:
                return self.word, line.strip()
            # 如果 flags 不为空，则使用 pseg.cut() 函数对当前行进行分词，并提取每个词的词性标记。
            # 然后，它检查每个词的前两个和后一个词的词性标记，如果满足某些条件，则返回当前行。
            else:
                words = pseg.cut(line)
                flags = [w.flag for w in words]
                for i, w in enumerate(words):
                    if i < len(flags) and (i + 1 < len(flags) and 'v' not in flags[i + 1]) and \
                            (i - 1 >= 0 and 'v' not in flags[i - 1]) and \
                            (i - 2 >= 0 and 'v' not in flags[i - 2]):
                        return self.word, line.strip()

    def close(self):
        self.fp.close()

