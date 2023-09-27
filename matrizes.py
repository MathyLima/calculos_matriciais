import numpy as np
import multiprocessing
import time
#classe para formar as matrizes
class Matriz():
    def __init__(self,*args):
        self._coordenadas = np.asarray(args)
        self._matriz = self.set_matriz
        self._matriz_transposta = self.set_matriz_transposta
        
    
    @property
    def set_matriz(self):
        matriz = np.zeros(self._coordenadas.shape)
        for dimensao in range(self._coordenadas.shape[1]):
            matriz[:,dimensao] = self._coordenadas[:,dimensao]
        return matriz
    @property
    def get_matriz(self):
        return self._matriz
    
    @property
    def set_matriz_transposta(self):
        matriz_inicial = self.get_matriz
        num_linhas = matriz_inicial.shape[0]
        num_colunas = matriz_inicial.shape[1]
        matriz_transposta = np.zeros((num_colunas,num_linhas))
        
        for linha in range(num_colunas):
            matriz_transposta[linha] = matriz_inicial[:,linha]
        
        return matriz_transposta
    
    @property
    def get_matriz_transposta(self):
        return self._matriz_transposta
    
    @property
    def get_ordem(self):
        return self._matriz.shape

    @property
    def get_ordem_transp(self):
        return self._matriz_transposta.shape
    
    
    def multiplicacao_escalar(self,k):
        matriz_resultado = self.get_matriz 
        matriz_resultado *= k
        return Matriz(*matriz_resultado)        
# #Classe que tem como objetivo conter as operações matriciais

class Calculo_Matriz():
    def __init__(self,*args):
        self.lista_matrizes = args
        self.shapes = self.get_shapes
    
    @property
    def get_shapes(self):
        shapes = []
        for i in self.lista_matrizes:
            shapes.append(i.get_ordem)
        return shapes
        
    @property
    def compare_shapes(self):
        first_shape = self.shapes[0]
        for shape in self.shapes:
            if shape != first_shape:
                return False
        return True
    
    @property
    def get_matrizes(self):
        for matriz in self.lista_matrizes:
            print(matriz.get_matriz)
    @property
    def sum(self):
        if self.compare_shapes:
            result = self.lista_matrizes[0].get_matriz
            for matriz in self.lista_matrizes[1:]:
                result += matriz.get_matriz
            return Matriz(*result) #retornando result como um novo objeto Matriz
        else:
            raise ValueError("Matrizes com diferentes tamanhos")
    
    def multiplica(self,matriz1,matriz2,resultado,row_start,row_end):
        for i in range(row_start,row_end):
            for j in range(matriz2.get_ordem[1]):
                resultado[i][j]= sum(matriz1.get_matriz[i][k] * matriz2.get_matriz[k][j] for k in range(matriz1.get_ordem[1]))
    
    def multiplica_matrizes_processos(self,matriz1,matriz2,num_processos):
        '''
            Com o uso do multiprocessing, podemos contornar as limitações do GIL, que  é o mecanismo de controle de concorrencia
        do python, foi projetado para facilitar a programação multithreading, mas impõe algumas limitações quando envolve grande uso de processamento
        , como é o caso de multiplicações matriciais.
        
            Utilizando multiprocessing, podemos criar varios processos, que são instâncias independentes de um programa em execução no sistema operacional,
        isso implica que cada processo possui um endereço e espaço de memória e podem ser executados de forma paralela
        
            Cada prcesso pode ter uma ou mais threads'''
        if matriz1.get_ordem[1] != matriz2.get_ordem[0]:
            raise ValueError("Número de colunas da primeira matriz difere do numero de linhas da segunda")
        resultado = np.zeros((matriz1.get_ordem[0],matriz2.get_ordem[1]))
        step = matriz1.get_ordem[0]//num_processos
        
        processos=[]
        for i in range(num_processos):
            row_start = i * step
            row_end = (i+1)* step if i < num_processos -1 else matriz1.get_ordem[0]
            processo = multiprocessing.Process(target=self.multiplica,args=(matriz1,matriz2,resultado,row_start,row_end))
            processos.append(processo)
            processo.start()
        for processo in processos:
            processo.join()
        
        return Matriz(*resultado)

def criar_matriz_aleatoria():
    return np.random.rand(1000, 1000)

# Criar matrizes aleatórias 1000x1000
matrizAlet1=criar_matriz_aleatoria()
matrizAlet2 = criar_matriz_aleatoria()
matriz1 = Matriz(*matrizAlet1)
matriz2 = Matriz(*matrizAlet2)
# matriz1 = Matriz([1, 2], [4, 5])
# matriz2 = Matriz([5, 6], [7, 8])

num_processos = 10  # Número de processos a serem utilizadas

calculadora = Calculo_Matriz(matriz1,matriz2)
inicio = time.time()
resultado = calculadora.multiplica_matrizes_processos(matriz1, matriz2, num_processos)
fim = time.time()


print("Tempo de execução:", fim - inicio, "segundos")

# matriz3 = Matriz([9, 10], [11, 12])
# matriz4 = Matriz([13,14],[15,16])
# calculadora = Calculo_Matriz(matriz1,matriz2,matriz3,matriz4)

# try:
#     resultado = calculadora.sum
#     print("Soma das matrizes:")
#     print(resultado.get_matriz)
# except ValueError as e:
#     print(e)
