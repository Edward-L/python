import os

def replace_str(FilePath,SourceStr,ObjectStr):
	file = open (FilePath,'r')
	str = file.read()
	str = str.replace(SourceStr,ObjectStr)
	file.close()
	file = open(FilePath,'w')
	file.write(str)
	file.close()

# def getfile(path):
# 	for file in os.listdir(path):
# 		file = os.path.join(path,file)
# 		if os.path.isdir(file):
# 			getfile(file)
# 		else:
# 			replace_str(file, 'abcd', '')

def getfile(path):
	generator = os.walk(path)
	for (now_dir, _, file_list,) in generator:
		for file in file_list:
			file = os.path.join(now_dir, file)
			replace_str(file, "abc", " ")

rootpath = "/Users/Edward_L/Desktop/playground"
getfile(rootpath)