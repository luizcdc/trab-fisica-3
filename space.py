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

    def validIndex(self, coord: tuple):
        return coord[0] >= 0 and coord[0] < self.size and coord[1] >= 0 and coord[1] < self.size

    def retorna_objeto(self, coord_inicial: Tuple, pontos_integrantes: set[Tuple] = set()):
        # retorna todos os pontos que fazem parte do mesmo objeto que o ponto inicial
        # ex: a partir de qualquer ponto de um circulo, retorna todos os pontos do circulo
        x, y = coord_inicial
        pontoInicial = self.points[x][y]
        if len(pontos_integrantes) == 0:
            pontos_integrantes.add((coord_inicial))
        for i in range(-1, 2):
            for j in range(-1, 2):
                xv = x+i
                yv = x+j
                if self.validIndex((xv, yv)):
                    vizinho = self.points[xv][yv]
                    if (xv, yv) not in pontos_integrantes and pontoInicial.mesmoMaterial(vizinho):
                        pontos_integrantes.add((xv, yv))
                        pontos_integrantes = pontos_integrantes.union(self.retorna_objeto(
                            (xv, yv), pontos_integrantes))
        return pontos_integrantes

    def retorna_pontos_superficiais(self, coord_inicial: Tuple, pontos_integrantes: set[Tuple] = None):
        # retorna todos os pontos superficiais de um objeto partindo de qualquer ponto do objeto
        if pontos_integrantes == None:
            pontos_integrantes = self.retorna_objeto(coord_inicial)
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
                    xv = x+i
                    yv = x+j
                    if self.validIndex((xv, yv)):
                        vizinho = self.points[xv][yv]
                        if not ponto.mesmoMaterial(vizinho):
                            pontos_de_superficie.add((xv, yv))
                            ehSuperficie = True
                            break
        return pontos_de_superficie

    def distancia_simples(self, coord_1, coord_2):
        x1, y1 = coord_1
        x2, y2 = coord_2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def desenhaCirculo(self, material: Ponto, coord_centro: Tuple, raio: int):
        x, y = coord_centro
        for i in range(-raio-1, raio+2):
            for j in range(-raio-1, raio+2):
                px, py = x+i, y+j
                if px >= 0 and px < self.size and py >= 0 and py < self.size:
                    if self.distancia_simples(coord_centro, (px, py)) < raio:
                        self.points[x][y] = Ponto(
                            epsilon=material.epsilon, cond=material.cond, carga=material.carga)

                    # para cada ponto, verificar se está dentro do círculo
                    # só usar posições absolutas e não "dar a volta" no espaço

    def inserir_carga_pontual(self, coord: Tuple, carga: float):
        ponto_antigo = self.points[coord[0]][coord[1]]
        self.points[coord[0]][coord[1]] = Ponto(epsilon=ponto_antigo.epsilon,
                                                cond=ponto_antigo.cond,
                                                carga=carga)

    def inserir_carga_em_objeto(self, ponto_inicial: Tuple, carga: float):
        x, y = ponto_inicial
        if self.points[x][y].epsilon == float("inf"):
            # é metal
            borda = self.retorna_pontos_superficiais(
                coord_inicial=ponto_inicial)
            carga_parcial = carga / len(borda)
            for p in borda:
                x, y = p
                self.inserir_carga_pontual(coord=p, carga=carga_parcial)
        elif self.points[x][y].epsilon == Ponto.EPSILON_0:
            # é o vácuo
            self.inserir_carga_pontual(coord=ponto_inicial, carga=carga)
        else:
            # é isolante
            pontos_integrantes = self.retorna_objeto(
                coord_inicial=ponto_inicial)
            carga_parcial = carga / len(pontos_integrantes)
            for p in pontos_integrantes:
                self.inserir_carga_pontual(coord=p, carga=carga_parcial)
