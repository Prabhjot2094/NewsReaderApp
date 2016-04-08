import os

	
def get_filenames(location):
	print location
	files = os.listdir("F:\News\\"+location+"\\")
	arr = []
	x=0
	for i in files:
		x+=1
		directory = "F:\News\\"+location+"\\"+i
		# if location[1] == "text":	
		# 	if i[-4:]==".jpg":
		# 		arr.append(directory)
		# 		return
		# 		continue
		# elif location[1] == "image":
		# 	if i[-4:]==".txt":
		# 		continue
		arr.append(directory)
		# if x==4:
		# 	break
	print arr
	return arr