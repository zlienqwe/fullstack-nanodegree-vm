import os
basepath = "/Users/zhujiang/Documents/fullstack-nanodegree-vm/learn_python/prank"
filter_char = '0123456789 '
def rename_files(base_path):
	a = os.getcwd()
	print a
	file_pwd = os.listdir(base_path)
	os.chdir(basepath)
	for file_name in file_pwd:
		path = os.path.join(base_path, file_name)
		if not os.path.isdir(path) and not path.startswith('.'):
			print file_name
			os.rename(file_name, file_name.translate(None, filter_char))

	os.chdir(file_pwd)
rename_files(basepath)