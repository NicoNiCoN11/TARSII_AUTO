# TARSII_AUTO
A method to predict the DMRs of genome of mammals efficiently

Another auto-product since the last one was published, and in this TARSII_Auto which is based on the TARSII developed by Zhangyi's lab, 
Here, we design a script that can make commands to the TARSII automatically, what we need to do is giving it the path to the raw data and path to the output data
This script can also catagories each file based on the file name and make different folders to make them more clear

This version can only be used on Macos now

How to use TARS_AUTO:
step1 : download TARS-for-macos and follow the steps to set TARS to the work path(chmod u + x)
step2 : download the TARS_Auto-v1.0
step3 : use "python TARS_Auto-v1.0 <input_files> <output_files>" to activate this script 
step4 : check the output path

input files should contain:
mCG_file.txt show the mCG levels in single base resolution in each tissue (>=6)
sam file generated from Bismark for each tissue(>=6)
Txt file from sperm/oocyte or AG/PG early embryos indicating mCG levels in single base resolution(=2)

