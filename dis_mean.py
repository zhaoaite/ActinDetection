import os
import pandas as pd

# 设置文件夹路径
dis_folder_path = './R153C/result/R153C_SNAP(Treatment 2)/distance'  # 修改为你的文件夹路径
angle_folder_path = './R153C/result/R153C_SNAP(Treatment 2)/angle'  # 修改为你的文件夹路径
output_path = './R153C/result/R153C_SNAP(Treatment 2)/dis_angle'

# 遍历文件夹中的所有 CSV 文件
for filename in os.listdir(dis_folder_path):
    if filename.endswith('.csv'):
        # 构建完整的文件路径
        dis_file_path = os.path.join(dis_folder_path, filename)
        angle_file_path = os.path.join(angle_folder_path, filename)

        # 读取 CSV 文件
        df = pd.read_csv(dis_file_path, header=None)
        # 求和
        row_sum = df.sum(axis=1)

        # 计算每行的平均值
        num_columns = df.shape[1]                 # 获取列数
        row_averages = row_sum / num_columns

        # 创建新的 DataFrame 来保存每行的平均值
        result_df = pd.DataFrame(row_averages)


        df2 = pd.read_csv(angle_file_path, header=None)
        # 删除所有包含NaN值的列
        df2 = df2.dropna(axis=1, how='all')
        #print(df2)

        # 求和
        row_sum = df2.sum(axis=1)

        # 计算每行的平均值
        num_columns = df2.shape[1]  # 获取列数
        row_averages = row_sum / num_columns

        # 将平均值追加到第二列
        result_df.insert(1, '', row_averages)


        # 设置输出文件路径，命名为原文件名 + '_averages.csv'
        output_file = os.path.join(output_path, filename.replace('.csv', '_averages.csv'))

        # 保存结果到新的 CSV 文件
        result_df.to_csv(output_file, index=False, header=False)

        print(f"文件 {filename} 的计算结果已保存到 {output_file}")

