import os
import sys
import shutil


import subprocess


# Part 1 divide input files into different paths
def tars_divide(data, output):  # 定义函数将不同的文件分类
    # data: path to the data
    # output: path to the output
    if data.endswith("mCG_file.wig"):  # 将mCG的wig格式的文件进行分类整理
        mcg_data = data
        # 将mCGdata复制到output目录下面
        mcg_dir = os.path.join(output, "mCG")  # 将mCG_dir的路径修改为path/to/output/mCG
        os.makedirs(mcg_dir, exist_ok=True)  # 创建path/to/output/mCG这个路径对应的文件夹
        shutil.move(mcg_data, mcg_dir)  # 将mCGdata文件复制到mCG_dir路径下
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


# Part2 run step1 automatically
# 定义mCG,sam文件夹的路径，并定义输出文件夹的路径
mCG_dir = os.path.join(output_dir, "mCG")
sam_dir = os.path.join(output_dir, "sam")
# output_dir = sys.argv[3]
# 获取mCG和sam文件夹下面的全部文件，并用sorted进行排序
mCG_files = sorted(os.listdir(mCG_dir))
sam_files = sorted(os.listdir(sam_dir))
# 检查两个文件夹中的文件数是否相等
if len(mCG_files) != len(sam_files):
    print("Error: mCG files and sam files do not match")
# 使用一个循环遍历mCG中的文件和sam中的文件
for i in range(len(mCG_files)):
    # 取出一对文件，拼接完整对路径
    mCG_file = os.path.join(mCG_dir, mCG_files[i])
    sam_file = os.path.join(sam_dir, sam_files[i])
    # 创建一个folder_name作为文件夹,此处用f-string语法
    folder_name = f"step1_output_{i+1}"
    # 拼接输出文件夹和文件夹名，得到一个新的路径
    folder_path = os.path.join(output_dir, folder_name)
    # 创建一个新文件夹
    os.makedirs(folder_path, exist_ok=True)
    output_file = folder_path  # 输出文件到指定文件夹中
    # 调用分析脚本
    subprocess.run(["sh", "/Users/guojiayi/DMR_prediction/TARSII/TARSII_step1_DMR_identify.sh",
                    "-x", mCG_file, "-s", sam_file, "-o", output_file])  # 得到多组数据分别存放在不同的文件夹中
    # 打印一些提示信息
    print(f"Processing file step1_output_ {i + 1}: {mCG_files[i]} and {sam_files[i]}")
    print(f"Output folder: {folder_path}")
# 检查是否有未被分析的data
folder_list = os.listdir(output_dir)  # 获取输出文件夹下的所有文件和文件夹的名字
folder_count = len(folder_list)
if folder_count == len(mCG_files):
    print("All files have been analysed with step1,step2 will start")
else:
    print("ERROR:Something wrong please check the log")
    exit(1)


# Part3 run step2 automatically
# 对不同文件夹的相同类型文件进行分类整理
input_dir = output_dir
file_list = os.listdir(input_dir)  # 获取目录下所有文件名
for file in file_list:
    if file.endswith("_DMR_candidate.bed"):  # 将文件进行分类整理
        candidate_data = os.path.join(input_dir, file)  # 拼接待分类文件的完整路径
        candidate_dir = os.path.join(input_dir, "candidate")  # 拼接子文件夹的完整路径
        os.makedirs(candidate_dir, exist_ok=True)  # 创建子文件夹
        shutil.move(candidate_data, candidate_dir)  # 将文件移动到子文件夹下
    elif file.endswith(".bed"):
        PMD_data = os.path.join(input_dir, file)
        PMD_dir = os.path.join(input_dir, "PMD_predict")
        os.makedirs(PMD_dir, exist_ok=True)
        shutil.move(PMD_data, PMD_dir)
    else:
        other_data = os.path.join(input_dir, file)
        other_dir = os.path.join(input_dir, "other")
        os.makedirs(other_dir, exist_ok=True)
        shutil.move(other_data, other_dir)

subprocess.run(["sh", "TARSII_step2_DMR_integration.sh",  # 调用脚本进行分析
                "-f", f"{input_dir}/candidate/*", "-o", f"{output_dir}"])

# Part4 run step3 automatically
input_parental = os.path.join(output_dir, "parental")
input_bed = os.path.join(output_dir, "PMD_predict")
parental_list = os.listdir(input_parental)
for file in parental_list:
    if file.find("pat") != -1:
        # 将名字中带有pat的文件路径保存下来
        pat_path = os.path.join(input_parental, file)
        print("父系mCG文件的路径为："f"{pat_path}")
    elif file.find("mat") != -1:
        mat_path = os.path.join(input_parental, file)
        print("母系mCG文件的路径为："f"{mat_path}")
    else:
        print("no such file in the path")
subprocess.run(["sh", "TARSII_step3_germline_DMR.sh", "-p",
                f"{pat_path}", "-m", f"{mat_path}", "-b", f"{input_bed}", "-o", f"{output_dir}"])
