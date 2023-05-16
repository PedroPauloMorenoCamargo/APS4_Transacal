# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xlrd
from math import *
"""
A funcao 'plota' produz um gráfico da estrutura definida pela matriz de nos N 
e pela incidencia Inc.

Sugestao de uso:

from funcoesTermosol import plota
plota(N,Inc)
-------------------------------------------------------------------------------
A funcao 'importa' retorna o numero de nos [nn], a matriz dos nos [N], o numero
de membros [nm], a matriz de incidencia [Inc], o numero de cargas [nc], o vetor
carregamento [F], o numero de restricoes [nr] e o vetor de restricoes [R] 
contidos no arquivo de entrada.

Sugestao de uso:
    
from funcoesTermosol import importa
[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xlsx')
-------------------------------------------------------------------------------
A funcao 'geraSaida' cria um arquivo nome.txt contendo as reacoes de apoio Ft, 
deslocamentos Ut, deformacoes Epsi, forcas Fi e tensoes Ti internas. 
As entradas devem ser vetores coluna.

Sugestao de uso:
    
from funcoesTermosol import geraSaida
geraSaida(nome,Ft,Ut,Epsi,Fi,Ti)
-------------------------------------------------------------------------------

"""
class Node:
    def __init__(self,n, x,y,Cx,Cy) -> None:
        self.n  = n
        self.x = x
        self.y = y
        self.Cx = Cx
        self.Cy = Cy
        pass

class Elemento:
    def __init__(self,no1,no2,E,A) -> None:
        self.no1 = no1
        self.no2 = no2
        self.E = E
        self.A = A
        self.L = sqrt(((no2.x-no1.x)**2+(no2.y-no1.y)**2))
        self.matriz_rigidez = None
        pass
    
    def setMatrizRigidez(self,matriz_rigidez):
        self.matriz_rigidez = matriz_rigidez
        return

def matriz_universal(nm,elementos):
    K_G = np.zeros((nm*2,nm*2))
    for elemento in elementos:
        index1 = min(elemento.no1.n,elemento.no2.n)*2
        index2 = max(elemento.no1.n,elemento.no2.n)*2
        lista = [index1-2, index1-1, index2-2,index2-1]

        for i in range(0,4):
            const = (elemento.E * elemento.A)/ elemento.L
            for j in range(0,4):
                K_G[lista[i]][lista[j]] += const*elemento.matriz_rigidez[i][j]
    return K_G
def cria_nos(nn,N,F):
    lista_nos = []
    for i in range(0,nn):
        no = Node(i+1,N[0][i],N[1][i],F[2*i][0],F[2*i +1][0])
        lista_nos.append(no)
    return lista_nos

def cria_elementos(nm,Inc,lista_nos):
    lista_elementos = []
    for i in range(0,nm):
        no1 = lista_nos[int(Inc[i][0]-1)]
        no2 =lista_nos[int(Inc[i][1]-1)]
        elemento = Elemento(no1,no2,Inc[i][2],Inc[i][3])
        lista_elementos.append(elemento)
    return lista_elementos

def calcula_matriz_rigidez(elemento):
    s = (elemento.no2.y-elemento.no1.y)/elemento.L
    c = (elemento.no2.x-elemento.no1.x)/elemento.L
    mat = [[c**2,c*s,-c**2,-c*s],
            [c*s,s**2,-c*s,-s**2],
            [-c**2,-c*s,c**2,c*s],
            [-c*s,-s**2,c*s,s**2]]
    return mat
def plota(N,Inc):
    # Numero de membros
    nm = len(Inc[:,0])
#    plt.show()
    fig = plt.figure()
    # Passa por todos os membros
    for i in range(nm):
        
        # encontra no inicial [n1] e final [n2] 
        n1 = int(Inc[i,0])
        n2 = int(Inc[i,1])        

        plt.plot([N[0,n1-1],N[0,n2-1]],[N[1,n1-1],N[1,n2-1]],color='r',linewidth=3)


    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    
def importa(entradaNome):
    
    arquivo = xlrd.open_workbook(entradaNome)
    
    ################################################## Ler os nos
    nos = arquivo.sheet_by_name('Nos')
    
    # Numero de nos
    nn = int(nos.cell(1,3).value)
                 
    # Matriz dos nós
    N = np.zeros((2,nn))
    
    for c in range(nn):
        N[0,c] = nos.cell(c+1,0).value
        N[1,c] = nos.cell(c+1,1).value
    
    ################################################## Ler a incidencia
    incid = arquivo.sheet_by_name('Incidencia')
    
    # Numero de membros
    nm = int(incid.cell(1,5).value)
                 
    # Matriz de incidencia
    Inc = np.zeros((nm,4))
    
    for c in range(nm):
        Inc[c,0] = int(incid.cell(c+1,0).value)
        Inc[c,1] = int(incid.cell(c+1,1).value)
        Inc[c,2] = incid.cell(c+1,2).value
        Inc[c,3] = incid.cell(c+1,3).value
    
    ################################################## Ler as cargas
    carg = arquivo.sheet_by_name('Carregamento')
    
    # Numero de cargas
    nc = int(carg.cell(1,4).value)
                 
    # Vetor carregamento
    F = np.zeros((nn*2,1))
    
    for c in range(nc):
        no = carg.cell(c+1,0).value
        xouy = carg.cell(c+1,1).value
        GDL = int(no*2-(2-xouy)) 
        F[GDL-1,0] = carg.cell(c+1,2).value
         
    ################################################## Ler restricoes
    restr = arquivo.sheet_by_name('Restricao')
    
    # Numero de restricoes
    nr = int(restr.cell(1,3).value)
                 
    # Vetor com os graus de liberdade restritos
    R = np.zeros((nr,1))
    
    for c in range(nr):
        no = restr.cell(c+1,0).value
        xouy = restr.cell(c+1,1).value
        GDL = no*2-(2-xouy) 
        R[c,0] = GDL-1


    return nn,N,nm,Inc,nc,F,nr,R

def geraSaida(nome,Ft,Ut,Epsi,Fi,Ti):
    nome = nome + '.txt'
    f = open("saida.txt","w+")
    f.write('Reacoes de apoio [N]\n')
    f.write(str(Ft))
    f.write('\n\nDeslocamentos [m]\n')
    f.write(str(Ut))
    f.write('\n\nDeformacoes []\n')
    f.write(str(Epsi))
    f.write('\n\nForcas internas [N]\n')
    f.write(str(Fi))
    f.write('\n\nTensoes internas [Pa]\n')
    f.write(str(Ti))
    f.close()
    


