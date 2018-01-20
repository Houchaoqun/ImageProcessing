#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import datetime

import shutil
import random

train_percentage = 0.8
val_percentage = 0.2
test_percentage = 0.0

def backup_txt_rename(txt_path):
	if os.path.exists(txt_path):
		i = datetime.datetime.now()
		date = str(i.year) + str(i.month) + str(i.day) + str(i.hour) + str(i.minute) + str(i.second)
		new_name = txt_path +".bak" + date
		os.rename(txt_path, new_name)
		print("copied and deleted file, new_name = {}".format(new_name))

def create_dir(dir_path):
	if not os.path.exists(dir_path):
		print("Create dir = {}".format(dir_path))
		os.makedirs(dir_path)

def get_slice_train_val_test(slice_path_txt_list, train_slice_path, val_slice_path, test_slice_path, label):
	### added by hcq 20180119
	### 
	# MCI_subject_num = 825 - 199 - 230 = 396 including sMCI, pMCI
	backup_txt_rename(train_slice_path)
	backup_txt_rename(val_slice_path)
	slice_list = os.listdir(slice_path_txt_list)
	# print(slice_list[0]) = GMAD17283_S002.jpg
	AD_subject_num = 199
	NC_subject_num = 230
	train_slice_num = 0
	val_slice_num = 0

	if ((label + "_subject_num") == "AD_subject_num"):
		subject_num = AD_subject_num
	elif ((label + "_subject_num") == "NC_subject_num"):
		subject_num = NC_subject_num
	else:
		print("fuck..")

	rondom_list = random.sample(range(1, subject_num+1), subject_num)

	### set the number of train, val, test
	train_num = int(train_percentage * subject_num)
	val_num = subject_num - train_num
	# test_num = len_slice_list - train_num - val_num
	print("total_sbject = {}".format(subject_num))
	print("train_sbject = {}".format(train_num))
	print("val_sbject = {}".format(val_num))

	# train: [0, train_num-1]
	print("===")
	print("{}, train_slice_path = {}".format(label, train_slice_path))
	with open(train_slice_path, "a") as train_txt:
		for i in range(train_num):
			rondom_id = rondom_list[i]
			rondom_id = "S" + str("%.3d"%rondom_id)
			
			for slice_item in slice_list:
				slice_name = slice_item.split(".")[0]
				subject_name = slice_name.split("_")[1]
				# print(subject_name)
				# print("rondom_id = {}".format(rondom_id))
				# print("subject_name = {}".format(subject_name))
				if (rondom_id == subject_name):
					print(slice_item)
					train_txt.writelines(slice_item + "\n")
					train_slice_num = train_slice_num + 1

	# val: [train_num, train_num + val_num - 1]
	print("===")
	print("{}, val_slice_path = {}".format(label, val_slice_path))
	with open(val_slice_path, "a") as val_txt:
		for i in range(val_num):
			index = i + train_num
			rondom_id = rondom_list[index]
			rondom_id = "S" + str("%.3d"%rondom_id)
			# print("test_num = {}".format(test_num))		
			for slice_item in slice_list:
				slice_name = slice_item.split(".")[0]
				subject_name = slice_name.split("_")[1]
				# print(subject_name)	
				if (rondom_id == subject_name):
					print(slice_item)
					val_txt.writelines(slice_item + "\n")
					val_slice_num = val_slice_num + 1
	print("train_slice_num = {}".format(train_slice_num))
	print("val_slice_num = {}".format(val_slice_num))
	### added finished 20180119

	### adde by hcq 20180113
	### get all silce through its path
	# slice_list = os.listdir(slice_path_txt_list)
	# len_slice_list = len(slice_list)
	# # print(slice_list[0]) = GMAD17283_S002.jpg

	# ### backup the old txt file
	# backup_txt_rename(train_slice_path)
	# backup_txt_rename(val_slice_path)
	# # backup_txt_rename(test_slice_path)
	
	# ### set the number of train, val, test
	# train_num = int(train_percentage * len_slice_list)
	# val_num = len_slice_list - train_num
	# # test_num = len_slice_list - train_num - val_num
	# print("total_num = {}".format(len_slice_list))
	# print("train_num = {}".format(train_num))
	# print("val_num = {}".format(val_num))
	# # print("test_num = {}".format(test_num))

	# ### create a rondom list without repetition
	# rondom_list = random.sample(range(1, len_slice_list+1), len_slice_list)

	# ### create txt file to store the index of train, val, test
	# # train: [0, train_num-1]
	# with open(train_slice_path, "a") as train_txt:
	# 	for i in range(train_num):
	# 		slice_index = rondom_list[i]
	# 		slice_name = "GM" + label + str("%.5d"%slice_index) + ".jpg"
	# 		train_txt.writelines(slice_name + "\n")
		
	# # val: [train_num, train_num + val_num - 1]
	# with open(val_slice_path, "a") as val_txt:
	# 	for i in range(val_num):
	# 		index = i + train_num
	# 		slice_index = rondom_list[index]
	# 		slice_name = "GM" + label + str("%.5d"%slice_index) + ".jpg"
	# 		val_txt.writelines(slice_name + "\n")

	# test: [train_num + val_num, end]
	# with open(test_slice_path, "a") as test_txt:
	# 	for i in range(test_num):
	# 		index = train_num + i
	# 		slice_index = rondom_list[index]
	# 		slice_name = "GM" + label + str("%.5d"%slice_index) + ".jpg"
	# 		test_txt.writelines(slice_name + "\n")

	### added finished 20180113

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
		print("slice txt [{}] is not exist...".format(slice_path_txt_list))


