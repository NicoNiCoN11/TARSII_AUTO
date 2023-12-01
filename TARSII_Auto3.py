import os
import sys
import shutil
import subprocess

input_dir = sys.argv[1]
output_dir = sys.argv[2]
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
