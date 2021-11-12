class Ponto:

    """Representa um ponto no espaço. Tem carga, epsilon relativo e condutividade.


    """
    # constantes estáticas de classe
    EPSILON_0 = 8.85 * (10 ** -12)
    COND_VACUO = 0
    COND_AGUA = 0.0000055
    EPSILON_AGUA = 0.0000000007
    COND_PRATA = 63000000
    EPSILON_PRATA = float("inf")
    # fim das constantes estáticas de classe

    def __init__(self, tipo="V", epsilon=EPSILON_0, cond=COND_VACUO, carga=0.0):
        """Construtor da classe Ponto. Por padrão, constrói um ponto de vácuo.

        Tipo pode ser apenas "V" (vácuo), "C" (condutor) ou "I" (isolante). O 
        tipo apenas determina quais os valores padrão que serão aplicados,
        ou seja, o tipo não é armazenado após a criação do objeto Ponto. Se fo-
        rem especificados valores "customizados" para as propriedades do materi-
        al, esses valores especificados serão utilizados.

        A carga padrão sempre é zero (float).

        """
        if tipo not in ("V", "C", "I"):
            raise ValueError(
                'Tipo do ponto no espaço a ser construído é inválido, pode ser apenas "V" (vácuo), "C" (condutor) ou "I" (isolante)')
        elif tipo == "V":
            # valores padrão são iguais ao vácuo
            self.epsilon = epsilon
            self.cond = cond
        elif tipo == "C":
            # se nao foi especificado uma condutividade diferente do padrao, usa o valor predefinido para condutores
            if cond == Ponto.COND_VACUO:
                cond = Ponto.COND_PRATA
            # se nao foi especificado uma permissividade diferente do padrao, usa o valor predefinido para condutores
            if epsilon == Ponto.EPSILON_0:
                epsilon = Ponto.EPSILON_PRATA
        elif tipo == "I":
            # se nao foi especificado uma condutividade diferente do padrao, usa o valor predefinido para isolantes
            if cond == Ponto.COND_VACUO:
                cond = Ponto.COND_AGUA
            # se nao foi especificado uma permissividade diferente do padrao, usa o valor predefinido para isolantes
            if epsilon == Ponto.EPSILON_0:
                epsilon = Ponto.EPSILON_AGUA

        self.carga = carga

    def getPermissividadeRelativa(self):
        """Retorna a permissividade relativa do material"""
        return self.epsilon / Ponto.EPSILON_0

    def isVacuo(self):
        """Em alguns casos, pode ser que desejamos tratar o vácuo de uma forma "especial", essa função
        é útil pra isso."""

        return self.epsilon == Ponto.EPSILON_0 and self.cond == Ponto.COND_VACUO

    def mesmoMaterial(self, outro):
        """Retorna se um ponto é feito do mesmo material que o outro. É preferível
        implementar isso do que o builtin __eq__, pois Ponto não guarda informa-
        ção sobre a posição que está localizado, portanto pontos com propriedades
        idênticas podem ser pontos distintos.
        """
        return isinstance(outro, Ponto) and self.cond == outro.cond and self.epsilon == outro.epsilon
