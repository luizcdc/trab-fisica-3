from _typeshed import ReadableBuffer
from typing import Tuple
from point import Point


class Space2D:
    def __init__(self, size=1001):
        self.size = size
        self.points = []
        for i in range(size):
            self.points.append([])
            for j in range(size):
                # inicializa tudo como se fosse vacuo
                self.points.append(Point())

    def relativeIndex(self, base, offset):
        return (base+offset) % self.size

    def retornaObjeto(self, coord_inicial: Tuple, pontos_integrantes=set()):
        # retorna todos os pontos que fazem parte do mesmo objeto que o ponto inicial
        # ex: a partir de qualquer ponto de um circulo, retorna todos os pontos do circulo
        if len(pontos_integrantes) == 0:
            x, y = coord_inicial
            pontoInicial = self.points[x][y]
            if pontoInicial.isVacuo():
                return pontos_integrantes
            else:
                pontos_integrantes.add(pontoInicial)
        for i in range(-1, 2):
            for j in range(-1, 2):
                xv = self.relativeIndex(x, i)
                yv = self.relativeIndex(y, j)
                vizinho = self.points[xv][yv]
                if vizinho not in pontos_integrantes and pontoInicial.mesmoMaterial(vizinho):
                    pontos_integrantes.add(vizinho)
                    pontos_integrantes = pontos_integrantes.union(self.retornaObjeto(
                        (xv, yv), pontos_integrantes))
        return pontos_integrantes
