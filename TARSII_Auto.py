import os
import sys
import shutil


def tars_divide(data, output):  # 定义函数将不同的文件分类
    # data : path to the data
    # output: path to the output
    if data.endswith("mCG_file.wig"):  # 将mCG的wig格式的文件进行分类整理
        mCG_data = data
        # 将mCGdata复制到output目录下面
        mCG_dir = os.path.join(output, "mCG")  # 将mCG_dir的路径修改为path/to/output/mCG
        os.makedirs(mCG_dir, exist_ok=True)  # 创建path/to/output/mCG这个路径对应的文件夹
        shutil.move(mCG_data, mCG_dir)  # 将mCGdata文件复制到mCG_dir路径下
    elif data.endswith(".sam"):  # 将bismark产生的sam文件分类
        sam_data = data
        sam_dir = os.path.join(output, "sam")
        os.makedirs(sam_dir, exist_ok=True)
        shutil.move(sam_data, sam_dir)
    elif data.endswith(".wig"):  # 将其他的wig文件分类整理
        parental_data = data
        parental_dir = os.path.join(output, "parental")
        os.makedirs(parental_dir, exist_ok=True)
        shutil.move(parental_data, parental_dir)
    else:
        return


data_dir = sys.argv[1]  # 命令行第一个参数输入输入文件路径
output_dir = sys.argv[2]  # 命令行第二个参数输入输出文件路径
# 获取输入数据目录下的所有文件名
file_list = os.listdir(data_dir)
# 过滤掉格式不对的文件
data_list = [file for file in file_list if file.endswith(".wig") or file.endswith(".sam")]
# 整理文件从而保证后续分析按顺序进行
data_list = sorted(data_list)
for file in data_list:
    data = os.path.join(data_dir, file)
    output = output_dir
    tars_divide(data, output)

