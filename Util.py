#


def tokenizeString(strng,symbolList):
 	result=[]

 	while strng!='':
 		oneFound=False
	 	for s in symbolList:
	 		strngAux=strng.replace(s,'',1)
	 		if strng != strngAux and strng.index(s)==0:
	 			oneFound=True
	 			result.append(s)
	 			strng=strngAux
	 	if not oneFound:	
 			return False
 	return result


