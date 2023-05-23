from funcoesTermosol import *
from jacobi_gauss import *
nn,N,nm,Inc,nc,F,nr,R = importa('entrada2.xls')
plota(N,Inc)
#Cria os objetos de estudos
nos = cria_nos(nn,N,F)
elementos = cria_elementos(nm,Inc,nos)
#Calcula as Matrizes de Rigidez
for elemento in elementos:
    matriz_rigidez = calcula_matriz_rigidez(elemento)
    elemento.setMatrizRigidez(matriz_rigidez)
#Calcula a matriz de rigidez universal
K_G = get_matriz_universal(nn,nm,elementos)
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
U = jacobi(K_G,F,1000,0.0001)
print(U)
U2 = U
#Colocar o vetor como antigamente para o produto escalar
for i in lista_delecao:
    U2 = np.insert(U2,int(i),0)

cont = 0
Reac = np.dot(temp,U2)
Reacoes_final = np.zeros((len(lista_delecao),1))
cont = 0
for i in range(0,len(Reac)):
    if i in lista_delecao:
        Reacoes_final[cont]  = Reac[i]
        cont+=1
deformacoes,tensoes,forcas = get_lista_deformacoes_forcas_tensoes(U2,elementos)
geraSaida("jacobi",Reacoes_final,U,deformacoes,forcas,tensoes)
#Fazer algebra linear
U = seidel(K_G,F,10000,0.0001)
U2 = U
#Colocar o vetor como antigamente para o produto escalar
for i in lista_delecao:
    U2 = np.insert(U2,int(i),0)

cont = 0
Reac = np.dot(temp,U2)
Reacoes_final = np.zeros((len(lista_delecao),1))
cont = 0
for i in range(0,len(Reac)):
    if i in lista_delecao:
        Reacoes_final[cont]  = Reac[i]
        cont+=1
deformacoes,tensoes,forcas = get_lista_deformacoes_forcas_tensoes(U2,elementos)
geraSaida("Seidel",Reacoes_final,U,deformacoes,forcas,tensoes)

#Fazer algebra linear
U = np.linalg.solve(K_G,F)
U2 = U
#Colocar o vetor como antigamente para o produto escalar
for i in lista_delecao:
    U2 = np.insert(U2,int(i),0)

cont = 0
Reac = np.dot(temp,U2)
Reacoes_final = np.zeros((len(lista_delecao),1))
cont = 0
for i in range(0,len(Reac)):
    if i in lista_delecao:
        Reacoes_final[cont]  = Reac[i]
        cont+=1
deformacoes,tensoes,forcas = get_lista_deformacoes_forcas_tensoes(U2,elementos)
geraSaida("Numpy",Reacoes_final,U,deformacoes,forcas,tensoes)

