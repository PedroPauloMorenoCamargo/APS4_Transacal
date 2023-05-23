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
        #Numero do nó
        self.n  = n
        #Posição no eixo cartesiano
        self.x = x
        self.y = y
        #Forças de carregamento aplicadas no nó
        self.Cx = Cx
        self.Cy = Cy
        pass

class Elemento:
    def __init__(self,n,no1,no2,E,A) -> None:
        #Número do Elemento
        self.n = n
        self.no1 = no1
        self.no2 = no2
        self.E = E
        #Area
        self.A = A
        #Comprimento
        self.L = sqrt(((no2.x-no1.x)**2+(no2.y-no1.y)**2))
        #Matriz de rigidez inicidada como Null
        self.matriz_rigidez = None
        pass
    #Define preenche o argumento da matriz de rigidez
    def setMatrizRigidez(self,matriz_rigidez):
        self.matriz_rigidez = matriz_rigidez
        return

def get_lista_deformacoes_forcas_tensoes(U2,elementos):
    #Listas que serão guardadas
    deformacoes = np.zeros((len(elementos),1))
    tensoes = np.zeros((len(elementos),1))
    forcas = np.zeros((len(elementos),1))
    #Array suporte que esta no produto escalar da equação
    array_suporte = np.zeros(4)
    for i in range(0,len(elementos)):
        #Seno e cosseno
        s = (elementos[i].no2.y-elementos[i].no1.y)/elementos[i].L
        c = (elementos[i].no2.x-elementos[i].no1.x)/elementos[i].L
        #Pega os index do no1 e no 2 e põe eles na posição relativa
        index1 = elementos[i].no1.n*2
        index2 = elementos[i].no2.n*2
        #Calcula o Vetor [u1,v1,u2,v2]
        U2_aux = np.array([[U2[index1-2]],[U2[index1-1]], [U2[index2-2]],[U2[index2-1]]])
        #Calcula o array suporte
        array_suporte = [-c,-s,c,s]
        #Calcula a deformação
        deformacao = np.dot(array_suporte,U2_aux)  * (1/elementos[i].L)
        deformacoes[i] = deformacao[0]
        #Calcula tensao
        tensoes[i] = (deformacao[0]*elementos[i].E)
        #Calcula forca
        forcas[i] = (deformacao[0]*elementos[i].E*elementos[i].A)
    
    return deformacoes,tensoes,forcas

def get_matriz_universal(nn,nm,elementos):
    #Cria matriz universal
    K_G = np.zeros((nn*2,nn*2))
    #Loopa por cada elemento
    for elemento in elementos:
        #Pega o maior e menor indexes e põe eles em sua posição relativa
        index1 = min(elemento.no1.n,elemento.no2.n)*2
        index2 = max(elemento.no1.n,elemento.no2.n)*2
        lista = [index1-2, index1-1, index2-2,index2-1]
        #Loopa pelo tamanho da matriz de rigidez de uma trelica
        const = (elemento.E * elemento.A)/ elemento.L
        for i in range(0,4):
            for j in range(0,4):
                #Adiciona na posição certa da matriz universal a matriz de rigidez
                K_G[lista[i]][lista[j]] += const*elemento.matriz_rigidez[i][j]
    return K_G
def cria_nos(nn,N,F):
    lista_nos = np.zeros(nn,dtype=Node)
    #Cria os nos
    for i in range(0,nn):
        no = Node(i+1,N[0][i],N[1][i],F[2*i][0],F[2*i +1][0])
        lista_nos[i] = no
    return lista_nos

def cria_elementos(nm,Inc,lista_nos):
    lista_elementos = np.zeros(nm,dtype=Elemento)
    #Cria os elementos
    for i in range(0,nm):
        no1 = lista_nos[int(Inc[i][0]-1)]
        no2 =lista_nos[int(Inc[i][1]-1)]
        elemento = Elemento(i+1,no1,no2,Inc[i][2],Inc[i][3])
        lista_elementos[i] = elemento
    return lista_elementos

def calcula_matriz_rigidez(elemento):
    #Calcula seno
    s = (elemento.no2.y-elemento.no1.y)/elemento.L
    #Calcula cosseno
    c = (elemento.no2.x-elemento.no1.x)/elemento.L
    #Calcula matriz rigida
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
    f = open(nome,"w+")
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
    


