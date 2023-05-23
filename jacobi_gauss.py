import numpy as np


def jacobi(a,b,N,tol):     
    n = len(a)  
    x = np.zeros((len(a),1))
    print(np.linalg.det(a))     
    for ite in range(0,N):
        x_antigo = x.copy()
        for i in range(0,n):
            linha  = a[i]
            x[i] = ((b[i]-np.dot(linha,x_antigo))/linha[i]) + x[i]
        erro = np.divide(np.subtract(x,x_antigo),x + 1e-15)
        if (max(erro) <tol):
            break
    return x  

def seidel(a,b,N,tol):     
    n = len(a)  
    x = np.zeros((len(a),1))     
    for ite in range(0,N):
        x_antigo = np.copy(x)
        for i in range(0,n):
            linha  = a[i]
            x[i] = ((b[i]-np.dot(linha,x))/linha[i]) + x[i]
        erro = np.divide(np.subtract(x,x_antigo),x + 1e-15)
        if (max(erro) <tol):
            break
    return x  

