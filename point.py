

class Ponto:
    # constantes estáticas de classe
    EPSILON_0 = 8.85 * (10 ** -12)
    COND_VACUO = 0
    COND_AGUA = 0.0000055
    EPSILON_AGUA = 0.0000000007
    COND_PRATA = 63000000
    EPSILON_PRATA = float("inf")
    # fim das constantes estáticas de classe

    def __init__(self, tipo="V", epsilon=EPSILON_0, cond=COND_VACUO, carga=0):
        """Tipo pode ser apenas "V" (vácuo), "C" (condutor) ou "I" (isolante)"""
        if tipo not in ("V", "C", "I"):
            raise ValueError(
                'Tipo do ponto no espaço a ser construído é inválido, pode ser apenas "V" (vácuo), "C" (condutor) ou "I" (isolante)')
        elif tipo == "V":
            # usa valores padrão
            self.epsilon = epsilon
            self.cond = cond
        elif tipo == "C":
            # se nao foi especificado uma condutividade diferente do padrao, usa o valor predefinido para condutores
            if cond == 0:
                cond = Ponto.COND_PRATA  # cond. da prata
            # se nao foi especificado uma permissividade diferente do padrao, usa o valor predefinido para condutores
            if epsilon == Ponto.EPSILON_0:
                epsilon = Ponto.EPSILON_PRATA
        elif tipo == "I":
            # se nao foi especificado uma condutividade diferente do padrao, usa o valor predefinido para isolantes
            if cond == 0:
                cond = Ponto.COND_AGUA  # cond. da agua destilada
            # se nao foi especificado uma permissividade diferente do padrao, usa o valor predefinido para isolantes
            if epsilon == Ponto.EPSILON_0:
                epsilon = Ponto.EPSILON_AGUA
        self.carga = carga

    def getPermissividadeRelativa(self):
        return self.epsilon / Ponto.EPSILON_0

    def getCampoEletrico(self):
        # retornar uma tupla representando o campo eletrico
        pass

    def getPotencialEletrico(self):
        # retornar um escalar
        pass
