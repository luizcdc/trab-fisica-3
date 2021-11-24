from typing import Tuple
from Ponto import Ponto
from sys import argv
from functools import reduce
from math import pi as PI
import sys
sys.setrecursionlimit(10000)


class Space2D:
    def __init__(self, size: int = 1001):
        """Construtor da classe Space2D.

        `size` é o tamanho do grid (diâmetro). Por padrão é 1001x1001 pontos.
        """
        self.size = size

        # essa list comprehension aninhada cria uma lista que contém `size` listas
        # com `size` pontos de vácuo cada uma
        self.points = [[Ponto() for _ in range(size)] for _ in range(size)]

    def relativeIndex(self, base: int, offset: int):
        """Calcula o índice relativo caso o offset ultrapasse as extremidades do espaço.

        Ex: para um grid de 1001, um índice base igual a 50 e offset de -200,
        retornaria -150 % 1001 = 851, isto é, 200 posições antes da posição 50
        teríamos a posição 851 (pois o espaço é conectado em suas extremidades).

        Necessário para a simulação do espaço infinito.
        """
        return (base+offset) % self.size

    def validIndex(self, coord: tuple):
        """Verifica se as coordenadas especificadas são válidas, isto é, não ul-
        trapassam as dimensões do grid."""
        return coord[0] >= 0 and coord[0] < self.size and coord[1] >= 0 and coord[1] < self.size

    def retorna_pontos_superficiais(self, pontos_integrantes: set[Tuple]):
        """Retorna todos os pontos que estão na borda de um objeto a partir de um
        ponto qualquer do objeto.

        Um "objeto" nesse caso é uma região contínua do espaço composta por
        pontos do mesmo material. Um ponto na borda de um objeto é um ponto que
        tem ao menos um vizinho que não é do mesmo material.

        Ex: a partir de qualquer ponto de um circulo feito de prata, retorna
        apenas os pontos da circunferência do circulo.
        """

        pontos_de_superficie = set()

        for coord_ponto in pontos_integrantes:
            ehSuperficie = False  # flag para ir para o próximo ponto
            x, y = coord_ponto
            ponto = self.points[x][y]
            ehSuperficie = False
            # para cada vizinho
            for i in range(-1, 2):
                for j in range(-1, 2):
                    xv = x+i
                    yv = x+j
                    if self.validIndex((xv, yv)):
                        vizinho = self.points[xv][yv]
                        if not ponto.mesmoMaterial(vizinho):
                            # se esse ponto tem um vizinho de material diferente,
                            # é um ponto da borda do objeto.
                            pontos_de_superficie.add((x, y))
                            ehSuperficie = True
                            break
                if (ehSuperficie):
                    # encerra o for do i, isto é, não precisa verificar nenhum
                    # outro vizinho, e vai processar o próximo ponto do objeto
                    break
        print(pontos_de_superficie)
        return pontos_de_superficie

    @staticmethod
    def distancia_simples(coord_1: Tuple, coord_2: Tuple):
        """Distância entre dois pontos (passados por coordenada)"""
        x1, y1 = coord_1
        x2, y2 = coord_2
        return Space2D.tamanho_vetor((x2-x1, y2-y1))

    @staticmethod
    def tamanho_vetor(x: Tuple):
        """Tamanho de um vetor"""
        return (x[0]**2 + x[1] ** 2) ** 0.5

    def desenha_circulo(self, material: Ponto, coord_centro: Tuple, raio: int):
        """Insere no espaço um círculo de um determinado material com um
        determinado raio, com seu centro em coord_centro."""
        x, y = coord_centro
        pontos_integrantes = set()
        for i in range(-raio-1, raio+2):
            for j in range(-raio-1, raio+2):
                # varredura de um quadrado de tamanho raio+1 * 2
                px, py = x+i, y+j
                if self.validIndex((px, py)):
                    if Space2D.distancia_simples(coord_centro, (px, py)) <= raio:
                        # se o ponto está dentro do círculo (distância menor que o raio)
                        # substitui ele por um ponto do mesmo material do círculo
                        self.points[px][py].epsilon = material.epsilon
                        self.points[px][py].cond = material.cond
                        pontos_integrantes.add((px, py))
        return pontos_integrantes

    def desenha_semiplano(self, material: Ponto, pos_borda: int, vertical: bool = True, superior_ou_esquerdo: bool = True):
        if (material == None or not self.validIndex((pos_borda, pos_borda))):
            raise ValueError(
                "Valores inválidos passados para desenha_semiplano.")
        pontos_integrantes = set()
        if (superior_ou_esquerdo):
            for x in range(pos_borda+1):
                for y in range(self.size):
                    if (vertical):
                        self.points[x][y].cond = material.cond
                        self.points[x][y].epsilon = material.epsilon
                        pontos_integrantes.add((x, y))
                    else:
                        self.points[y][x].cond = material.cond
                        self.points[y][x].epsilon = material.epsilon
                        pontos_integrantes.add((y, x))
        else:
            for x in range(pos_borda, self.size):
                for y in range(self.size):
                    if (vertical):
                        self.points[x][y].cond = material.cond
                        self.points[x][y].epsilon = material.epsilon
                        pontos_integrantes.add((x, y))
                    else:
                        self.points[y][x].cond = material.cond
                        self.points[y][x].epsilon = material.epsilon
                        pontos_integrantes.add((y, x))
        return pontos_integrantes

    def inserir_carga_pontual(self, coord: Tuple, carga: float):
        """Sem mudar o material de um ponto no espaço, insere uma carga ali."""
        self.points[coord[0]][coord[1]].carga = carga

    def somar_carga_pontual(self, coord: Tuple, carga: float):
        """Sem mudar o material de um ponto no espaço, soma uma carga 
        com a carga existente ali."""
        self.points[coord[0]][coord[1]].carga += carga

    def get_todas_as_cargas(self):
        """Retorna as coordenadas de todos os pontos do espaço que têm qualquer carga."""
        cargas = set()
        for i, row in enumerate(self.points):
            for j, point in enumerate(row):
                if point.carga != 0:
                    cargas.add((i, j))
        return cargas

    def forca_eletrica_entre(self, coord_a: Tuple, coord_b: Tuple):
        """Retorna o vetor da força elétrica que o ponto coord_b exerce no
        ponto coord_a.
        """
        if coord_a == coord_b:
            return (0, 0)

        if not self.validIndex(coord_a) or not self.validIndex(coord_b):
            raise ValueError("Coordenadas passadas para "
                             "forca_eletrica_entre(coord_a, coord_b) "
                             "inválidas.")

        ax, ay = coord_a
        bx, by = coord_b
        carga_a = self.points[ax][ay]
        carga_b = self.points[bx][by]
        v = (ax - bx, ay - by)  # vetor entre as cargas

        dist = Space2D.tamanho_vetor(v)
        v = (v[0]/dist, v[1]/dist)  # transforma no vetor unitário

        # lei de Coulomb
        forca = (1/(4*PI*Ponto.EPSILON_0) *
                 ((carga_a.carga*carga_b.carga)/(dist**2)))

        # vetor da força elétrica referente a carga_a
        v = (v[0]*forca, v[1]*forca)
        return v

    def calcula_forca_eletrica_pontual(self, coord_ponto: Tuple, cargas: set = None):
        """Retorna um vetor que representa a força elétrica resultante
        de todo o espaço naquele ponto.

        O parâmetro 'cargas' pode ser passado opcionalmente para evitar recalcular.
        """
        x, y = coord_ponto
        carga_local = self.points[x][y]
        if carga_local.carga == 0:
            # se aqui não tem carga, nem precisa calcular
            return 0

        if cargas == None:
            # cargas pode ser passado opcionalmente para evitar recalcular
            cargas = self.get_todas_as_cargas()

        # a list comprehension gera o conjunto das forças elétricas independentes
        # atuando sobre a carga, enquanto que reduce faz o somatório dos vetores
        # ao fim retornando o vetor da força resultante
        forca_resultante = reduce(lambda x, y:  (x[0]+y[0], x[1] + y[1]),
                                  (self.forca_eletrica_entre(coord_ponto,
                                                             coord_atual)
                                   for coord_atual in cargas))

        return forca_resultante

    def campo_entre_dois_pontos(self, coord_ponto: Tuple, coord_carga: Tuple):
        if coord_ponto == coord_carga:
            return (0, 0)
        ax, ay = coord_ponto
        bx, by = coord_carga
        carga_b = self.points[bx][by]
        v = (ax - bx, ay - by)  # vetor entre as os pontos

        dist = Space2D.tamanho_vetor(v)
        v = (v[0]/dist, v[1]/dist)  # transforma no vetor unitário

        # fórmula do campo
        campo = (1/(4*PI*Ponto.EPSILON_0) *
                 ((carga_b.carga)/(dist**2)))

        # vetor do campo referente a carga no ponto
        v = (v[0]*campo, v[1]*campo)
        return v

    def campo_eletrico_pontual(self, coord_ponto: Tuple, cargas: set = None):
        x, y = coord_ponto

        if cargas == None:
            # cargas pode ser passado opcionalmente para evitar recalcular
            cargas = self.get_todas_as_cargas()

        # a list comprehension gera o conjunto das forças elétricas independentes
        # atuando sobre a carga, enquanto que reduce faz o somatório dos vetores
        # ao fim retornando o vetor da força resultante
        campo_resultante = reduce(lambda x, y:  (x[0]+y[0], x[1] + y[1]),
                                  [self.campo_entre_dois_pontos(coord_ponto,
                                                                coord_atual)
                                   for coord_atual in cargas], (0, 0))

        return campo_resultante

    def inserir_carga_em_objeto(self, pontos_integrantes: set[tuple[int, int]], carga: float):
        """Insere uma carga num objeto. Se for condutor, distribui igualmente
        por pelos pontos da borda do objeto, se for isolante, distribui igualmente
        por todos os pontos do objeto. Se for vácuo, insere apenas no ponto inicial."""
        x, y = pontos_integrantes.__iter__().__next__()
        if len(pontos_integrantes) != 0:
            if self.points[x][y].epsilon == float("inf"):
                # é metal
                borda = self.retorna_pontos_superficiais(
                    pontos_integrantes=pontos_integrantes)
                carga_parcial = carga / len(borda)
                for p in borda:
                    x, y = p
                    self.somar_carga_pontual(coord=p, carga=carga_parcial)
            elif self.points[x][y].isVacuo():
                # é o vácuo
                self.somar_carga_pontual(coord=(x, y), carga=carga)
            else:
                # é isolante
                carga_parcial = carga / len(pontos_integrantes)
                for p in pontos_integrantes:
                    self.somar_carga_pontual(coord=p, carga=carga_parcial)

    def resetar_carga_em_objeto(self, pontos_integrantes: set[Tuple[int, int]]):
        if len(pontos_integrantes) != 0:
            for p in pontos_integrantes:
                self.inserir_carga_pontual(coord=p, carga=0)

    def campo_e_potencial_relativo(self, ponto: Tuple, carga: Tuple):
        if ponto == carga:
            v = (0, 0)
            pot = 0
        else:
            # vetor entre as os pontos
            v = (ponto[0] - carga[0], ponto[1] - carga[1])

            dist = Space2D.tamanho_vetor(v)
            v = (v[0]/dist, v[1]/dist)  # transforma no vetor unitário

            # fórmula do campo
            campo = (1/(4*PI*Ponto.EPSILON_0) *
                     ((self.points[carga[0]][carga[1]].carga)/(dist**2)))
            # fórmula do potencial
            pot = ((1/(4*PI*Ponto.EPSILON_0) *
                    self.points[carga[0]][carga[1]].carga)/dist)

            # vetor do campo referente a carga no ponto
            v = (v[0]*campo, v[1]*campo)

        return (v, pot)

    def calcular_campo_e_potencial(self, cargas: set = None):
        self.mapa_campo_e_potencial = [
            [((0, 0), 0) for y in range(self.size)] for x in range(self.size)]
        if (cargas == None):
            cargas = self.get_todas_as_cargas()
        for x in range(self.size):
            for y in range(self.size):
                resultado = reduce(lambda x, y:  ((x[0][0]+y[0][0], x[0][1] + y[0][1]), x[1]+y[1]),
                                   (self.campo_e_potencial_relativo((x, y),
                                                                    c)
                                    for c in cargas))
                self.mapa_campo_e_potencial[x][y] = resultado

    def calcula_potencial_eletrico_pontual(self, coord_ponto: tuple[int, int], cargas: set):
        x, y = coord_ponto
        return sum((self.campo_e_potencial_relativo((x, y),
                                                    c)[1]
                    for c in cargas))


def main(argv):
    pass


if __name__ == "__main__":
    main(argv)
