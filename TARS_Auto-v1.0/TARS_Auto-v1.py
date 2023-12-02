import os
import sys
import shutil


import subprocess


# Part 1 divide input files into different paths
def tars_divide(data, output):  # 定义函数将不同的文件分类
    # data : path to the data
    # output: path to the output
    ext = os.path.splitext(data)[1]  # 获取文件的扩展名
    base = os.path.basename(data)  # 获取文件的基本名
    if base.find("mCG_file") != -1:  # 将mCG的txt格式的文件进行分类整理
        mCG_dir = os.path.join(output, "mCG")  # 将mCG_dir的路径修改为path/to/output/mCG
        os.makedirs(mCG_dir, exist_ok=True)  # 创建path/to/output/mCG这个路径对应的文件夹
        shutil.move(data, mCG_dir)  # 将mCGdata文件移动到mCG_dir路径下
    elif ext == ".sam":  # 将bismark产生的sam文件分类
        sam_dir = os.path.join(output, "sam")
        os.makedirs(sam_dir, exist_ok=True)
        shutil.move(data, sam_dir)
    elif ext == ".txt":  # 将其他的txt文件分类整理
        parental_dir = os.path.join(output, "parental")
        os.makedirs(parental_dir, exist_ok=True)
        shutil.move(data, parental_dir)
    else:
        return


data_dir = sys.argv[1]  # 命令行第一个参数输入输入文件路径
output_dir = sys.argv[2]  # 命令行第二个参数输入输出文件路径
# 获取输入数据目录下的所有文件名
file_list = os.listdir(data_dir)
# 过滤掉格式不对的文件
data_list = [file for file in file_list if file.endswith(".txt") or file.endswith(".sam")]
# 整理文件从而保证后续分析按顺序进行
data_list = sorted(data_list)
for filename in data_list:
    data = os.path.join(data_dir, filename)  # 拼接文件的完整路径
    output = output_dir
    tars_divide(data, output)

# Part2 run step1 automatically
# 定义mCG,sam文件夹的路径，
mCG_dir = os.path.join(output_dir, "mCG")
sam_dir = os.path.join(output_dir, "sam")
mCG_files = sorted(os.listdir(mCG_dir))
sam_files = sorted(os.listdir(sam_dir))
# 检查两个文件夹中的文件数是否相等
if len(mCG_files) != len(sam_files):
    print("Error: mCG files and sam files do not match")
output_path = os.path.join(output_dir, "Step1_output")
os.makedirs(output_path, exist_ok=True)
n = 0
# 使用一个循环遍历mCG中的文件和sam中的文件
for i in range(len(mCG_files)):
    # 取出一对文件，拼接完整对路径
    mCG_file = os.path.join(mCG_dir, mCG_files[i])
    sam_file = os.path.join(sam_dir, sam_files[i])
    # 创建一个file_name作为输出文件的名称
    file_name = f"Step1_output{i+1}"
    # 拼接输出文件夹和文件夹名，得到一个新的路径
    folder_path = os.path.join(output_path, file_name)
    # 调用分析脚本
    subprocess.run(["sh", "/Users/guojiayi/DMR_prediction/TARSII/TARSII_step1_DMR_identify.sh",
                    "-x", mCG_file, "-s", sam_file, "-o", folder_path])
    # 打印一些提示信息
    print(f"Processing file step1_output_ {i + 1}: {mCG_files[i]} and {sam_files[i]}")
    print(f"Output folder: {folder_path}")
    n = n + 1  # 循环计时器
# 检查是否有未被分析的data
if n == len(mCG_files):
    print("All files have been analysed with step1")
else:
    print("Error in step1 Something wrong please check the log")
    exit(1)

# Part3 run step2 automatically
# 对不同文件夹的相同类型文件进行分类整理
input_dir = output_path
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

subprocess.run(["sh", "/Users/guojiayi/DMR_prediction/TARSII/TARSII_step2_DMR_integration.sh",  # 调用脚本进行分析
                "-f", f"{input_dir}/candidate/*", "-o", f"{output_dir}"])

# Part4 run step3 automatically
input_parental = os.path.join(output_dir, "parental")
input_bed = os.path.join(output_path, "PMD_predict")
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
subprocess.run(["sh", "/Users/guojiayi/DMR_prediction/TARSII/TARSII_step3_germline_DMR.sh", "-p",
                f"{pat_path}", "-m", f"{mat_path}", "-b", f"{input_bed}", "-o", f"{output_dir}"])
print("All missions done! please check the", f"{output_dir}")
