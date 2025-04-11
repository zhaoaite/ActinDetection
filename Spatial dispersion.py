import csv
import math
import numpy as np
import pandas as pd

# dsp_csv = "./finish/Cys224Tyr-3/bilateralFilter100/iso/iso_dsp.csv"
dsp_csv = "./R153C/result/R153C_SNAP(Treatment 2)/Spatial_dispersion.csv"
dsp_list = []
for p in range(1, 43):
    # if p == 18:
    #     continue
    # 读取CSV文件
    # data = pd.read_csv("./finish/Cys224Tyr-3/bilateralFilter100/iso/iso_" + str(p) + "_dis.csv", header=None)  # header是否把第一行读入，如果第一行是标题，可不读入

    if p < 10:
        data = pd.read_csv("./R153C/result/R153C_SNAP(Treatment 2)/dis_angle/0" + str(p) + "_R153C_SNAP_averages.csv", header=None)  # header是否把第一行读入，如果第一行是标题，可不读入
    else:
        data = pd.read_csv("./R153C/result/R153C_SNAP(Treatment 2)/dis_angle/" + str(p) + "_R153C_SNAP_averages.csv", header=None)
    # 提取某一列数据并存储到列表中
    X = data.iloc[:, 0].tolist()
    Y = data.iloc[:, 1].tolist()

    angle = 45
    distance = 100
    spatial_num = 0
    each_spatial_point = []
    # 划分为20个小空间
    for i in range(4):
        for j in range(5):
            temp = 0   # 统计每个小空间点的个数
            spatial_num += 1
            print('当前空间：', spatial_num)
            for k in range(len(X)):
                x = X[k]
                y = Y[k]
                if (x > distance-100 and x <= distance) and (y > angle-45 and y <= angle):
                    temp += 1
            each_spatial_point.append(temp)
            distance += 100  # 横坐标进入下一个小空间
        angle += 45
        distance = 100
    print(each_spatial_point)
    # print(sum(each_spatial_point))

    # 计算各空间落入的点数占总点数的比例作为落入该小空间的概率
    each_prob = []
    for n in range(len(each_spatial_point)):
        temp_prob = each_spatial_point[n] / sum(each_spatial_point)
        each_prob.append(round(temp_prob, 3))
    print("each_prob:", each_prob)
    # print(sum(each_prob))

    # 计算信息熵
    etp = []
    for m in range(len(each_prob)):
        if each_prob[m] == 0:           # 不能计算0的对数
            etp.append(each_prob[m])
        else:
            each_etp = each_prob[m] * math.log(each_prob[m], 2)
            etp.append(-each_etp)
    print('etp:', etp)

    etp_sum = sum(etp)
    print("etp_sum:", etp_sum)

    # 除以一个和维度相关的值
    dsp = etp_sum / (-math.log(1 / sum(each_spatial_point), 2))
    # dsp = etp_sum / (-math.log(1 / 20, 2))
    print('dsp:', round(dsp, 2))
    dsp_list.append(round(dsp, 2))
print('dsp_list:', dsp_list)


# dsp写入csv
with open(dsp_csv, mode='a', newline='') as file1:
    writer = csv.writer(file1)

    # 遍历一维列表，并将每个元素写入CSV文件的指定列的不同行
    for item in dsp_list:
        # 创建一个包含空字符串的列表，用于表示CSV文件的一行
        row = ["" for _ in range(len(dsp_list))]
        # 在指定列中插入要写入的值
        row[0] = item
        writer.writerow(row)