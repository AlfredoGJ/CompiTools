import graphviz as gv
class Tree:
	"""Class that represents a binary tree"""
	
	
	symbol=''
	C1=None
	C2=None
	number=-1

	GraphStyle = {
	    'graph': {
	        'fontname': 'Arial',
	        'fontsize': '28',
	        'fontcolor': 'white',
	        'bgcolor': '#333333',
	        'rankdir': 'TB',
	    },
	    'nodes': {
	        'fontname': 'Arial',
	        'fontsize': '28',
	        'fontcolor': 'white',
	        'color': 'white',
	        'style': 'filled',
	        'fillcolor': '#006699',
	    },
	    'edges': {
	        'color': 'white',
	        'arrowhead': 'open',
	        'fontname': 'Arial',
	        'fontsize': '16',
	        'fontcolor': 'purple',
	    }}

    


	def __init__(self, initial):
		"""Class constructor"""
		self.symbol=initial
		#self.C1=Tree
		#self.C2=Tree

	def fill_2(self,c1,c2):
		"""Sets both child nodes of the tree to the tree"""
		self.C1=Tree(c1)
		self.C2=Tree(c2)


	def fill_1(self,c1):
		"""Sets the left child of the tree"""
		self.C1=Tree(c1)


	def printStart(self,caption,name):

		"""Start to printing the tree to an image file"""
		g=gv.Graph(format='png')
		#self.GraphStyle[0]['label']='Nopthing'
		g.graph_attr.update(label=caption)
		cont=[]

		Tree.print_it(self,g,cont)

		Tree.apply_styles(g)

		#print(g.source)

		filename = g.render(filename='img/'+name)
		#print(filename) 
		return filename

		


	def apply_styles(graph):
		"""Apllies the visual style to the graphviz tree"""

		graph.graph_attr.update(('graph' in Tree.GraphStyle and Tree.GraphStyle['graph']) or {})
		graph.node_attr.update(('nodes' in Tree.GraphStyle and Tree.GraphStyle['nodes']) or {})
		graph.edge_attr.update(('edges' in Tree.GraphStyle and Tree.GraphStyle['edges']) or {})
		return graph

		
			
	def printxt(self):
		"""Prints to console the content of the tree"""

		print(self.symbol)
		if self.C1 is not None:
			self.C1.printxt()
		if self.C2 is not None:
			self.C2.printxt()

	def print_it(node, g, cont):
		"""Generates recursively the graphviz graph of the tree"""
		g.node(str(len(cont)),node.symbol)
		node.number=len(cont)
		cont.append('i')
		if node.C1 is not None:
			g.edge(str(node.number),str(len(cont)))
			Tree.print_it(node.C1,g,cont)
		if node.C2 is not None:
			g.edge(str(node.number),str(len(cont)))
			Tree.print_it(node.C2,g,cont)
		

