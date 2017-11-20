# -*- coding: utf-8 -*-
import string
from Production import Production
from Tree import Tree
import logging

logging.basicConfig(level=logging.DEBUG)

class Grammar:
	NotTerminals=string.ascii_uppercase;
	Terminals= string.ascii_lowercase+string.digits+string.punctuation+'ε' 

	LOG=logging.getLogger()						# We isntantiate a logging object for debugging purposes
	LOG.setLevel('WARNING')
	Productions=[]								# Ceate a Productions list
	VT=[]
	VN=[] 
	ProdsJoined=[]
	Type=''
	description=''
	PrimeroSet={}
	SiguienteSet={}

	def __init__(self):
		VT=[]
		VN=[] 
		ProdsJoined=[]
		Type=''
		description=''
		PrimeroSet={}
		SiguienteSet={}


	def copy(self):
		 Aux=Grammar()
		 Aux.VT=self.VT[0:len(self.VT)]
		 Aux.VT=self.VN[0:len(self.VN)]
		 # Aux.VT=self.PrimeroSet[0:len(self.PrimeroSet)]
		 # Aux.VT=self.SiguienteSet[0:len(self.SiguienteSet)]

		 Prods=[]
		 for P in self.Productions:
		 	Prods.append(P.copy())
		 Aux.Productions=Prods

		 ja=[]
		 for P in self.ProdsJoined:
		 	ja.append(P.copy())
		 Aux.ProdsJoined=ja
		 return Aux



		

	def onlyOneNTinLeft(self):

		for P in self.Productions:
			if len(P.Left)>1:
				return False
		return True	


	def clear(self):

		
		self.Productions.clear()
		self.VT.clear()
		self.VN.clear()
		self.description=''
		self.ProdsJoined.clear()

	def fromString(input_rules):

		
		lines=input_rules.split('\n')  		# Partimos la entrada en renglones

		for i in range(0,len(lines)):			# Quitamos los espacios al final y principio de cada renglon
			lines[i]=lines[i].strip()

		linesAux=lines.copy()					# removemos las cadenas vacias de la coleccion de cadenas
		lines.clear()
		for line in linesAux:
			if line !='':
				lines.append(line)	

		#self.LOG.debug("Lines content: {} ".format(lines))

		#Errors=False

		myNewGrammar=Grammar()
		myNewGrammar.clear()
		for line in lines:
			processStatus=myNewGrammar.processLine(line)
			if processStatus:
				myNewGrammar.LOG.error(processStatus+' in line {} '.format(lines.index(line)+1))
				return processStatus+' in line {} '.format(lines.index(line)+1)+'\n'
				#Errors=True
				#break
		myNewGrammar.findTermAndNotTerm()
		#if not Errors:

		# for prod in myNewGrammar.Productions:

		# 	for symbol in prod.Left+prod.Right:
		# 		if myNewGrammar.containsTerminal(symbol):
		# 			if symbol not in myNewGrammar.VT: 
		# 				myNewGrammar.VT.append(symbol)

		# 		elif symbol not in myNewGrammar.VN :
		# 				myNewGrammar.VN.append(symbol)
		
		if len(myNewGrammar.Productions)==0:
			return 'Not Sentences were processed, please write some valid sentences  '

		myNewGrammar.Type=myNewGrammar.gramaticType()
		myNewGrammar.description+='VT: '
		myNewGrammar.description+=str(myNewGrammar.VT)+'\n'
		myNewGrammar.description+='VN: '
		myNewGrammar.description+=str(myNewGrammar.VN)+'\n'
		myNewGrammar.description+='S: '+myNewGrammar.Productions[0].Left[0]+'\n'
		myNewGrammar.description+='Type: '+ myNewGrammar.Type

		myNewGrammar.productionsJoin()

		return myNewGrammar

	def findTermAndNotTerm(self):

		for prod in self.Productions:

			for symbol in prod.Left+prod.Right:
				if self.containsTerminal(symbol):
					if symbol not in self.VT: 
						self.VT.append(symbol)

				elif symbol not in self.VN :
						self.VN.append(symbol)

	def productionsJoin(self):
		""" Joins all productions of the same Not Terminal: A->a A->b A->c in one single production 
			with the form  A-> a | b |c"""

		for prod in self.Productions:
				if len(self.ProdsJoined)==0:

					self.ProdsJoined.append(Production(prod.Left[0], [''.join(prod.Right)]))

				else:
					found=False
					for joined in self.ProdsJoined:
						if joined.Left[0]==prod.Left[0]:
							found=True
							joined.Right.append(''.join(prod.Right))
							
					if found==False:
						self.ProdsJoined.append(Production(prod.Left[0], [''.join(prod.Right)]))

			
		print('BEGIN Aqui las factorizadas')
		for prod in self.ProdsJoined:
			# prod.factorize()
			print(prod)



		print('Aqui las factorizadas  END')    



	def containsTerminal(self, strng):
		"""Checks if a string contains at least one terminal symbol"""
		for char in strng:
			if char in Grammar.Terminals and char!='`':   # modified for srtting "`" symbol as not termina
				return True
		return False

	def isPureTerminal(self, strng):

		"""Checks if a string contains only terminal symbols"""
		for c in strng:
			if c not in Grammar.Terminals:
				return False
		return True
		
	def separateOperands(self,line):

		parts=line.split("-->")   	# Separamos la cadena en la dos partes a la derecha y a la izquierda 
									# de la secuencia -->
		
		if len(parts) ==2:          # Formato correcto simbolo --> producto
			
			parts[0]=(parts[0].rstrip()).lstrip()	#se eliminan los espacios al final e inicio de la caddena
			parts[1]=(parts[1].rstrip()).lstrip()	#se eliminan los espacios al final e inicio de la caddena

			if parts[0].find('ϵ')!=-1:
				return 'Left part of the operand contais E (Epsilon) '

			else:
				if parts[1].find('ε')!=-1:
					if len(parts[1])==1:
						return (parts)
					else:
						return 'Sentence not valid, derivations with E (Epsilon) can not contain other characters'		
				else:
					return (parts)

		else:						#la cadena no contiene -->  o se encuentra mas de una vez
			return('Sentence not valid, missing separator "-->" in line ')


	def extractOperands(self,word,symbols):

		#self.LOG.debug('string received as operand {}'.format(word))

		if word!='':
			if word.startswith('<'):
				i=0
				for i in range(1,len(word)): 
					if word[i] =='>':
						symbols.append(word[1:i])
						
						return self.extractOperands(word[i+1:len(word)],symbols)

					elif word[i] not in string.ascii_uppercase and word[i]!='`':  # modified for accepting prime derivations of the kind "E`"
						return 'Delimitated words must only contain UPPERCASE symbols'
					
				return 'Missing delimitator'
			else:
				i=0
				for i in range(0,len(word)):
					if word[i]!='>':
						break
					else:
						return 'Not correctly delimitated operands in '
				if word[i]!=' '	:
					symbols.append(word[i])
				return self.extractOperands(word[i+1:len(word)],symbols)


	def processLine(self,line):

		parts=self.separateOperands(line)

		if type(parts) is list:
			
			#self.LOG.debug('lne: {} was split into {}'.format(line,parts))
			leftSymbols=[]
			result=self.extractOperands(parts[0],leftSymbols)


			if len(leftSymbols) > 0:
				
				if self.isPureTerminal (''.join(leftSymbols))==False:

					rightSymbols=[]
					result=self.extractOperands(parts[1],rightSymbols)
					for var in rightSymbols:
						self.LOG.debug('Right symbols found: {} '.format(var))

					if type(result)!=str:

						self.Productions.append(Production(leftSymbols,rightSymbols))
							
					else:
						return result
				else:
					return 'Pure terminals cannot be on left side '

			else:
				return result

		else:
			return parts

	def gramaticType(self):

		LeftCount=0
		RightCount=0
		AllNotTerminalsInLeft=True
		IsNotTerminalFirstInRight=False
		for prod in self.Productions:
			if len(prod.Left)> LeftCount:
				LeftCount=len(prod.Left)
			if len(prod.Right)> RightCount:
				RightCount=len(prod.Right)

			if len(prod.Left) > len(prod.Right) or 'ε' in prod.Right:
				return 'Unrestricted Grammar'

			if self.containsTerminal(''.join(prod.Left)):
				AllNotTerminalsInLeft=False 

			if self.isPureTerminal(prod.Right[0])==False:
				IsNotTerminalFirstInRight=True

		if LeftCount>1 or AllNotTerminalsInLeft==False or IsNotTerminalFirstInRight==True:
			return 'Context Sensitive Grammar'

		elif RightCount>2 :

				return 'Context Free Grammar'
		return'Regular Grammar'


	def genRegularExpression(self):

		# Step 1: this is already done, we got this in ProdsJoined, so we just copy it
		logStr='Step #1\n\n'
		B=[]
		for production in self.ProdsJoined:
			B.append(production.copy())
			logStr+=(production.__str__()+'\n')
		
		logStr+='\n\n'
		
		# Step2  
		logStr+='Step #2 - Up Iteration\n'
	
		for i in range(0,len(B)-1):
			logStr+=('\ni: '+ str(i)+'	')  
			for strng in B[i].Right:                            # We check for recursivity
				if B[i].Left in strng:  		  				# and make the reducion
					newRight=B[i].Right
					newRight.remove(strng)
					reducedStr='{'+strng.strip(B[i].Left)+'}'
					for k in range(len(newRight)):
						newRight[k]=reducedStr+newRight[k]
					logStr+=('reduced '+B[i].Left+ ' to '+ str(reducedStr)+':	')
					logStr+=(str(B[i])+'')

			for j in range(i+1,len(B)):  
				logStr+=('\n	j: '+str(j)+'')                        	#we check if a substitution can
				newElements=B[j].Right[0:len(B[j].Right)]
				for strng in B[j].Right: 							# be made, and do it if is the case 
					if B[i].Left in strng:	
						newElements.remove(strng)
						for der in B[i].Right:
							# B[j].Right.append(strng.replace(B[i].Left,der))
							newElements.append(strng.replace(B[i].Left,der))
						logStr+=('	replaced '+B[i].Left+ ' on '+ str(B[j].Left)+', '+str(B[j].Left)+' --> '+'	')
						logStr+=(str(newElements)+'')
					else:
						pass
				B[j].Right=newElements


		# Step3
		logStr+='\n\nStep #3 - Down Iteration\n'
	
		for i in reversed(range(len(B))):
			logStr+=('\ni: '+str(i)+'	')
			for strng in B[i].Right:                            # We check for recirsivity
				if B[i].Left in strng:  		  				# and make the reducion
					newRight=B[i].Right
					# newRight.remove(strng)
					reducedStr='{'+strng.strip(B[i].Left)+'}'
					for k in range(len(newRight)):
						newRight[k]=reducedStr+newRight[k]
					logStr+=('reduced '+B[i].Left+ ' to '+ str(reducedStr)+':	')
					logStr+=(str(B[i])+'')
					

			for j in reversed(range(i)):      
				logStr+=('\n	j: '+str(j)+'')                  	#we check if a substitution can
				newElements=B[j].Right[0:len(B[j].Right)]										#be made, and do it if is the case 
				for strng in B[j].Right: 							
					if B[i].Left in strng:	
						newElements.remove(strng)
						for der in B[i].Right:
							# B[j].Right.append(strng.replace(B[i].Left,der))
							newElements.append(strng.replace(B[i].Left,der))
						logStr+=('	replaced '+B[i].Left+ ' on '+ str(B[j].Left)+',  '+str(B[j].Left)+' --> '+'	')
						logStr+=(str(newElements)+'')
					else:
						pass
				B[j].Right=newElements

						

		# Step 4 Reduction

		logStr+='\n\nStep #4 - Simplification\n'
		ER=[]
		for term in B[0].Right:
			index=B[0].Right.index(term)+1
			trimStart=0
			trimEnd=len(term)
			#logStr+=('Term: '+ term)

			while '{' in term or '}'  in term:
				print('im in the loop: '+term)
				#Open=False
				for i in range(len(term)):

					if term[i]=='{':
						trimStart=i
						#Open=True
					if term[i]=='}':
						trimEnd=i
						break

				termX=term[trimStart+1:trimEnd]
				#logStr+=('TermX: '+termX)
				print('TermX: '+termX)
				print('S: '+str(trimStart)+' E: '+str(trimEnd))

				if trimEnd+len(termX) <= len(term) or True:
					print('TemrOr:'+term[trimEnd+1:trimEnd+len(termX)+1])


					if termX== term[trimEnd+1:trimEnd+len(termX)+1]:
						if len(termX)==1:	
							term=term[0:trimStart]+termX+'+'+term[trimEnd+1:trimEnd+len(termX)]+term[trimEnd+len(termX)+1:len(term)]
							logStr+=('\nSimplified Term '+ str(index)+' To: '+ term)
							print('\nSimplified Term '+ str(index)+' To: '+ term)
						else:
							term=term[0:trimStart]+'('+termX+')+'+term[trimEnd+1:trimEnd+len(termX)]+term[trimEnd+len(termX)+1:len(term)]
							logStr+=('\nSimplified Term '+ str(index)+' To: '+ term)
							print('\nSimplified Term '+ str(index)+' To: '+ term)

					elif termX== term[trimStart-len(termX):trimStart]:
						if len(termX)==1:	
							term=term[0:trimStart-len(termX)]+termX+'+'+term[trimEnd+1:trimEnd]+term[trimEnd+1:len(term)]
							logStr+=('\nSimplified Term '+ str(index)+' To: '+ term)
							print('\nSimplified Term '+ str(index)+' To: '+ term)
						else:
							term=term[0:trimStart-len(termX)]+'('+termX+')+'+term[trimEnd+1:trimEnd]+term[trimEnd+1:len(term)]
							logStr+=('\nSimplified Term '+ str(index)+' To: '+ term)
							print('\nSimplified Term '+ str(index)+' To: '+ term)

					else:
						if len(termX)==1:	
							term=term[0:trimStart]+termX+'*'+term[trimEnd+1:len(term)]
							logStr+=('\nSimplified Term '+ str(index)+' To: '+ term)
							print('\nSimplified Term '+ str(index)+' To: '+ term)
						else:
							term=term[0:trimStart]+'('+termX+')*'+term[trimEnd+1:len(term)]
							logStr+=('\nSimplified Term '+ str(index)+' To: '+ term)
							print('\nSimplified Term '+ str(index)+' To: '+ term)

			ER.append(term)

		return [ER,logStr]			

	def genPostFixed(ER):
		print('ER-----------------:'+ER)
		pF=''
		tope=0
		for i in range(len(ER)):
			
			if i>=tope:	
				
				if ER[i] in string.ascii_lowercase:
					if pF=='': 
						if i+1<len(ER): 
							
							if ER[i+1]=='+':
								pF+=ER[i]+'+'
							elif ER[i+1]=='*':
								pF+=ER[i]+'*'
							else:
								pF+=ER[i]

						else:
							pF+=ER[i]
					else:
						if i+1<len(ER):
							if ER[i+1]=='+':
								pF+=ER[i]+'+·'
							elif ER[i+1]=='*':
								pF+=ER[i]+'*·'
							else:
								pF+=ER[i]+'·'
						else:
							pF+=ER[i]+'·'

				# if ER[i]=='*' and ER[i-1]==')':
				# 	pF+='*·'

				# if ER[i]=='+' and ER[i-1]==')':
				# 	pF+='+·'

				if ER[i]=='(':
					endChar=''
					cont=1
					for j in range(i+1,len(ER)):
						
						if ER[j]=='(':
							cont+=1
						if ER[j]==')':
							cont-=1
							if j+1<len(ER):
								if ER[j+1]=='+':
									endChar='+'
								if ER[j+1]=='*':
									endChar='*'

							if cont==0:
								break
					print('():'+ER[i+1:j])			
					
					if pF!='':
						pF+=Grammar.genPostFixed(ER[i+1:j])+endChar+'·'
						print('hgh')
					else:
						pF+=Grammar.genPostFixed(ER[i+1:j])+endChar
						
					

					# print('j1:'+str(i)+'j2:'+str(j))
					tope=j

				if ER[i]=='|':
					for j in range(i+2,len(ER)):
						if ER[j]==' ':
							break
						if j==len(ER)-1:
							tope=j=len(ER)
							break
					print('|:'+ER[i+1:j])	
					pF+=Grammar.genPostFixed(ER[i+1:j])+'|'
					print('j1:'+str(i+2)+'j2:'+str(j))
					tope=j
					print('PF: '+pF)
		return pF	

	def genTreefromER(RE):
		operands='*|·+'
		Pila=[]
		#RE=Grammar.genRegularExpression()
		PF=Grammar.genPostFixed(RE)
		PF+='#·'
		print(PF)
		for s in PF:
			if s not in operands:
				Pila.append(Tree(s))
			else:
				if s=='*':
					c1=Pila.pop()
					T=Tree('*')
					T.C1=c1
					Pila.append(T)
				if s=='+':
					c1=Pila.pop()
					T=Tree('+')
					T.C1=c1
					Pila.append(T)
				if s=='|':
					c2=Pila.pop()
					c1=Pila.pop()
					T=Tree('|')
					T.C1=c1
					T.C2=c2
					Pila.append(T)
				if s=='·':
					c2=Pila.pop()
					c1=Pila.pop()
					T=Tree('·')
					T.C1=c1
					T.C2=c2
					Pila.append(T)

		print('Pila:\n')
		print(Pila)
		return Pila[0]

	def sustitute(prod,prodList):
		""" Sustitutes a Not Terminal symbol with its derivations when its found
			in an element of the list"""
		print('i Receive')
		print('prod:')
		print(prod)
		print('prodList:')
		print(prodList)
		newList=prodList[0:len(prodList)]
		for strng in prodList: 							
			if prod.Left[0] in strng:	
				newList.remove(strng)
				for der in prod.Right:
					newList.append(strng.replace(prod.Left[0],der))
		print('Result:')
		print (newList)

		return newList



	def KillRecursionOnLeft(self):
		""" Checks for recursion on the left and creates a new production to eliminate recursion """

		if self.onlyOneNTinLeft():
			
			PrimProductions=[]
			for i in range(len(self.ProdsJoined)):
				print('this is i:'+str(i))
				Alphas=[]
				Betas=[]
				Nlist=[]
				NT=self.ProdsJoined[i].Left[0]
				if i==0:
					Nlist=self.ProdsJoined[i].Right
				for j in range (0,i):
					# print(len(self.ProdsJoined))
					# print(str(i)+':'+str(j))
					# print(j==None) 
					Nlist=Grammar.sustitute(self.ProdsJoined[j],self.ProdsJoined[i].Right)
					# print('Nlist after sustitutions')
					# print(Nlist)

				for Deriv in Nlist: 
					if Deriv[0]==NT:
						
						Alphas.append(Deriv.replace(NT,'',1))
					else:
						Betas.append(Deriv)

				if len(Betas)>0 and len(Alphas)>0:   # The production has the form A-> Aα | β otherwise
													 # Nothing is done to the production 
					lAux=[]					 
					for B in Betas:
						lAux.append(B+'<'+NT+'`'+'>')
					self.ProdsJoined[i].Right=lAux[0:len(lAux)]
				
					lAux.clear()
					for A in Alphas:
						lAux.append(A+'<'+NT+'`'+'>')
					lAux.append('ε')
				
					p=Production('<'+NT+'`'+'>', lAux[0:len(lAux)]) 
					PrimProductions.append(p)
			self.ProdsJoined.extend(PrimProductions)
			for V in PrimProductions:
				self.VN.append(V.Left)
			# self.Productions.extend(PrimProductions)
			# self.productionsJoin()
			# self.findTermAndNotTerm()


		


	def leftFactorize(self):

		newProds=[]
		for P in self.ProdsJoined:
			Alpha=Grammar.findLongestFactorOnLeft(P.Right)
			if  Alpha!='':
				Gammas=[]
				Betas=[]
				for prod in P.Right:
					if Alpha in prod:
						newTerm=prod.replace(Alpha,'',1)
						if newTerm=='':
							if 'ε' not in Betas:
								Betas.append('ε')
						else:
							Betas.append(newTerm)

							
					else:
						Gammas.append(prod)
				P.Right=[Alpha+'<'+P.Left+'`'+'>']+Gammas
				newP=Production('<'+P.Left+'`'+'>',Betas) 
				newProds.append(newP)
		self.ProdsJoined.extend(newProds)
		for V in newProds:
			self.VN.append(V.Left)
		# self.Productions.extend(newProds)
		# self.productionsJoin()
		# self.findTermAndNotTerm()





	def findLongestFactorOnLeft(strList):
		""" Receives a list of strings and finds the longest common factor in the left
		part of them, this is the value of return """
		L=sorted(strList,key=len)
		Alpha=''
		descarted=[]

		for i in range(len(L)): #stng in L-descarted:
			for w in reversed(range(len(L[i]))):

				found=False
				for j in range(len(L)): #strng2 in L-descarted:				
					if L[j].find(L[i][0:w])>=0 and j!=i:
						found=True
						break

				if found and len(L[i][0:w])>len(Alpha):
					print('Alpha: '+Alpha)
					print('newAlpha: '+L[i][0:w])
					Alpha=L[i][0:w]
					
					break


		return Alpha

	def Primero(self):
		self.PrimeroSet.clear()
		primero=[]
		for Nt in self.VN:
			prim=self.primeroR(Nt)
			primero.append([[Nt,],prim])
			self.PrimeroSet[Nt]=prim
		print(self.PrimeroSet)
		return primero

		
	

	def primeroR(self, X):
		"""Calculates the set 'First' for a given symbol based on the productions of the Grammar"""
		primero=[]
		if self.isPureTerminal(X):
			return [X]
		else:
			for prod in self.ProdsJoined:
				if prod.Left==X:
					print('its a match: '+ X)
					for derivation in prod.Right: 
						if 'ε'==derivation:
							primero.append('ε')
						elif X not in derivation[0]:
							symbolPrimero=[]
							allEpsilon=True
							for symbol in derivation:
								Aux=self.primeroR(symbol)
								symbolPrimero.extend(Aux)
								if 'ε' not in Aux:
									allEpsilon=False
									break 

							for val in symbolPrimero:
								if val!='ε' and val not in primero:
									primero.append(val)
							if allEpsilon:
								primero.append('ε')							
							
		return primero


	def Siguiente(self):

		self.SiguienteSet.clear()
		for i in range(len(self.VN)):
			if i==0:
				self.SiguienteSet[self.VN[i]]=['$']
			else:
				self.SiguienteSet[self.VN[i]]=[]
		 

		for i in range(len(self.VN)):
			if self.VN[i] not in self.SiguienteSet: #No se ha calculado siguiente para el NT[i]
				self.siguienteR(self.VN[i])


	def siguienteR(self,X):			

		print('Term:'+str(X))
		if X not in self.SiguienteSet or X==self.VN[0]:
			for Prod in self.ProdsJoined:
				for Term in Prod.Right:			
					NTpos= Term.find(X)

					if NTpos!= -1 and  NTpos+len(X)<len(Term) and Term [NTpos+len(X)]!='`':
						sigPos=NTpos+len(X)

						
						A=Prod.Left
						Alpha=Term[NTpos:sigPos]
						B=Term[NTpos:sigPos]
						Betha=Term[sigPos:len(Term)]
						
						sig=[]
						
						if X==self.VN[0] and '$' not in sig:

							sig.append('$')

						if Betha!='': # production with the form A--> αBβ 
							print('Producion type: A->αBβ ')
							print('A:'+A)
							print('Alpha:'+Alpha)
							print('B:'+B)
							print('Betha:'+Betha)

							sig.extend(self.gimmePrim(Betha))

							
							if 'ε' in sig:
								sig.remove('ε')
								if A==self.VN[0]:
									sig.append('$')
								else:
									sig.extend(self.siguienteR(A))
							print('Prim de '+Betha+' = '+str(sig))
							self.SiguienteSet[B]=sig  # Here ends the procedure for this case
							return sig

						else:  # production with the form A-->ab
							print('Producion type: A->αB ')
							print('A:'+A)
							print('Alpha:'+Alpha)
							print('B:'+B)
							print('Betha:'+Betha)
							if A==self.VN[0]:
								sig.append('$')
							else:
								sig.extend(self.siguienteR(A))
							print('Prim de '+Betha+' = '+str(sig))
							self.SiguienteSet[B]=sig
							return sig

		else:
			return self.SiguienteSet[X]														
			


	def gimmePrim(self,Betha):
		"""Finds primero for a string based on the existing primero"""
		print('i receive as β :'+Betha)
		primerosDeI=[]
		prim=[]
		for i in range(len(Betha)):
			if Betha[i]=='`':
				continue
			if self.isPureTerminal(Betha[i]):
				if  Betha[i] not in prim:
					prim.append(Betha[i])
				break
			else:
				X=''
				if i+1 < len(Betha):
					if Betha[i+1]=='`': # prime Not Terminal
						X=Betha[i]+Betha[i+1]
					else:
						X=Betha[i]

				elif Betha[i]!='`':           #normal Not Terminal
					X=Betha[i]
				primerosDeI.append(self.PrimeroSet.get(X))

				if 'ε'  not in primerosDeI:
					break
				# # for s in Aux:
				# # 	if s not in prim:
				# 		prim.append(s)
		print('XXdfX:'+ str(primerosDeI))
		allEpsilon=True	
		for P in primerosDeI:
			if 'ε' not in P:
				allEpsilon=False
			for foo in P:
				if foo not in prim:
					prim.append(foo)
		if not allEpsilon and 'ε' in prim:
			prim.remove('ε')

		print('an d prim of β = '+str(prim))
		return prim


	def Sig(self):

		self.SiguienteSet.clear()
		for i in range(len(self.VN)):
			if i==0:
				self.SiguienteSet[self.VN[i]]=['$']
			else:
				self.SiguienteSet[self.VN[i]]=[]

		modifiedFlag=True
		while modifiedFlag:
			modifiedFlag=False
			for P in self.ProdsJoined:
				for prod in P.Right:
					for i in range(len(prod)) :
						if i+1 < len(prod) and prod[i+1]=='`':
							X=prod[i]+prod[i+1]
						elif prod[i]=='`':							
							continue
						else:
							X=prod[i]

						
						if not self.isPureTerminal(X):
							print('X:'+X)
							sigX=self.SiguienteSet.get(X)
							primK=[]

							if i+len(X)<len(prod):
								Rp=prod[i+len(X):len(prod)]
								print('Rp:'+Rp)

								primK.extend(self.gimmePrim(Rp))	

							else:
								if 'ε'not in sigX:
									primK=['ε']

							for m in primK:
									if m not in sigX and m!='ε':
										sigX.append(m)
										modifiedFlag=True

							print('SetPrim:'+str(primK))

							if 'ε' in primK:
								Aux=self.SiguienteSet.get(P.Left)
								print('Sig '+P.Left+': '+str(Aux)) 
								for a in Aux:
									if a not in sigX:											
										sigX.extend(a)
										modifiedFlag=True
						

	def tabla(self):

		Table={}
		for col in self.VN:
			Table[col]={}

		for col in self.VN:
			for row in self.VT:
				Table[col][row]='--------'	

		# print('Table PrrooodskcfvpasdvjadwlkNVDksdsj')
		# for x in Table:
		# 	print(Table[x])
		# # print(Table)	

		Matrix = [[0 for x in range(len(self.VT))] for y in range(len(self.VN))]

		for produccion in self.ProdsJoined:
			for P in produccion.Right:
				primero=self.gimmePrim(P)
				siguiente=[]
				for pr in primero:
					if self.isPureTerminal(pr) and pr!='ε':
						Matrix[self.VN.index(produccion.Left)][self.VT.index(pr)]=produccion.Left+'->'+P
						Table[produccion.Left][pr]=[produccion.Left,P]

				if 'ε' in primero:
					siguiente=self.SiguienteSet.get(produccion.Left)

					for s in siguiente:
						if self.isPureTerminal(s):
							Matrix[self.VN.index(produccion.Left)][self.VT.index(s)]=produccion.Left+'->'+P
							Table[produccion.Left][s]=[produccion.Left,P]

				if 'ε' in primero and '$' in siguiente:
					Matrix[self.VN.index(produccion.Left)][self.VT.index('$')]=produccion.Left+'->'+P
					Table[produccion.Left]['$']=[produccion.Left,P]
		
		print(Table)

		return Table


	def findSymbols(strng):
		symbols=[]
		for i  in range(len(strng)):			
			if strng[i]!= '`':
				if i+1< len(strng):
					if strng[i+1]=='`':
						symbols.append(strng[i]+strng[i+1])
					else:
						symbols.append(strng[i])
				else:
					symbols.append(strng[i])
		return symbols


	def belongsTo(self,strng):


		self.Primero()
		self.Sig()
		Table=self.tabla()

		Pila=['$',self.VN[0]]
		strng+='$'
		ae=0
		X=Pila[len(Pila)-1]

		logTable=[]

		while X!='$':

			prodEmmited=''
			X=Pila[len(Pila)-1]

			if self.isPureTerminal(X) or X=='$':
				if X==strng[ae]:
					prodEmmited=''
					Pila.pop()
					ae+=1
				else:
					 return False

			else:
				if  X in Table.keys():
					if strng[ae] in Table[X].keys():
						prod=Table[X][strng[ae]][1]
						Pila.pop()
						symbols=Grammar.findSymbols(prod)
						for i in reversed(range(len(symbols))):
							if symbols[i]!='ε':
								Pila.append(symbols[i])
						prodEmmited='->'.join(Table[X][strng[ae]])
					else:
						return False
				else:
					return False
			logRen=[Pila[0:len(Pila)],strng[ae:len(strng)],prodEmmited]
			print(logRen)
			logTable.append(logRen)

		return logTable








		


		










				





















