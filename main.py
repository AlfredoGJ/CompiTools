from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix import actionbar
from kivy.uix.boxlayout import BoxLayout
from Production import Production
from Grammar import Grammar
#from Tree import Tree
from Graph import Graph
import logging


class RootWidget(BoxLayout):
    '''This is the class representing your root widget.
       By default it is inherited from BoxLayout,
       you can use any other layout/widget depending on your usage.
    '''

    cont1 = ObjectProperty(None)
    cont2 = ObjectProperty(None)
    action_bar = ObjectProperty(None)
    carousel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.cont1 = actionbar.ContextualActionView(
            action_previous=actionbar.ActionPrevious(title='Go Back'))
        self.cont2 = actionbar.ContextualActionView(
            action_previous=actionbar.ActionPrevious(title='Go Back'))
        

        self.action_bar.bind(on_previous=self.on_previous)
        self.prev_index = 0
        self.from_actionbar = False

    def testStringOnGrammar(self):

        myGrammar=self.extractGrammar()
        if myGrammar:
            myGrammar.VT.append('$')
            result=myGrammar.belongsTo(self.testString.text)
            if result!= False:
                self.logBox.text+='THE STRING CORRESPONDS TO THE GRAMMAR\n\n'
                self.logBox.text+='Pila                             Cadena                            Produccion\n'
                for r in result:

                    self.logBox.text+=str(r[0])+'                          '+str(r[1])+'                         '+str(r[2])+'\n'
            else:
                self.logBox.text+="ERROR\nTHE STRING '"+self.testString.text+"' STRING DOESN'T CORRESPONDS TO THE GRAMMAR\n\n"




    def on_index(self, instance, value):
        if value == 2:
            self.action_bar.add_widget(self.cont2)

        elif value == 1:
            if self.prev_index == 0:
                self.action_bar.add_widget(self.cont1)

            elif not self.from_actionbar:
                try:
                    self.action_bar.on_previous()
                except:
                    pass

        elif self.from_actionbar is False:
                try:
                    self.action_bar.on_previous()
                except:
                    pass

        self.prev_index = value
        self.from_actionbar = False

    def on_previous(self, *args):
        self.from_actionbar = True
        self.carousel.load_previous()

    def insertEpsilon(self):
        self.grammarInput.insert_text('ε')

    def refocusTextInput(self):
        self.grammarInput.focus = True

    def ShowAFN(self):
        AFN=Graph.fromPostFixed(Grammar.genPostFixed(self.regExInputBox.text))
        self.regExImage.source=AFN.print('AFN')
        self.regExImage.reload()
        self.regExCarousel.load_next()

        print('DEBUG')
        for state in AFN.Nodes:
            print('state: '+str(state))
            print(AFN.cerraduraEpsilon([state],[state]))

    def ShowAFD(self):
        AFN=Graph.fromPostFixed(Grammar.genPostFixed(self.regExInputBox.text))
        AFD=AFN.getAFDfromAFN()
        self.logBox.text=AFD[1]
        self.regExImage.source=AFD[0].print('AFD')
        self.regExImage.reload()
        self.regExCarousel.load_next()


    def ShowMinAFD(self):
        AFN=Graph.fromPostFixed(Grammar.genPostFixed(self.regExInputBox.text))
        AFD=AFN.getAFDfromAFN()
        AFDMin=AFD[0].minimize()
        self.regExImage.source=AFDMin.print('MinimizedAFD')
        self.regExImage.reload()
        self.regExCarousel.load_next()

    def regExpressionCopy(self):
        self.regExpression.select_all()
        self.regExpression.copy()
        self.regExpression.select_text(0,0)

    def regExInputBoxTextInput(self):
        print('im getting some text')
        if self.regExInputBox.text!='':
            PF=Grammar.genPostFixed(self.regExInputBox.text)  #Post Fixed Grammar
            self.regExPostFixedBox.text=PF

            AuGrammar='('+self.regExInputBox.text+')#'        #Augmented Grammar

            augPFGrammar=PF+' #·'                             # Augmented PF
            self.regAugmentedBox.text=augPFGrammar
           
            Tree=Grammar.genTreefromER(self.regExInputBox.text)
            self.regExTreeImg.source=Tree.printStart(self.regExInputBox.text,'ERTree')
            self.regExTreeImg.reload()

    def extractGrammar(self):
        self.regExpression.text=''
        self.logBox.text = ''
        self.grammarInfo.text = ''
        if self.grammarInput.text != '':

            myGrammar = Grammar.fromString(self.grammarInput.text)

            if type(myGrammar) is Grammar:

                self.grammarInfo.text = myGrammar.description
                print('Prods')
                for p in myGrammar.Productions:
                    print(p)
                print('Original F')
                for p in myGrammar.ProdsJoined:
                    print(p)
                print('\n')

                if myGrammar.Type == 'Regular Grammar':

                    ER = myGrammar.genReBgularExpression()
                    self.grammarInfo.text += '\nRegular Expresion: S--> ' + ' | '.join(ER[0])
                    self.logBox.text = ER[1]

                    self.regExpression.text=' | '.join(ER[0])
                    print(Grammar.genPostFixed(' | '.join(ER[0])))

                return myGrammar


            else:
                self.logBox.text = myGrammar
                return False

    def showLR1Table(self):
        myGrammar=self.extractGrammar()
        if myGrammar:
            myGrammar.Primero()
            myGrammar.Sig()

            E=myGrammar.Elementos()
            print("These are the Sets")
            for e in E:
                Grammar.printLRElementSet(e)
            
            Gp=myGrammar.copy()
            Gp.Productions.insert(0,Production([Gp.Productions[0].Left[0]+'`'],[Gp.Productions[0].Left[0]]))
            Gp.VT.append('$')

            Table= Gp.LR1Table()

            for el in Table:
                print(el)
                
    def testStringLR1(self):
        myGrammar=self.extractGrammar()
        if myGrammar:
            myGrammar.Primero()
            myGrammar.Sig()
            Gp=myGrammar.copy()
            Gp.Productions.insert(0,Production([Gp.Productions[0].Left[0]+'`'],[Gp.Productions[0].Left[0]]))
            Gp.VT.append('$')
            result=Gp.belongsToLR1(self.testString.text)

            if result!=False:
                for row in result:
                    print(row)

   





    def primUndDemencia(self):
        myGrammar=self.extractGrammar()
        if  myGrammar:

                print('After Killing Recursion On Left: ')
                for p in myGrammar.ProdsJoined:
                    print(p)
                    print('\n')

                p=myGrammar.Primero()
                for var in p:
                    print(var)

                myGrammar.Sig()
                print(myGrammar.SiguienteSet)

                self.logBox.text+='Primero:\n\n'
                for p in myGrammar.PrimeroSet:
                    self.logBox.text+=str(p)+' '+str(myGrammar.PrimeroSet.get(p))+'\n'

                self.logBox.text+='\n'

                self.logBox.text+='Siguiente:\n\n'
                for p in myGrammar.SiguienteSet:
                    self.logBox.text+=str(p)+' '+str(myGrammar.SiguienteSet.get(p))+'\n'

                self.logBox.text+='\n\n\n'
                self.logBox.text+='Tabla:\n\n'
                
                myGrammar.VT.append('$')
                table=myGrammar.tabla()

                self.logBox.text+='              '
                for col in myGrammar.VT:
                    self.logBox.text+=col+'                          '
                self.logBox.text+='\n\n'

                for ren in table: 
                    self.logBox.text+=ren+'      '                   
                    for col in table[ren]:
                        if type (table[ren].get(col)) is list:
                            self.logBox.text+='->'.join(table[ren].get(col))+'                   '
                        else:
                            self.logBox.text+=table[ren].get(col)+'                   '
                         

                    self.logBox.text+=('\n')
                # for t in table:

                #     self.logBox.text+=str(t)+'\n'
       
           

    def testGrammar(self):
        self.leftRecursion.text=''
        self.leftFact.text=''
        self.regExpression.text=''
        self.logBox.text = ''
        self.grammarInfo.text = ''
        if self.grammarInput.text != '':

            myGrammar = Grammar.fromString(self.grammarInput.text)

            if type(myGrammar) is Grammar:

                self.grammarInfo.text = myGrammar.description
                print('Prods')
                for p in myGrammar.Productions:
                    print(p)
                print('Original F')
                for p in myGrammar.ProdsJoined:
                    print(p)
                print('\n')

                print("Test point insertion")
                print(myGrammar.Productions[0].dotNextChar())
                myGrammar.Productions[0].dotInit()

                print("Alpha:")
                print(myGrammar.Productions[0].getDotAlpha())
                print("B:")
                print(myGrammar.Productions[0].dotNextChar())
                print("Betha:")
                print(myGrammar.Productions[0].getDotBetha())
                for i in range(10):

                    myGrammar.Productions[0].dotAdvance()
                    print("Alpha:")
                    print(myGrammar.Productions[0].getDotAlpha())
                    print("B:")
                    print(myGrammar.Productions[0].dotNextChar())
                    print("Betha:")
                    print(myGrammar.Productions[0].getDotBetha())


                if myGrammar.Type == 'Regular Grammar':

                    ER = myGrammar.genRegularExpression()
                    self.grammarInfo.text += '\nRegular Expresion: S--> ' + ' | '.join(ER[0])
                    self.logBox.text = ER[1]
                    for h in ER:
                        print(h)

                    self.regExpression.text=' | '.join(ER[0])
                    print(Grammar.genPostFixed(' | '.join(ER[0])))


                recur=myGrammar.copy()
                recur.KillRecursionOnLeft()

                for p in recur.ProdsJoined:
                    for d in p.Right:
                        self.leftRecursion.text+=str(p.Left)+'-->'+str(d)+'\n'


                factor=myGrammar.copy()
                factor.leftFactorize()

                for p in factor.ProdsJoined:
                    for d in p.Right:
                        self.leftFact.text+=str(p.Left)+'-->'+str(d)+'\n'
                # for p in factor.ProdsJoined:
                #     for d in p.Right:
                #         self.leftRecursion.text+=str(p.Left)+'-->'+str(d)+'\n'




                # myGrammar.leftFactorize()
                # print('After Killing Recursion On Left: ')
                # for p in myGrammar.ProdsJoined:
                #     print(p)
                #     print('\n')

                # p=myGrammar.Primero()
                # for var in p:
                #     print(var)

                # myGrammar.Sig()
                # print(myGrammar.SiguienteSet)
                # myGrammar.VT.append('$')

                # table=myGrammar.tabla()
                # print('tabla')

                # for col in myGrammar.VT:
                #     print(col+'     ')

                # for ren in range(len(table)): 
                #     print(myGrammar.VN[ren])                   
                #     for col in range(len(table[ren])):
                #         print(table[ren][col]+'    ')
                #         print('\n')

                # print(table)






            else:
                self.logBox.text = myGrammar
       



class MainApp(App):
    '''This is the main class of your app.
       Define any app wide entities here.
       This class can be accessed anywhere inside the kivy app as,
       in python::

         app = App.get_running_app()
         print (app.title)

       in kv language::

         on_release: print(app.title)
       Name of the .kv file that is auto-loaded is derived from the name
       of this class::

         MainApp = main.kv
         MainClass = mainclass.kv

       The App part is auto removed and the whole name is lowercased.
    '''

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()

