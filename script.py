import numpy
import csv
import random

def getInput(a,b):
	"""
		Input: Name of file to read from and the array.
		Output: Enters the data into the array.
	"""
	with open(a) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=';')
	    for row in csv_reader:
	    	b.append(row)

def matchTitles(a,b,c):
	"""
		Input: Two array with data.
		Output: Matches the titles and fills the relevant matched data into the third array.
	"""
	for i in a:
		for j in b:
			if(i[0].lower()==j[2].lower()):
				c.append([i[0]]+j[5:6]+j[7:15]+[i[2]])

def rectifyData(a):
	"""
		Input: Final matched Data.
		Output: Removes inconsistency from the data.
	"""
	for i in a:
		for j in i:
			if(len(j)==0):
				a.remove(i)
		for k in range(1,len(i)):
			if(',' in i[k]):
				s=''
				for j in i[k]:
					if(j!=','):
						s+=j
					else:
						s+='.'
				i[k]=s

def combinations(a,i,finalData):
	"""
		Input: Auxilary array a, i(Current index), Final matched data
		Output: returns all the possible combinations of variables and calls the function getAnswer()
				for it.
	"""
	if(i==8):
		a[i]=True
		getAnswer(a,finalData)
		a[i]=False
		getAnswer(a,finalData)
	else:
		a[i]=True
		combinations(a,i+1,finalData)
		a[i]=False
		combinations(a,i+1,finalData)

def getAnswer(variablesToconsider,finalData):
	"""
		Input: Final matched data, combination of varibale to consider.
		OUtput: Writes the final error and mean squared error to a file.
	"""
	varibales=["SJR","H index","Total Docs(2017)","Total Docs(3yrs)","Total Refs.","Total cites(3yrs)","Citable Docs(3 yrs)","Cites(2 yrs)","Ref"]
	N=len(finalData)
	n=int(.8*N)
	va=1
	x=numpy.arange(N*(sum(variablesToconsider)+1)).reshape(N,(sum(variablesToconsider)+1))
	y=[float(finalData[i][10]) for i in range(N)]
	for i in range(N):
		x[i][0]=1
	for i in range(len(variablesToconsider)):
		if(variablesToconsider[i]):
			for j in range(N):
				x[j][va]=float(finalData[j][i+1])
			va+=1

	b=numpy.matmul(x[:n,:].transpose(),x[:n,:])
	b=numpy.linalg.inv(b)
	b=numpy.matmul(b,x[:n,:].transpose())
	b=numpy.matmul(b,y[:n])
	yi=y[n:]
	xi=x[n:]
	y_calculated=numpy.matmul(xi,b)
	errorMean=0
	errorRMS=0
	for i in range(len(yi)):
		errorMean+=abs(yi[i]-y_calculated[i])
		errorRMS+=abs(yi[i]-y_calculated[i])**2
	errorRMS/=len(yi)
	errorMean/=len(yi)
	update=[]
	s=""
	for i in range(len(variablesToconsider)):
		if(variablesToconsider[i]):
			s+=varibales[i]
			s+=' '
	update.append(s)
	
	update+=[str(errorMean)]
	update+=[str(errorRMS)]
	with open('Answer.csv', 'a') as csvFile:
	    writer = csv.writer(csvFile)
	    writer.writerow(update)


def printMinimumError(s):
	"""
		Input: File which contains the list of error for all 
				Combinations.
		Output: Prints the minimum error and mean squared errror 
				found in the file and also the combination in which
				it was found.
	"""
	array=[]
	with open(s) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    for row in csv_reader:
	    	array.append(row)
	
	minimumError=1000000000
	s1=""
	minimumErrorRMS=10000000000
	s2=""

	for i in range(1,len(array)-1):
		if(float(array[i][1])<minimumError):
			minimumError=float(array[i][1])
			s1=array[i][0]
		if(float(array[i][2])<minimumErrorRMS):
			minimumErrorRMS=float(array[i][2])
			s2=array[i][0]

	print("Minimum error:",minimumError,"in",s1)
	print("Minimum Mean Squared error:",minimumErrorRMS,"in",s2)

if __name__ == '__main__':
	jourData=[]
	foundData=[]
	finalData=[]
	getInput("jour.csv",jourData)
	getInput("found.txt",foundData)
	matchTitles(foundData,jourData,finalData)
	rectifyData(finalData)
	random.shuffle(finalData)
	update=["Combination","Mean Error", "Mean Squared Error"]
	with open('Answer.csv', 'w') as csvFile:
	    writer = csv.writer(csvFile)
	    writer.writerow(update)
	combinations([False,False,False,False,False,False,False,False,False],0,finalData)
	printMinimumError("Answer.csv")