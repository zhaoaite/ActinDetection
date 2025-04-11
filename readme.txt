1.首先更改BlueAreaCenter2dis_2.py文件中的目录

        image = cv2.imread("./R153C/R153C_SNAP(Treatment 2)/0" + str(p) + "_R153C_SNAP.png")                                    //原图像文件路径及文件名
        output_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/0" + str(p) + "_R153C_SNAP.png"                        //输出标记stress fiber边缘和蓝色区域的路径及文件名
        lunkuo_path = "./R153C/result/R153C_SNAP(Treatment 2)/image/outline/0" + str(p) + "_R153C_SNAP.png"            //输出边缘轮廓的二值图像的文件路径及文件名   
        dis_csv = "./R153C/result/R153C_SNAP(Treatment 2)/distance/0" + str(p) + "_R153C_SNAP.csv"                               //计算出的距离保存到的csv文件路径及文件名
        angle_csv = "./R153C/result/R153C_SNAP(Treatment 2)/angle/0" + str(p) + "_R153C_SNAP.csv"                               //计算出的角度保存到的csv文件路径及文件名

修改完成后，直接运行即可

2.dis_mean.py
# 设置文件夹路径
dis_folder_path = './R153C/result/R153C_SNAP(Treatment 2)/distance'  	// BlueAreaCenter2dis_2.py文件中距离保存到的csv文件路径，不包括文件名，只要路径即可
angle_folder_path = './R153C/result/R153C_SNAP(Treatment 2)/angle'      // BlueAreaCenter2dis_2.py文件中角度保存到的csv文件路径，不包括文件名，只要路径即可
output_path = './R153C/result/R153C_SNAP(Treatment 2)/dis_angle'         //距离的平均值及角度的保存路径，不需要文件名，路径即可

3.Spatial_dispersion.py
修改dsp_csv = "./R153C/result/R153C_SNAP(Treatment 2)/Spatial_dispersion.csv"为输出路径
修改data = pd.read_csv("./R153C/result/R153C_SNAP(Treatment 2)/dis_angle/0" + str(p) + "_R153C_SNAP_averages.csv", header=None)为dis_mean.py中output_path路径，需要加上文件名



执行顺序：先执行BlueAreaCenter2dis_2.py，然后执行dis_mean.py，最后执行Spatial_dispersion.py