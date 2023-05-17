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
K_G = get_matriz_universal(nm,elementos)
temp = K_G
#Dropar restricoes
F = F.flatten()
cont = 0
lista_delecao = []
for restricao in R:
    F = np.delete(F, int(restricao[0])-cont, 0)
    K_G = np.delete(K_G, int(restricao[0])-cont, 0)
    K_G = np.delete(K_G, int(restricao[0])-cont, 1)
    lista_delecao.append(restricao[0])
    cont+=1

U = np.linalg.solve(K_G,F)
print("Deslocamentos: \n",U)
U2 = U
for i in lista_delecao:
    U2 = np.insert(U2,int(i),0)

R = np.dot(temp,U2)
print("Reacoes de apoio nos nós\n",R)

deformacoes,tensoes,forcas = get_lista_deformacoes_forcas_tensoes(U2,elementos)

print("Deformações:\n",deformacoes)

print("Tensões:\n",tensoes)

print("Forças Internas:\n",forcas)

