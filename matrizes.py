import numpy as np


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
                    
    
        
matriz1 = Matriz([1, 2], [4, 5])
matriz2 = Matriz([5, 6], [7, 8])
matriz3 = Matriz([9, 10], [11, 12])
matriz4 = Matriz([13,14],[15,16])
calculadora = Calculo_Matriz(matriz1,matriz2,matriz3,matriz4)

try:
    resultado = calculadora.sum
    print("Soma das matrizes:")
    print(resultado.get_matriz)
except ValueError as e:
    print(e)
