from os.path import exists

def valid_name(name, path):
	if " " in name:
		print("please do not contain spaces in the name")
		return False
	
	file_exist = exists(path+ "/" + name +".yaml")
	if file_exist == True:
		print("file already exit")
		return False
	return True 
