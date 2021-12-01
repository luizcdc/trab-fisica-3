import matplotlib.pyplot as plt
import numpy as np

def main():
    tam = 1001

    #grid do espaço 2d, de tam//2*-1 a tam//2
    x = np.arange(tam//2*-1,tam//2,tam//10)
    y = np.arange(tam//2*-1,tam//2,tam//10)

    X, Y = np.meshgrid(x, y)

    #direção do vetor no ponto, usar campo_eletrico_pontual
    #u,v = map((X,Y), for each i,j in X -> Space2D.campo_eletrico_pontual(i, j)
    u = 1
    v = 1

    fig, ax = plt.subplots(figsize=(7,7))
    ax.quiver(X,Y,u,v)

    ax.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    main()