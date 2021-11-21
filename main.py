from Space2D import Space2D
from Ponto import Ponto


if __name__ == '__main__':
    tam = 1
    while tam % 2:
        try:
            tam = int(input("Tamanho do espaço 2D quadrado (inteiro ímpar): "))
        except ValueError:
            print("\nValor incorreto! Digite um número inteiro ímpar.\n")
            continue

    espaco = Space2D(size=tam)

    entrada = ""
    while entrada != "5":
        entrada = input(f"""
    Tamanho do espaço: {tam}
    Obs: um espaço de tamanho {tam} tem coordenadas de -{tam//2} a {tam//2}.
    
    Menu:
        1 - Desenhar um objeto.
        2 - Inserir uma carga num objeto.
        3 - Inserir uma carga pontual.
        4 - Consultar as informações de um ponto.
        5 - Gerar as visualizações.
        0 - Sair.
        
        Opção: """)
        if entrada == 0:
            break
        elif entrada == 1:
            obj = input(
                "Que objeto deseja inserir? 1 - círculo, 2 - semiplano: ").strip()
            while obj not in ("1", "2"):
                print("Valor inválido.")
                obj = input(
                    "Que objeto deseja inserir? 1 - círculo, 2 - semiplano: ").strip()
            if obj == "1":
                mat = ""
                while mat not in ('V', 'C', 'I'):
                    mat = input(
                        'Tipo do material ("V" para vácuo, "C" para condutor e "I" para isolante): ').strip().upper()
                materiais = {'V': 'vácuo', 'C': 'condutor', 'I': 'isolante'}
                print(f'Material escolhido: {materiais[mat]}.')
                # TODO: implementar material personalizado
                # perguntar epsilon do material do círculo
                # perguntar condutividade do material do círculo
                # perguntar se terá carga no círculo
                # se sim, perguntar o valor da carga
                while True:
                    try:
                        posx = int(input('Coordenada x do círculo: ')
                                   ) + (espaco.size//2)
                        posy = int(input('Coordenada y do círculo: ')
                                   ) + (espaco.size//2)
                        raio_circulo = int(input('Raio do círculo em metros'))
                        if not espaco.validIndex(coord=(posx, posy)):
                            raise ValueError
                        break
                    except ValueError:
                        print('Valores inválidos. Digite novamente.')

                espaco.desenha_circulo(material=Ponto(mat), coord_centro=(
                    posx, posy), raio=raio_circulo)
                # chamar inserir_carga_em_objeto() em um ponto do círculo
            elif obj == "2":
                mat = ""
                while mat not in ('V', 'C', 'I'):
                    mat = input(
                        'Tipo do material ("V" para vácuo, "C" para condutor e "I" para isolante): ').strip().upper()
                materiais = {'V': 'vácuo', 'C': 'condutor', 'I': 'isolante'}
                print(f'Material escolhido: {materiais[mat]}.')
                # TODO: implementar material personalizado
                # perguntar epsilon do material do semiplano
                # perguntar condutividade do material do semiplano
                # perguntar se terá carga no semplano
                # se sim, perguntar o valor da carga
                while True:
                    try:
                        orientacao = input(
                            'Limite do semiplano |V|ertical ou |H|orizontal: ').strip().upper()
                        if orientacao not in ('V', 'H'):
                            raise ValueError
                        else:
                            orientacao = True if orientacao == 'V' else False
                        if orientacao == 'V':
                            lado = input('|E|squerda ou |D|ireita?')
                            if lado not in ('E', 'D'):
                                raise ValueError
                            else:
                                lado = True if lado == 'E' else False
                        elif orientacao == 'H':
                            lado = input('|S|uperior ou |I|nferior?')
                            if lado not in ('S', 'I'):
                                raise ValueError
                            else:
                                lado = True if lado == 'S' else False
                        pos = int(input('Coordenada do limite do semiplano: ')
                                  ) + (espaco.size//2)
                        if not espaco.validIndex(coord=(0, pos)):
                            raise ValueError
                        break
                    except ValueError:
                        print('Valores inválidos. Digite novamente.')
                if not isinstance(lado, bool):
                    lado = True
                espaco.desenha_semiplano(material=Ponto(
                    mat), pos_borda=pos, vertical=orientacao, superior_ou_esquerdo=lado)
                # chamar inserir_carga_em_objeto() em um ponto do círculo

                # perguntar os limites do semiplano
                # chamar desenhar_semiplano()
                # chamar inserir_carga_em_objeto() em um ponto do círculo
                pass
