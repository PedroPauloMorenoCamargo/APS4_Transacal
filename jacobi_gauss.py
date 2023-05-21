import numpy as np

def jacobi(A,b,N,tol):                                                                                                                                                        
    n = len(A)  
    x = np.zeros((len(A),1))     
    for ite in range(0,N):
        x_antigo = np.copy(x)
        for i in range(0,n):
            linha  = A[i]
            x[i] = ((b[i]-np.dot(linha,x_antigo))/linha[i]) + x[i]
        erro = np.divide(np.subtract(x,x_antigo),x + 1e-30)
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
        erro = np.divide(np.subtract(x,x_antigo),x + 1e-30)
        if (max(erro) <tol):
            break
    return x  

