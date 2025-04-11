import math

import cv2
import imutils
import numpy as np
import csv

# 读取图像
# image = cv2.imread('D:/PycharmProjects/segment-anything-main/finish/is/isogenic control_24.png')

# image = cv2.imread('./finish/Arg153Cys-3/Arg153Cys/stack-30.png')
# output_path = './finish/Arg153Cys-3/Arg-red/stack-30.png'
# lunkuo_path = './finish/Arg153Cys-3/Arg-red/lunkuo/stack-30.png'
# dis_a  ngle_csv = './finish/Arg153Cys-3/data/Arg/patient_30_dis.csv'


# image = cv2.imread('./finish/Arg153Cys-3/isogenic/isogenic control_14.png')
# output_path = './finish/Arg153Cys-3/iso-red/stack-14.png'
# lunkuo_path = './finish/Arg153Cys-3/iso-red/lunkuo/stack-14.png'
# dis_angle_csv = './finish/Arg153Cys-3/data/iso/iso_14_dis.csv'


for p in range(1, 43):

    # image = cv2.imread("./finish/Arg153Cys-3/Arg153Cys/stack-" + str(p) + ".png")
    # output_path = "./finish/Arg153Cys-3/11.23/Arg/Arg-red/stack-" + str(p) + ".png"
    # lunkuo_path = "./finish/Arg153Cys-3/11.23/Arg/Arg-red/lunkuo/stack-" + str(p) + ".png"
    # dis_csv = "./finish/Arg153Cys-3/11.23/Arg/patient_" + str(p) + "_dis.csv"
    # angle_csv = "./finish/Arg153Cys-3/11.23/Arg/patient_" + str(p) + "_angle.csv"

    if p < 10:
        image = cv2.imread("./R153C/R153C_SNAP(Treatment 2)/0" + str(p) + "_R153C_SNAP.png")
        # print("./R153C/C224Y(patient)/0" + str(p) + "_C224Y.png")
        output_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/0" + str(p) + "_R153C_SNAP.png"
        lunkuo_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/outline/0" + str(p) + "_R153C_SNAP.png"
        dis_csv = "./R153C/result/R153C_SNAP(Treatment 2)/distance/0" + str(p) + "_R153C_SNAP.csv"
        angle_csv = "./R153C/result/R153C_SNAP(Treatment 2)/angle/0" + str(p) + "_R153C_SNAP.csv"
    else:
        image = cv2.imread("./R153C/R153C_SNAP(Treatment 2)/" + str(p) + "_R153C_SNAP.png")
        # print("./C224Y/C224Y(patient)/0" + str(p) + "_C224Y.png")
        output_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/" + str(p) + "_R153C_SNAP.png"
        lunkuo_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/outline/" + str(p) + "_R153C_SNAP.png"
        dis_csv = "./R153C/result/R153C_SNAP(Treatment 2)/distance/" + str(p) + "_R153C_SNAP.csv"
        angle_csv = "./R153C/result/R153C_SNAP(Treatment 2)/angle/" + str(p) + "_R153C_SNAP.csv"


    # 图像预处理
    image = imutils.resize(image, height=512)

    # 计算图像的梯度
    gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    # 计算梯度的均值和标准差
    mean_gradient = np.mean(gradient_magnitude)
    stddev_gradient = np.std(gradient_magnitude)
    # 根据梯度的统计信息自适应计算阈值
    threshold = mean_gradient + 2 * stddev_gradient

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)

    gray = cv2.bilateralFilter(gray, 5, sigmaColor=100, sigmaSpace=100)

    print('thereshold:', threshold)
    binary = cv2.Canny(gray, threshold1=(threshold / 2.5), threshold2=int(threshold))
    # binary = cv2.Canny(gray, threshold1=30, threshold2=120)
    # 轮廓检索
    green_contours, hierarchy = cv2.findContours(binary,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    green_contours_len = len(green_contours)
    print("green_contours-len:", green_contours_len)

    # cv2.imshow('binary', binary)
    cv2.imwrite(lunkuo_path, binary)

    # 转换颜色空间（BGR到HSV）
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义蓝色的HSV范围
    lower_blue = np.array([75, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # 创建蓝色掩码
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # 寻找蓝色区域的轮廓
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    average_distances = []  # 存放所有中心点到每一个绿色轮廓的平均值
    angle_list = []   # 存储所有绿色轮廓的角度
    all_distances = []
    temp_n = 1   # 全局变量用于限制计算angle_list的个数
    # 遍历蓝色区域的轮廓
    for blue_contour in blue_contours:
        # 计算每个蓝色区域的面积
        blue_area = cv2.contourArea(blue_contour)
        # 设置一个阈值，仅绘制较大的蓝色区域
        if blue_area > 400:  # 更改阈值以匹配您的需求
            # 计算中心坐标
            M = cv2.moments(blue_contour)
            if M["m00"] != 0:   # 零阶矩“m00”的含义比较直观，它表示一个轮廓的面积
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # 在图像上绘制中心坐标
                cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)  # 绘制中心坐标
                cv2.drawContours(image, [blue_contour], -1, (0, 0, 255), 2)  # 绘制蓝色区域

            distances = []  # 存储到所有绿色线条的距离
            n = 0
            for i in range(len(green_contours)):
                # 筛掉面积过小的轮廓
                # area = cv2.contourArea(green_contours[i])
                green_area = cv2.arcLength(green_contours[i], False)
                if green_contours_len < 200:
                    if green_area < 100:
                        n += 0
                        continue
                    n += 1
                    # rect = cv2.minAreaRect(green_contours[i])    # 返回一个Box2D结构，其中包括以下详细信息–（中心(x,y)，（宽度、高度）、旋转角度）
                    (x, y), (w, h), angle = cv2.minAreaRect(green_contours[i])
                    # print('angle:', angle)
                    # # 计算矩形框的四个顶点坐标
                    # box = cv2.boxPoints(rect)
                    # box = np.int0(box)
                    if angle != 90:
                        if h > w:
                            angle = angle + 90
                    else:
                        if h > w:
                            angle = 0
                    if temp_n == 1:     # 只在第一次计入角度
                        angle_list.append(angle)
                    dist = cv2.pointPolygonTest(green_contours[i], (cX, cY), True)
                    distances.append(abs(dist))
                    # # 绘制轮廓
                    cv2.drawContours(image, [green_contours[i]], -1, (0, 0, 255), 1)
                else:
                    if green_area < 200:
                        n += 0
                        continue
                    n += 1
                    # rect = cv2.minAreaRect(green_contours[i])
                    (x, y), (w, h), angle = cv2.minAreaRect(green_contours[i])
                    # print('angle:', angle)
                    # # 计算矩形框的四个顶点坐标
                    # box = cv2.boxPoints(rect)
                    # box = np.int0(box)
                    # # 计算矩形框的四个顶点坐标
                    # box = cv2.boxPoints(rect)
                    # box = np.int0(box)
                    # box0 = box[0]
                    # box1 = box[1]
                    if angle != 90:
                        if h > w:
                            angle = angle + 90
                    else:
                        if h > w:
                            angle = 0
                    if temp_n == 1:  # 只在第一次计入角度
                        angle_list.append(angle)
                    # # 计算矩形框的四个顶点坐标
                    # box = cv2.boxPoints(rect)
                    # box = np.int0(box)
                    dist = cv2.pointPolygonTest(green_contours[i], (cX, cY), True)
                    distances.append(abs(dist))
                    # # 绘制轮廓
                    cv2.drawContours(image, [green_contours[i]], -1, (0, 0, 255), 1)
            temp_n = 0
            all_distances.append(distances)   # 所有距离
            print('dist:', distances)
            print('dist-len:', len(distances))
            temp = sum(distances)/len(distances)    # 一个中心点到所有绿色轮廓距离的平均值
            print('eachline-average-len:', temp)
            average_distances.append(temp)

    # # 将列表转换为 NumPy 数组
    # array = np.array(all_distances)
    # # 计算每一列的平均值
    # column_means = np.mean(array, axis=0)
    # print('column_means:', column_means)
    # print(len(column_means))
    #
    # dis_angle = []
    # dis_angle.append(column_means.tolist())
    # dis_angle.append(angle_list)
    # print('dis_angle:', dis_angle)
    #
    # # 距离写入csv
    # with open(dis_angle_csv, mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     # 使用zip函数将数据按列写入CSV文件
    #     for row in zip(*dis_angle):
    #         writer.writerow(row)


    # 距离写入csv
    with open(dis_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        # 使用zip函数将数据按列写入CSV文件
        for row in zip(*all_distances):
            writer.writerow(row)

    # 角度写入csv
    with open(angle_csv, mode='a', newline='') as file1:
        writer = csv.writer(file1)

        # 遍历一维列表，并将每个元素写入CSV文件的指定列的不同行
        for item in angle_list:
            # 创建一个包含空字符串的列表，用于表示CSV文件的一行
            row = ["" for _ in range(len(angle_list))]
            # 在指定列中插入要写入的值
            row[0] = item
            writer.writerow(row)


    # 显示带有标记的图像
    print('average_distances:', average_distances)
    all_averge_distances = sum(average_distances)/len(average_distances)
    print("n=", n)
    print('angle_list_len:', len(angle_list))
    print('angle_list:', angle_list)
    print('all-averge-distances:', all_averge_distances)
    cv2.imwrite(output_path, image)
    # cv2.imshow('Marked Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()




