from Space2D import Space2D
from Ponto import Ponto


if __name__ == '__main__':
    tam = 2
    while not tam % 2:
        try:
            tam = int(input('Tamanho do espaço 2D quadrado (inteiro ímpar): '))
        except ValueError:
            print('\nValor incorreto! Digite um número inteiro ímpar.\n')
            continue

    espaco = Space2D(size=tam)
    objetos = []
    entrada = ''
    while entrada != '0':
        entrada = input(f"""
    Tamanho do espaço: {tam}
    Obs: um espaço de tamanho {tam}x{tam} tem coordenadas de -{tam//2} a {tam//2}.

    Menu:
        1 - Desenhar um objeto.
        2 - Inserir uma carga num objeto.
        3 - Inserir uma carga pontual.
        4 - Consultar as informações de um ponto.
        5 - Gerar as visualizações.
        0 - Sair.

        Opção: """)

        if entrada == '0':  # OPÇÃO SAIR
            print('Encerrando simulador.')
            break
        elif entrada == '1':  # OPÇÃO DESENHAR OBJETO
            # repete até o usuário escolher 1 ou 2.
            obj = input(
                'Que objeto deseja inserir? 1 - círculo, 2 - semiplano, 0 - cancelar: ').strip()
            while obj not in ('1', '2', '0'):
                print('Valor inválido.')
                obj = input(
                    'Que objeto deseja inserir? 1 - círculo, 2 - semiplano, 0 - cancelar: ').strip()

            if obj == '0':  # repete o menu, cancelando operacao
                continue
            elif obj == '1':  # desenhar circulo
                mat = ''
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
                        raio_circulo = int(
                            input('Raio do círculo em metros: '))
                        if not espaco.validIndex(coord=(posx, posy)):
                            raise ValueError
                        break
                    except ValueError:
                        print('Valores inválidos. Digite novamente.')

                objetos.append(espaco.desenha_circulo(material=Ponto(mat), coord_centro=(
                    posx, posy), raio=raio_circulo))
                # chamar inserir_carga_em_objeto() em um ponto do círculo
            elif obj == '2':  # desenhar semiplano
                mat = ''
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
                        if orientacao == True:
                            lado = input('|E|squerda ou |D|ireita? ')
                            if lado not in ('E', 'D'):
                                raise ValueError
                            else:
                                lado = True if lado == 'E' else False
                        else:
                            lado = input('|S|uperior ou |I|nferior? ')
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
                objetos.append(espaco.desenha_semiplano(material=Ponto(
                    mat), pos_borda=pos, vertical=orientacao, superior_ou_esquerdo=lado))

                # chamar inserir_carga_em_objeto() em um ponto do círculo

                # perguntar os limites do semiplano
                # chamar desenhar_semiplano()
                # chamar inserir_carga_em_objeto() em um ponto do círculo
        elif entrada == '2':  # OPÇÃO INSERIR CARGA EM OBJETO
            try:
                carga = float(
                    input('Digite a carga em Coulombs a ser inserida no objeto: '))
                posx = int(
                    input('Digite a coordenada x de um ponto pertencente ao objeto: ')) + (espaco.size//2)
                posy = int(input(
                    'Digite a coordenada y do ponto pertencente ao objeto: ')) + (espaco.size//2)
                if not espaco.validIndex(coord=(posx, posy)):
                    raise ValueError
            except ValueError:
                print('Valores inválidos. Voltando ao menu.')
                continue
            for o in objetos:
                if (posx, posy) in o:
                    espaco.inserir_carga_em_objeto(
                        pontos_integrantes=o, carga=carga)
                    break

        elif entrada == '3':  # OPÇÃO INSERIR CARGA PONTUAL
            try:
                carga = float(
                    input('Digite a carga em Coulombs a ser inserida no ponto do espaço: '))
                posx = int(
                    input('Digite a coordenada x de um ponto: ')) + (espaco.size//2)
                posy = int(input(
                    'Digite a coordenada y do ponto: ')) + (espaco.size//2)
                if not espaco.validIndex(coord=(posx, posy)):
                    raise ValueError
            except ValueError:
                print('Valores inválidos. Voltando ao menu.')
                continue
            espaco.inserir_carga_pontual(coord=(posx, posy), carga=carga)
        elif entrada == '4':  # OPÇÃO CONSULTAR INFORMAÇÕES DE UM PONTO
            try:
                posx = int(
                    input('Digite a coordenada x de um ponto: ')) + (espaco.size//2)
                posy = int(input(
                    'Digite a coordenada y do ponto: ')) + (espaco.size//2)
                if not espaco.validIndex(coord=(posx, posy)):
                    raise ValueError
            except ValueError:
                print('Valores inválidos. Voltando ao menu.')
                continue
            print()
            print(
                f'Informações do ponto ({posx-(espaco.size//2)},{posy-(espaco.size//2)}):')
            print(espaco.points[posx][posy])
            cargas = espaco.get_todas_as_cargas()
            print(
                f'Força elétrica: {espaco.calcula_forca_eletrica_pontual(coord_ponto=(posx,posy),cargas=cargas)} N')
            print(
                f'Campo elétrico: {espaco.campo_eletrico_pontual(coord_ponto=(posx,posy),cargas=cargas)} N/C')
            print(
                f'Potencial elétrico: {espaco.calcula_potencial_eletrico_pontual(coord_ponto=(posx,posy),cargas=cargas)} V')
            print()
            input("Enter para voltar ao menu principal")
        elif entrada == '5':  # OPÇÃO GERAR VISUALIZAÇÕES
            # TODO: inserir essas funções de gerar visualização aqui
            pass
