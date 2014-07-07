import os
filenames=os.listdir(os.getcwd())
reviews=[]
for filename in filenames:
	if filename[0:6]=="review":
		f=open(filename)
		tmp=f.read().splitlines()
		reviews.append(tmp)

for i in range(0,len(reviews)):
	print '[!!review',i,']:'
	print (reviews[i])[0]

