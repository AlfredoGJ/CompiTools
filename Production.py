# -*- coding: utf-8 -*-

class Production:
		"""Class that represents a production of a grammar"""
		Left=[]
		Right=[]
		def __init__(self,left,right):
			self.Left=left
			self.Right=right

		def getLeftPart(self):
			"""Returns the left part of the production"""
			return self.Left
		def getRightPart(self):
			"""Returns the right part of the production"""
			return self.Right

		def Equals(self,other):
			"""Check if this production is equivalent to other production"""
			return self.Left==other.Left and self.Right==other.Right


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
			"""Copy method for the Production object"""

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
			"""Factorizes the production"""

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

		def dotInit(self):	
			"""Returns a production with a dot at the beginning"""		
			c=Production(self.Left[:],self.Right[:])
			c.Right.insert(0,"·")
			# print(c.Right)
			# print(c.Left)
			return c

		def dotAdvance(self):
			"""Returns a production with the dot in the next position"""
			c=Production(self.Left[:],self.Right[:])
			if "·" in c.Right:
				index=c.Right.index("·")
				if index+1<len(c.Right):
					c.Right.insert(index,c.Right[index+1])
					c.Right.pop(index+2)
					# print(c.Right)
					return c

				else:
					print("dot at the end")
					return False


		def dotNextChar(self):
			"""Returns the symbol ath the right of the dot"""
			if "·" in self.Right:
				index=self.Right.index("·")
				if index+1<len(self.Right):
					return self.Right[index+1]
				else:
					return ""
			else:
				return False


		def getDotAlpha(self):
			"""Returns the symbol at the left of the dot"""
			if "·" in self.Right:
				index=self.Right.index("·")
				if index>0:
					return self.Right[index-1]
				else:
					return""
			else:
				return False

		def getDotBetha(self):
			"""Returns the symbol at the second position at the right of the dot"""
			if "·" in self.Right:
				index=self.Right.index("·")
				if index+2<len(self.Right):
					return self.Right[index+2]
				else:
					return ""
			else:
				return False


		def getDotIndex(self):
			"""Returns the index of the dot in the production"""
			if "·" in self.Right:
				return self.Right.index("·")
			else:
				return -1