if __name__=="__main__":
	### 
	run_flag = 'NC'
	dataset_path = "AD_NC_except_entropy_zero"
	fold_name = "single_subject_data_fold_03_entropy_except_zero"
	print("dataset_path = {}".format(dataset_path))
	print("label = {}".format(run_flag))
	print("fold_name = {}".format(fold_name))

	### 
	if (run_flag == 'AD'):
		### initial
		# AD GM
		slice_path_txt_list = './' + dataset_path + '/AD_GM_except_entropy_zero_single_subject'
		train_slice_path = './' + dataset_path + '/ADGM_train_' + fold_name + '.txt'
		val_slice_path = './' + dataset_path + '/ADGM_val_' + fold_name + '.txt'
		test_slice_path = './' + dataset_path + '/ADGM_test_' + fold_name + '.txt'
		label = 'AD'
		### create the txt file of train, val, test
		get_slice_train_val_test(slice_path_txt_list, train_slice_path, val_slice_path, test_slice_path, label)

		### move slice to folder of train, val, test
		train_target_path = "./InceptionV4_FineTunning/" + fold_name + "/train/" + label
		create_dir(train_target_path)
		move_slice_to_train_val_test_fold(slice_path_txt_list, train_slice_path, train_target_path)

		val_target_path = "./InceptionV4_FineTunning/" + fold_name + "/validation/" + label
		create_dir(val_target_path)
		move_slice_to_train_val_test_fold(slice_path_txt_list, val_slice_path, val_target_path)


	elif (run_flag == 'NC'):
		# NC GM
		slice_path_txt_list = './' + dataset_path + '/NC_GM_except_entropy_zero_single_subject'
		train_slice_path = './' + dataset_path + '/NCGM_train_' + fold_name + '.txt'
		val_slice_path = './' + dataset_path + '/NCGM_val_' + fold_name + '.txt'
		test_slice_path = './' + dataset_path + '/NCGM_test_' + fold_name + '.txt'
		label = 'NC'
		### create the txt file of train, val, test
		get_slice_train_val_test(slice_path_txt_list, train_slice_path, val_slice_path, test_slice_path, label)

		### move slice to folder of train, val, test
		train_target_path = "./InceptionV4_FineTunning/" + fold_name + "/train/" + label
		create_dir(train_target_path)
		move_slice_to_train_val_test_fold(slice_path_txt_list, train_slice_path, train_target_path)

		val_target_path = "./InceptionV4_FineTunning/" + fold_name + "/validation/" + label
		create_dir(val_target_path)
		move_slice_to_train_val_test_fold(slice_path_txt_list, val_slice_path, val_target_path)



### run it 
### python .\specified_subject_get_slice_train_val_test.py > specified_subject_get_slice_train_val_test.txt