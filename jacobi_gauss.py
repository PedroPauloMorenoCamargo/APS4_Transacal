import numpy as np
#Código teve como referência: https://www.quantstart.com/articles/Jacobi-Method-in-Python-and-NumPy/
def jacobi(A,b,N,tol):                                                                                                                                                        
    x = np.zeros(len(A[0]))                                                                                                                                                                   
    D = np.diag(A)
    R = A - np.diagflat(D) 
    i = 2
    j = 1 
    x_antigo = np.copy(x)                                                                                                                                                                      
    for i in range(N):
        x = (b - np.dot(R,x)) / D 
        erro = np.divide(np.subtract(x,x_antigo),x + 1e-30)
        x_antigo = np.copy(x)
        if (max(erro) <0.0000000000000000001):
            break
    return x

def seidel(a,b,N,tol):     
    n = len(a)  
    x = np.zeros(len(a))     
    for ite in range(0,N):
        x_antigo = np.copy(x)
        for i in range(0,n):
            linha  = a[i]
            x[i] = ((b[i]-np.dot(linha,x))/linha[i]) + x[i]
        erro = np.divide(np.subtract(x,x_antigo),x + 1e-30)
        if (max(erro) <tol):
            break
    return x  

