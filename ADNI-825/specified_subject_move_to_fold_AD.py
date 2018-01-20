#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import datetime

import shutil

def specified_subject_move_to_fold(slice_path_txt_list, target_path, label):
	# print(slice_path_txt_list)
	# try:
	slice_index = 1
	subject_num = 0
	with open(slice_path_txt_list,"r") as slice_txt_path_list:
		for slice_txt_path in slice_txt_path_list:
			# slice_txt_path = slice_txt_path_list.readline()
			slice_txt_path = slice_txt_path.replace("\n", "")
			slice_txt_path = slice_txt_path.replace("\\", "/")
			subject_num = subject_num + 1
			try:
				subject_id = slice_txt_path.split("/")[4]
				# print("subject_id = {}".format(subject_id))
			except:
				subject_id = ""
				print("fuck..")
			# print(slice_txt_path)
			entropy_value_txt_name = "entropy_value_" + label + "_gray_matter_Slices.txt"
			slice_txt = os.path.join(slice_txt_path, entropy_value_txt_name)
			# print(slice_txt)
			with open(slice_txt, "r") as slice_path_list:
				for item_slice in slice_path_list:
					slice_name = item_slice.split(",")[0]
					try:
						if (slice_name.split(".")[1] == "jpg"):
							slice_path = os.path.join(slice_txt_path, slice_name)
							if (os.path.exists(slice_path)):
								# print("slice_path = {}".format(slice_path))
								new_slice_name = "GM" + label + str("%.5d"%slice_index) + "_" + subject_id +  ".jpg"
								# new_slice_name = "GM" + label + "_" + subject_id +  ".jpg"
								new_name = os.path.join(target_path, new_slice_name)
								slice_index = slice_index + 1
								print("copied {} image to {}".format(slice_path, new_name))
								shutil.copyfile(slice_path, new_name)
					except:
						pass
						# print("{} not a jpg file.".format(slice_name))

	# except:
	# 	print("[error]...")
	### subject_num/3 --> 3 including X Y Z
	print("subject_num = {}".format(subject_num/3))
	print("total slice num = {}".format(slice_index))

### according to AD_gray_matter_Slices_path.txt file, move all slices to a folder (AD_GM_except_entropy_zero)
### new file: all slices in a folder. AD_GM_except_entropy_zero + NC_GM_except_entropy_zero

if __name__=="__main__":
	slice_path_txt_list = './AD_NC_except_entropy_zero/AD_gray_matter_Slices_except_entropy_zero/AD_gray_matter_Slices_path.txt'
	target_path = './AD_NC_except_entropy_zero/AD_GM_except_entropy_zero_single_subject'
	label = 'AD'

	# slice_path_txt_list = './AD_NC_except_entropy_zero/NC_gray_matter_Slices_except_entropy_zero/NC_gray_matter_Slices_path.txt'
	# target_path = './AD_NC_except_entropy_zero/NC_GM_except_entropy_zero_single_subject'
	# label = 'NC'


	if not os.path.exists(target_path):
		print("Create dir = {}".format(target_path))
		os.makedirs(target_path)

	specified_subject_move_to_fold(slice_path_txt_list, target_path, label)

### run it 
### python .\specified_subject_move_to_fold.py > specified_subject_move_to_fold_AD.txt