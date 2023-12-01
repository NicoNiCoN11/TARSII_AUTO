import sys
import os
import subprocess

input_parental = sys.argv[1]
input_bed = sys.argv[2]
output_dir = sys.argv[3]
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
