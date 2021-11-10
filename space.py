from _typeshed import ReadableBuffer
from typing import Tuple
from point import Ponto


class Space2D:
    def __init__(self, size: int = 1001):
        self.size = size
        self.points = []
        for i in range(size):
            self.points.append([])
            for j in range(size):
                # inicializa tudo como se fosse vacuo
                self.points.append(Ponto())

    def relativeIndex(self, base: int, offset: int):
        return (base+offset) % self.size

    def retornaObjeto(self, coord_inicial: Tuple, pontos_integrantes: set[Tuple] = set()):
        # retorna todos os pontos que fazem parte do mesmo objeto que o ponto inicial
        # ex: a partir de qualquer ponto de um circulo, retorna todos os pontos do circulo
        x, y = coord_inicial
        pontoInicial = self.points[x][y]
        if len(pontos_integrantes) == 0:
            if pontoInicial.isVacuo():
                return pontos_integrantes
            else:
                pontos_integrantes.add((coord_inicial))
        for i in range(-1, 2):
            for j in range(-1, 2):
                xv = self.relativeIndex(x, i)
                yv = self.relativeIndex(y, j)
                vizinho = self.points[xv][yv]
                if (xv, yv) not in pontos_integrantes and pontoInicial.mesmoMaterial(vizinho):
                    pontos_integrantes.add((xv, yv))
                    pontos_integrantes = pontos_integrantes.union(self.retornaObjeto(
                        (xv, yv), pontos_integrantes))
        return pontos_integrantes

    def retornaPontosSuperficiais(self, coord_inicial: Tuple, pontos_integrantes: set[Tuple] = None):
        # retorna todos os pontos superficiais de um objeto partindo de qualquer ponto do objeto
        pontos_integrantes = self.retornaObjeto(coord_inicial)
        pontos_de_superficie = set()
        if len(pontos_integrantes) == 0:
            # caso o ponto inicial seja vácuo
            return pontos_integrantes
        for coord_ponto in pontos_integrantes:
            ehSuperficie = False
            x, y = coord_ponto
            ponto = self.points[x][y]
            for i in range(-1, 2):
                if (ehSuperficie):
                    break
                for j in range(-1, 2):
                    xv = self.relativeIndex(x, i)
                    yv = self.relativeIndex(y, j)
                    vizinho = self.points[xv][yv]
                    if not ponto.mesmoMaterial(vizinho):
                        pontos_de_superficie.add((xv, yv))
                        ehSuperficie = True
                        break
        return pontos_de_superficie
