import graphviz as gv
import string


class Graph:
    Nodes = []
    Edges = []
    start = ''
    end = ''
    symbols=[]

    GraphStyle = {
        'graph': {
            'fontsize': '32',
            'fontcolor': 'white',
            'bgcolor': '#333333',
            'rankdir': 'LR',
        },
        'nodes': {
            'fontname': 'Helvetica',
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
            'fontsize': '28',
            'fontcolor': '#dabded',
        }}

    def __init__(self):
        self.Nodes = []
        self.Edges = []
        self.start = ''
        self.end = ''
        self.symbols=[]

    def apply_styles(graph):
        graph.graph_attr.update(
            ('graph' in Graph.GraphStyle and Graph.GraphStyle['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in Graph.GraphStyle and Graph.GraphStyle['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in Graph.GraphStyle and Graph.GraphStyle['edges']) or {}
        )
        return graph

    def print(self, name):

        g1 = gv.Digraph(format='png')

        for i in range(len(self.Nodes)):
            if type(self.Nodes[i]) is list:
                g1.node(str(i),string.ascii_uppercase[i]+'\n'+str(self.Nodes[i]))

            else:
                g1.node(self.Nodes[i])

        for edge in self.Edges:
            g1.edge(edge[0], edge[1], edge[2])

        Graph.apply_styles(g1) 

        filename = g1.render(filename='img/' + name)
       
        return filename

    def TRAN(c):
        if len(c) > 1:
            return False
        else:
            result = Graph()

            result.Nodes = ['i', 'f']
            result.Edges = [[result.Nodes[0], result.Nodes[1], c]]
            result.start = result.Nodes[0]
            result.end = result.Nodes[1]
        return result

    def CAT(g1, g2):

        result = Graph()
        G1 = g1.copy()
        G2 = g2.copy()
        markdG2 = []

        for i in range(len(G1.Nodes)):
            print('Hallo:' + str(i))
            if G1.Nodes[i] == 'i':
                result.Nodes.append('i')
            else:
                result.Nodes.append(str(i))

        for e in G1.Edges:
            if e[0] == 'f':
                e[0] = str(len(G1.Nodes) - 1)
            if e[1] == 'f':
                e[1] = str(len(G1.Nodes) - 1)
            result.Edges.append(e)

        for j in range(len(G2.Edges)):
            if G2.Edges[j][0] == 'i':
                G2.Edges[j][0] = str(len(G1.Nodes) - 1)
                markdG2.append(str(j) + '0')
            if G2.Edges[j][1] == 'i':
                G2.Edges[j][1] = str(len(G1.Nodes) - 1)
                markdG2.append(str(j) + '1')

        for i in range(len(G2.Nodes)):

            if G2.Nodes[i] is not 'f' and G2.Nodes[i] is not 'i':
                result.Nodes.append(str(len(G1.Nodes) + i - 1))

                for j  in range(len(G2.Edges)):

                    if G2.Edges[j][0] == G2.Nodes[i] and str(j) + '0' not in markdG2:
                        G2.Edges[j][0] = str(len(G1.Nodes) + i - 1)
                        markdG2.append(str(j) + '0')
                    if G2.Edges[j][1] == G2.Nodes[i] and str(j) + '1' not in markdG2:
                        G2.Edges[j][1] = str(len(G1.Nodes) + i - 1)
                        markdG2.append(str(j) + '1')
                    print('e-Index')
                    print(j)

        result.Nodes.append('f')

        for e in G2.Edges:
            result.Edges.append(e)
        print('markedIndexes:')
        print(markdG2)
        return result

    def OR(g1, g2):

        G1 = g1.copy()
        G2 = g2.copy()
        result = Graph()
        nodeCont = 0
        markdG2 = []
        markdG1 = []
        iVar1 = ''
        fVar1 = ''
        iVar2 = ''
        fVar2 = ''

        result.Nodes.append('i')
        for i in range(len(G1.Nodes)):
            print('i2:' + str(i))
            nodeCont += 1
            if G1.Nodes[i] == 'i':
                iVar1 = str(nodeCont)
            if G1.Nodes[i] == 'f':
                fVar1 = str(nodeCont)
            for j in range(len(G1.Edges)):
                if G1.Nodes[i] == G1.Edges[j][0] and str(j) + str(0) not in markdG1:
                    G1.Edges[j][0] = str(nodeCont)
                    markdG1.append(str(j) + str(0))
                if G1.Nodes[i] == G1.Edges[j][1] and str(j) + str(1) not in markdG1:
                    G1.Edges[j][1] = str(nodeCont)
                    markdG1.append(str(j) + str(1))

            result.Nodes.append(str(nodeCont))

        for e in G1.Edges:
            result.Edges.append(e)

        for i in range(len(G2.Nodes)):
            print('i2:' + str(i))
            nodeCont += 1
            if G2.Nodes[i] == 'i':
                iVar2 = str(nodeCont)
            if G2.Nodes[i] == 'f':
                fVar2 = str(nodeCont)
            for j in range(len(G2.Edges)):
                if G2.Nodes[i] == G2.Edges[j][0] and str(j) + str(0) not in markdG2:
                    G2.Edges[j][0] = str(nodeCont)
                    markdG2.append(str(j) + str(0))
                if G2.Nodes[i] == G2.Edges[j][1] and str(j) + str(1) not in markdG2:
                    G2.Edges[j][1] = str(nodeCont)
                    markdG2.append(str(j) + str(1))

            result.Nodes.append(str(nodeCont))

        for e in G2.Edges:
            result.Edges.append(e)

        print('VARS')
        print(iVar1)
        print(fVar1)
        print(iVar2)
        print(fVar2)
        result.Nodes.append('f')
        result.Edges.append(['i', iVar1, 'ε'])
        result.Edges.append(['i', iVar2, 'ε'])
        result.Edges.append([fVar1, 'f', 'ε'])
        result.Edges.append([fVar2, 'f', 'ε'])

        # for n in G1.Nodes:
        # 	nodeCont+=1
        # 	result.Nodes.append(str(nodeCont))
        # 	for e in G1.Edges:
        # 		if e[0]==n and str(G1.Edges.index(e))+'0'not in markdG1:
        # 			e[0]=str(nodeCont)
        # 			markdG1.append(str(G1.Edges.index(e))+'0')
        # 		if e[1]==n and str(G1.Edges.index(e))+'1'not in markdG1:
        # 			e[1]=str(nodeCont)
        # 			markdG1.append(str(G1.Edges.index(e))+'1')
        # 	if n=='i':
        # 		iVar=str(nodeCont)
        # 	if n=='f':
        # 		fVar=str(nodeCont)



        # for e in G1.Edges:
        # 	result.Edges.append(e)

        # result.Nodes.append('i')
        # result.Nodes.append('f')
        # result.Edges.append(['i',iVar,'ε'])
        # result.Edges.append([fVar,'f','ε'])

        # for n in G2.Nodes:
        # 	nodeCont+=1
        # 	result.Nodes.append(str(nodeCont))
        # 	for e in G2.Edges:
        # 		if e[0]==n and str(G2.Edges.index(e))+'0'not in markdG2:
        # 			e[0]=str(nodeCont)
        # 			markdG2.append(str(G2.Edges.index(e))+'0')
        # 		if e[1]==n and str(G2.Edges.index(e))+'1'not in markdG2:
        # 			e[1]=str(nodeCont)
        # 			markdG2.append(str(G2.Edges.index(e))+'1')
        # 	if n=='i':
        # 		result.Edges.append(['i',str(nodeCont),'ε'])

        # 	if n=='f':
        # 		fVar=str(nodeCont)


        # for e in G2.Edges:
        # 	result.Edges.append(e)



        # result.Edges.append([fVar,'f','ε'])

        return result

    def CERR_POS(g):

        result = Graph()
        G = g.copy()
        nodeCont = 1
        fVar = ''
        iVar = ''
        markdG = []

        result.Nodes.append('i')
        for i  in reversed(range(len(G.Nodes))):
            print('N:' + G.Nodes[i])
            result.Nodes.append(str(nodeCont))
            for e in G.Edges:
                if e[0] == G.Nodes[i] and str(G.Edges.index(e)) + '0' not in markdG:
                    e[0] = str(nodeCont)
                    markdG.append(str(G.Edges.index(e)) + '0')
                if e[1] == G.Nodes[i] and str(G.Edges.index(e)) + '1' not in markdG:
                    e[1] = str(nodeCont)
                    markdG.append(str(G.Edges.index(e)) + '1')
            if G.Nodes[i] == 'i':
                iVar = str(nodeCont)
            if G.Nodes[i] == 'f':
                fVar = str(nodeCont)
                print('fvar: ' + fVar)
                print('count:' + str(nodeCont))
            nodeCont += 1

        result.Edges.append(['i', iVar, 'ε'])

        for e in G.Edges:
            result.Edges.append(e)

        result.Nodes.append('f')
        result.Edges.append([fVar, iVar, 'ε'])
        result.Edges.append([fVar, 'f', 'ε'])
      

        return result

    def CERR_KLEENE(g):

        result = Graph()
        G = g.copy()
        nodeCont = 1
        fVar = ''
        iVar = ''
        markdG = []

        result.Nodes.append('i')
        for i  in reversed(range(len(G.Nodes))):
            print('N:' + G.Nodes[i])
            result.Nodes.append(str(nodeCont))
            for e in G.Edges:
                if e[0] == G.Nodes[i] and str(G.Edges.index(e)) + '0' not in markdG:
                    e[0] = str(nodeCont)
                    markdG.append(str(G.Edges.index(e)) + '0')
                if e[1] == G.Nodes[i] and str(G.Edges.index(e)) + '1' not in markdG:
                    e[1] = str(nodeCont)
                    markdG.append(str(G.Edges.index(e)) + '1')
            if G.Nodes[i] == 'i':
                iVar = str(nodeCont)
            if G.Nodes[i] == 'f':
                fVar = str(nodeCont)
                print('fvar: ' + fVar)
                print('count:' + str(nodeCont))
            nodeCont += 1

        result.Edges.append(['i', iVar, 'ε'])

        for e in G.Edges:
            result.Edges.append(e)

        result.Nodes.append('f')
        result.Edges.append([fVar, iVar, 'ε'])
        result.Edges.append([fVar, 'f', 'ε'])
        result.Edges.append(['i', 'f', 'ε'])

        return result

    def printxt(self):
        print(self.Nodes)
        print(self.Edges)

    def copy(self):
        R = Graph()
        edges = []

        for e in self.Edges:
            edge = []
            for i in e:
                edge.append(i)
            edges.append(edge)
        R.Edges = edges

        for n in self.Nodes:
            R.Nodes.append(n)

        R.start = self.start
        R.end = self.end
        return R

    def fromPostFixed(PF):
        pila = []
        print('I received as PF: ' + PF)
        cont = 1

        for c in PF:
            if c in string.ascii_lowercase or c in string.digits and c != ' ':
                pila.append(Graph.TRAN(c))
                p = pila[len(pila) - 1]
                # p.print(str(cont))
                p.printxt()

            if c == '·':
                op2 = pila.pop()
                op1 = pila.pop()
                pila.append(Graph.CAT(op1, op2))
                p = pila[len(pila) - 1]
                # p.print(str(cont))
                p.printxt()
            if c == '|':
                op2 = pila.pop()
                op1 = pila.pop()
                pila.append(Graph.OR(op1, op2))
                p = pila[len(pila) - 1]
                # p.print(str(cont))
                p.printxt()
            if c == '*':
                op1 = pila.pop()
                pila.append(Graph.CERR_KLEENE(op1))
                p = pila[len(pila) - 1]
                # p.print(str(cont))
                p.printxt()
            if c == '+':
                op1 = pila.pop()
                pila.append(Graph.CERR_POS(op1))
                p = pila[len(pila) - 1]
                # p.print(str(cont))
                p.printxt()

            cont += 1
        pila[0].enlistSymbols()
        return pila[0]



    def cerraduraEpsilon(self, States,accStates):
        # newstates=States[0:len(States)]
        for s in States:
            for e in self.Edges:
                if e[0]==s and e[2]=='ε' and e[1] not in accStates:
                    accStates.append(e[1])
                    self.cerraduraEpsilon([e[1]],accStates)

        # for n in newstates:
        #     if n not in States:
        #         States.append(n)

        return accStates


    def mueve(self, States,Symbol):
        statesList=[]
        for St in States:
            for Ed in self.Edges:
                if Ed[0]==St and Ed[2]==Symbol and Ed[1] not in statesList:
                    statesList.append(Ed[1])
        return statesList

    def enlistSymbols(self ):
        for e in self.Edges:
            if e[2] not in self.symbols and e[2]!='ε':
                self.symbols.append(e[2])

    def getAFDfromAFN(self):
        debugStr=''
        result=Graph()
        States=[]
        markedIndexes=[]
        newEdges=[]

        debugStr+='DEBUGGING FOR THE ALGORITM OF AFD CREATION\n\n'

        States.append(self.cerraduraEpsilon(['i'],['i'] ))

        debugStr+='FIRST STATE: '+ str(States[0])+'\n'
        debugStr+='STATES: '+str(States)+'\n\n\n'


        while len(States)>len(markedIndexes): 
            for i in range(len(markedIndexes),len( States)):
                if i not in markedIndexes:
                    markedIndexes.append(i)
                    debugStr+='\nSet: '+str(States[i])+' Has been Marked!\n'
                    debugStr+='* Generating U for: '+ str(States[i])+'\n'
                    for s in self.symbols:
                        debugStr+='   ---Symbol: '+ s+'\n'
                        U=self.cerraduraEpsilon(self.mueve(States[i],s),self.mueve(States[i],s))
                        debugStr+='     U = '+ str(U)+' --- '
                        if len(U) > 0:
                            if U not in States:
                                debugStr+='U was added to the list as Unmarked\n\n'
                                States.append(U)
                                newEdges.append([str(i),str(len(States)-1),s])
                            else:
                                newEdges.append([str(i),str(States.index(U)),s])
                                debugStr+='U already exist in the list\n\n'
        print('i reach here')
        print(States)
        print(newEdges)
        for i in range(len(States)):
            result.Nodes.append(States[i])

        for e in newEdges :
            result.Edges.append(e)
            result.enlistSymbols()

        return [result,debugStr]


    def minimize(self):
        result=Graph()
        acceptStatesSet=[]
        notAcceptStatesSet=[]
        allSets=[]
        acceptStatesSet.append(-1)
        notAcceptStatesSet.append(-1)
        for i in range(len(self.Nodes)):
            if 'f' in self.Nodes[i]:
                acceptStatesSet.append(str(i))
            else:
                notAcceptStatesSet.append(str(i))

        if len(acceptStatesSet)>1:
            allSets.append(acceptStatesSet)
        if len(notAcceptStatesSet)>1:   
            allSets.append(notAcceptStatesSet)
        print('Initial Sets:'+ str(allSets))


        symbolNumber=len(self.symbols)-1
        print('Symbol number:' + str(symbolNumber))
        symbolIndex=0
        while symbolIndex< symbolNumber:
            for i in range(len(self.symbols)):

                if symbolIndex==-1:
                    symbolIndex=0
                    break
                else:
                    symbolIndex=i
                for Set in allSets:
                    print('Checking '+ self.symbols[i]+' in set: '+ str(Set))
                    newStatesInSet=[]
                    for setIndex in range(1,len(Set)):
                        if len(Set)>2:
                            endGroupIndex=self.toWhichGroup(allSets,Set[setIndex],self.symbols[i])
                            if len(newStatesInSet)==0:
                                newStatesInSet.append([endGroupIndex,Set[setIndex]])
                            else:                 
                                found=False
                                for nSIS in newStatesInSet:
                                    if nSIS[0]==endGroupIndex:
                                        nSIS.append(Set[setIndex])
                                        found=True
                                if found is False:
                                    newStatesInSet.append([endGroupIndex,Set[setIndex]])

            
                    print('Sets generated:'+ str(newStatesInSet))

                    if len(newStatesInSet)>1:
                        allSets.remove(Set)
                        for s in newStatesInSet:
                            allSets.append(s)
                        print('allSets now:'+ str(allSets))
                        symbolIndex=-1
                        break
                print('symbolIndex:'+ str(symbolIndex))


        for i in range(len(allSets)):
            result.Nodes.append(allSets[i][1:len(allSets[i])])
            for S in self.symbols:
                if self.toWhichGroup(allSets,allSets[i][1],S)!= -1:
                    result.Edges.append([str(i),str(self.toWhichGroup(allSets,allSets[i][1],S)),S])

        print(result.Edges)


        print('Final Sets:'+ str(allSets))

        return result


            

    def toWhichGroup(self,sets,state,symbol):
       
       endState=''
       for N in self.Edges:
            if N[0]==state and N[2]== symbol:
                endState=N[1]
       if endState=='':
            return-1

       for i in range(len(sets)):
            if endState in sets[i]:
                return i













