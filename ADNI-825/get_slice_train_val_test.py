#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import datetime

import shutil
import random

train_percentage = 0.6
val_percentage = 0.2
test_percentage = 0.2

def backup_txt_rename(txt_path):
	if os.path.exists(txt_path):
		i = datetime.datetime.now()
		date = str(i.year) + str(i.month) + str(i.day) + str(i.hour) + str(i.minute) + str(i.second)
		new_name = txt_path +".bak" + date
		os.rename(txt_path, new_name)
		print("copied and deleted file, new_name = {}".format(new_name))

def get_slice_train_val_test(slice_path_txt_list, train_slice_path, val_slice_path, test_slice_path, label):
	### get all silce through its path
	slice_list = os.listdir(slice_path_txt_list)
	len_slice_list = len(slice_list)

	### backup the old txt file
	backup_txt_rename(train_slice_path)
	backup_txt_rename(val_slice_path)
	backup_txt_rename(test_slice_path)
	
	### set the number of train, val, test
	train_num = int(train_percentage * len_slice_list)
	val_num = int(val_percentage * len_slice_list)
	test_num = len_slice_list - train_num - val_num
	print("total_num = {}".format(len_slice_list))
	print("train_num = {}".format(train_num))
	print("val_num = {}".format(val_num))
	print("test_num = {}".format(test_num))

	### create a rondom list without repetition
	rondom_list = random.sample(range(1, len_slice_list+1), len_slice_list)

	### create txt file to store the index of train, val, test
	# train: [0, train_num-1]
	with open(train_slice_path, "a") as train_txt:
		for i in range(train_num):
			slice_index = rondom_list[i]
			slice_name = "GM" + label + str("%.5d"%slice_index) + ".jpg"
			train_txt.writelines(slice_name + "\n")
		
	# val: [train_num, train_num + val_num - 1]
	with open(val_slice_path, "a") as val_txt:
		for i in range(val_num):
			index = i + train_num
			slice_index = rondom_list[index]
			slice_name = "GM" + label + str("%.5d"%slice_index) + ".jpg"
			val_txt.writelines(slice_name + "\n")

	# test: [train_num + val_num, end]
	with open(test_slice_path, "a") as test_txt:
		for i in range(test_num):
			index = train_num + i
			slice_index = rondom_list[index]
			slice_name = "GM" + label + str("%.5d"%slice_index) + ".jpg"
			test_txt.writelines(slice_name + "\n")


def move_slice_to_train_val_test_fold(slice_path_txt_list, slice_txt_path, target_path):
	if os.path.exists(slice_txt_path):
		with open(slice_txt_path,"r") as slice_list_file:
			for slice_name in slice_list_file:
				slice_name = slice_name.replace("\n", "")
				try:
					if (slice_name.split(".")[1] == "jpg"):
						slice_pos = os.path.join(slice_path_txt_list, slice_name)
						# print("slice_pos = {}".format(slice_pos))
						target_slice_pos = os.path.join(target_path, slice_name)
						print("target_slice_pos = {}".format(target_slice_pos))
						shutil.copyfile(slice_pos, target_slice_pos)
				except:
					pass
	else:
		print("slice txt is not exist...")


if __name__=="__main__":
	### 
	run_flag = 'AD'

	### 
	if (run_flag == 'AD'):
		### initial
		# AD GM
		slice_path_txt_list = './AD_NC_except_entropy_zero/AD_GM_except_entropy_zero'
		train_slice_path = './AD_NC_except_entropy_zero/ADGM_train_except_entropy_zero.txt'
		val_slice_path = './AD_NC_except_entropy_zero/ADGM_val_except_entropy_zero.txt'
		test_slice_path = './AD_NC_except_entropy_zero/ADGM_test_except_entropy_zero.txt'
		label = 'AD'
		### create the txt file of train, val, test
		get_slice_train_val_test(slice_path_txt_list, train_slice_path, val_slice_path, test_slice_path, label)

		### move slice to folder of train, val, test
		train_target_path = "./InceptionV4_FineTunning/data_fold_02_entropy_except_zero/train/" + label
		move_slice_to_train_val_test_fold(slice_path_txt_list, train_slice_path, train_target_path)

		val_target_path = "./InceptionV4_FineTunning/data_fold_02_entropy_except_zero/validation/" + label
		move_slice_to_train_val_test_fold(slice_path_txt_list, val_slice_path, val_target_path)

		test_target_path = "./InceptionV4_FineTunning/data_fold_02_entropy_except_zero/test/" + label
		move_slice_to_train_val_test_fold(slice_path_txt_list, test_slice_path, test_target_path)

	elif (run_flag == 'NC'):
		# NC GM
		slice_path_txt_list = './AD_NC_except_entropy_zero/NC_GM_except_entropy_zero'
		train_slice_path = './AD_NC_except_entropy_zero/NCGM_train_except_entropy_zero.txt'
		val_slice_path = './AD_NC_except_entropy_zero/NCGM_val_except_entropy_zero.txt'
		test_slice_path = './AD_NC_except_entropy_zero/NCGM_test_except_entropy_zero.txt'
		label = 'NC'
		### create the txt file of train, val, test
		get_slice_train_val_test(slice_path_txt_list, train_slice_path, val_slice_path, test_slice_path, label)

		### move slice to folder of train, val, test
		train_target_path = "./InceptionV4_FineTunning/data_fold_02_entropy_except_zero/train/" + label
		move_slice_to_train_val_test_fold(slice_path_txt_list, train_slice_path, train_target_path)

		val_target_path = "./InceptionV4_FineTunning/data_fold_02_entropy_except_zero/validation/" + label
		move_slice_to_train_val_test_fold(slice_path_txt_list, val_slice_path, val_target_path)

		test_target_path = "./InceptionV4_FineTunning/data_fold_02_entropy_except_zero/test/" + label
		move_slice_to_train_val_test_fold(slice_path_txt_list, test_slice_path, test_target_path)




### run it 
### python .\get_data.py > result.txt