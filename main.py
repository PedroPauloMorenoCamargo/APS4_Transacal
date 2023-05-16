from funcoesTermosol import *

nn,N,nm,Inc,nc,F,nr,R = importa('entrada.xls')
#Cria os objetos de estudos
nos = cria_nos(nn,N,F)
elementos = cria_elementos(nm,Inc,nos)
#Calcula as Matrizes de Rigidez
for elemento in elementos:
    matriz_rigidez = calcula_matriz_rigidez(elemento)
    elemento.setMatrizRigidez(matriz_rigidez)
#Calcula a matriz de rigidez universal
K_G = matriz_universal(nm,elementos)
print(K_G)

