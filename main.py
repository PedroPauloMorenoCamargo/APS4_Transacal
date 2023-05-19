from funcoesTermosol import *
from jacobi_gauss import *
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
#Fazer algebra linear
U = np.linalg.solve(K_G,F)
print("Deslocamentos normal: \n",U)
U2 = U
#Colocar o vetor como antigamente para o produto escalar
for i in lista_delecao:
    U2 = np.insert(U2,int(i),0)

R = np.dot(temp,U2)
print("Reacoes de apoio nos nós normal:\n",R)

deformacoes,tensoes,forcas = get_lista_deformacoes_forcas_tensoes(U2,elementos)

print("Deformações normal::\n",deformacoes)

print("Tensões normal:\n",tensoes)

print("Forças Internas normal:\n",forcas)


#Fazer algebra linear
U = jacobi(K_G,F,10000,0.00000001)
print("Deslocamentos jacobi: \n",U)
U2 = U
#Colocar o vetor como antigamente para o produto escalar
for i in lista_delecao:
    U2 = np.insert(U2,int(i),0)

R = np.dot(temp,U2)
print("Reacoes de apoio nos nós jacobi:\n",R)

deformacoes,tensoes,forcas = get_lista_deformacoes_forcas_tensoes(U2,elementos)

print("Deformações jacobi:\n",deformacoes)

print("Tensões jacobi:\n",tensoes)

print("Forças Internas jacobi:\n",forcas)


#Fazer algebra linear
U = seidel(K_G,F,10000,0.00000001)
print("Deslocamentos seidel: \n",U)
U2 = U
#Colocar o vetor como antigamente para o produto escalar
for i in lista_delecao:
    U2 = np.insert(U2,int(i),0)

R = np.dot(temp,U2)
print("Reacoes de apoio nos nós seidel:\n",R)

deformacoes,tensoes,forcas = get_lista_deformacoes_forcas_tensoes(U2,elementos)

print("Deformações seidel:\n",deformacoes)

print("Tensões seidel:\n",tensoes)

print("Forças Internas seidel:\n",forcas)