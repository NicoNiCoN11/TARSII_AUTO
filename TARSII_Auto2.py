import os
import sys
import subprocess
# 定义mCG,sam文件夹的路径，并定义输出文件夹的路径
mCG_dir = sys.argv[1]
sam_dir = sys.argv[2]
output_dir = sys.argv[3]
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
                    "-x", mCG_file, "-s", sam_file, "-o", output_file])
    # 打印一些提示信息
    print(f"Processing file step1_output_ {i + 1}: {mCG_files[i]} and {sam_files[i]}")
    print(f"Output folder: {folder_path}")
# 检查是否有未被分析的data
folder_list = os.listdir(output_dir)  # 获取输出文件夹下的所有文件和文件夹的名字
folder_count = len(folder_list)
if folder_count == len(mCG_files):
    print("All files have been analysed")
else:
    print("Something wrong please check the log")
