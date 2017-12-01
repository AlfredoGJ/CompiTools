import ply.lex as lex
import ply.yacc as yacc


#---------DECLARACIONES-----------------
num_Lineas=0
num_caracteres=0

#---------OPCIONES Y DEFINICIONES REGULARES--------



#----------ACCIONES---------------------------
num_Lineas+=1
num_caracteres+=1


#---------MAIN Y CODIGO ----------------
lex.lex()
print('Lineas:'+str(num_Lineas))
print('CAracteres:'+str(num_caracteres))