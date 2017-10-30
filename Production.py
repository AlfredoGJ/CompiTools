# -*- coding: utf-8 -*-

class Production:
		Left=[]
		Right=[]
		def __init__(self,left,right):
			self.Left=left
			self.Right=right

		def getLeftPart(self):
			return self.Left
		def getRightPart(self):
			return self.Right

		def __str__(self):
			string=''
			for  var in self.Left:
				string+='"'+var+'" '
			string+='-->'

			for  var in self.Right:
				if type(var)==list:
					for unit in var:
						string+='"'+str(unit)+'" '	
					string+="|"		
				else:	
					string+='"'+var+'" '
			return string
			
		def copy(self):

			if type(self.Left)!=list:
				if type(self.Right)!=list:
					return Production(self.Left,self.Right)
				else:
					return Production(self.Left,self.Right[:])
			else:
				if type(self.Right)!=list:
					return Production(self.Left[:],self.Right[:])	
					
				else:			
					return Production(self.Left[:],self.Right)
			
		def factorize(self):

			factors=[]
			common=[]
 			
			A=self.Left[0]
			for P in self.Right:
				if A in P:
					factors.append(P.replace(A,''))
					common.append(P)

			for c in common:
				if c in self.Right:
					self.Right.remove(c)


			print(factors)

			if len(factors)>=2:
				self.Right.append(''+' | '.join(factors)+' '+A)

			if len(factors)==1:
				self.Right.append(factors[0]+A)





