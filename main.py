from Space2D import Space2D


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
              """)
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
                # perguntar epsilon do material do círculo
                # perguntar condutividade do material do círculo
                # perguntar se terá carga no círculo
                # se sim, perguntar o valor da carga
                # chamar desenhar_circulo()
                # chamar inserir_carga_em_objeto() em um ponto do círculo
                pass
            elif obj == "2":
                # perguntar epsilon do material do semiplano
                # perguntar condutividade do material do semiplano
                # perguntar se terá carga no semplano
                # se sim, perguntar o valor da carga
                # chamar desenhar_semiplano()
                # chamar inserir_carga_em_objeto() em um ponto do círculo
                pass
