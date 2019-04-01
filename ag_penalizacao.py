import numpy as np
from random import random

C = 120
n_obj = 42
peso_unidade = np.array([3, 8, 12, 2, 8, 4, 4, 5, 1, 1, 8, 6, 4, 3, 3, 5, 7, 3, 5, 7, 4, 3, 7, 2, 3, 5, 4, 3, 7, 19, 20, 21, 11, 24, 13, 17, 18, 6, 15, 25, 12, 19])
valor_unidade = np.array([1, 3, 1, 8, 9, 3, 2, 8, 5, 1, 1, 6, 3, 2, 5, 2, 3, 8, 9, 3, 2, 4, 5, 4, 3, 1, 3, 2, 14, 32, 20, 19, 15, 37, 18, 13, 19, 10, 15, 40, 17, 39])

pm = 0.05 # probabilidade de mutacao 
pc = 0.8 # probabilidade de crossover
npop = 100 # tamanho da populacao
geracoes = 500
g = 0
flag = True

peso_total = np.zeros(npop, dtype=int)
valor_total = np.zeros(npop, dtype=int)
filho = np.zeros((npop,n_obj), dtype=int)
best = np.zeros(n_obj + 4, dtype=int)

pai = np.random.choice([0, 1], size=(npop, n_obj))

# geracao dos pais
for j in range(npop):
    flag = True
    while flag:
        for i in range(n_obj):
            peso_total[j] = peso_total[j] + pai[j][i] * peso_unidade[i]
            valor_total[j] = valor_total[j] + pai[j][i] * valor_unidade[i]
        if peso_total[j] > C:
            peso_total[j] = 0
            valor_total[j] = 0
            new = np.random.choice([0, 1], size=(n_obj,))
            for k in range(n_obj):
                pai[j][k] = new[k]
        else:
            flag = False

# seleciona o melhor pai
pos_max = np.argmax(valor_total)
best[0] = g # geracao
best[1] = np.sum(pai, axis = 1)[pos_max] # total de itens na mochila
best[2] = peso_total[pos_max] # peso da mochila
best[3] = valor_total[pos_max] # melhor maximo da mochila
for i in range(4, len(best), 1):
    best[i] = pai[pos_max][i-4]
#print("geracao: " + str(g) + ": ")
#print(pai)
#print("peso: " + str(peso_total))
#print("valor: " + str(valor_total) + "\n\n")

# geracoes
for g in range(1, geracoes + 1, 1):
    # organiza os casais
    pai_selec = np.array([], dtype=int)
    selecao = np.zeros(npop, dtype=int)
    for k in range(npop):
        selecao[k] = random() * valor_total[k]
    #print("selecao: " + str(selecao))
    for j in range(npop):
        pos_max = np.argmax(selecao)
        #print("pos_max: " + str(pos_max))
        for i in range(n_obj):
            new[i] = pai[pos_max][i]
        if j == 0:
            pai_selec = np.hstack((pai_selec, new))
        else:
            pai_selec = np.vstack((pai_selec, new))
        selecao = np.delete(selecao, pos_max)

    # crossover
    for j in range(0, npop - 1, 2):
        if random() < pc:
            corte = round(random() * n_obj)
            for i in range(n_obj):
                if i <= corte:
                    filho[j][i] = pai_selec[j][i]
                    filho[j+1][i] = pai_selec[j+1][i]
                else:
                    filho[j][i] = pai_selec[j+1][i]
                    filho[j+1][i] = pai_selec[j][i]
        else:
            for i in range(n_obj):
                filho[j][i] = pai_selec[j][i]
                filho[j+1][i] = pai_selec[j+1][i]

    # mutacao
    for j in range(npop):
        for i in range(n_obj):
            if random() < pm:
                if filho[j][i] == 1:
                    filho[j][i] = 0
                else:
                    filho[j][i] = 1

    # penaliza os individuos infactiveis
    peso_total = np.zeros(npop, dtype=int)
    valor_total = np.zeros(npop, dtype=int)
    for j in range(npop):
        for i in range(n_obj):
            peso_total[j] = peso_total[j] + filho[j][i] * peso_unidade[i]
            valor_total[j] = valor_total[j] + filho[j][i] * valor_unidade[i]
        if peso_total[j] > C:
            valor_total[j] = 1

    # seleciona o melhor resultado
    pos_max = np.argmax(valor_total)
    if valor_total[pos_max] > best[3]:
        best[0] = g # geracao
        best[1] = np.sum(filho, axis = 1)[pos_max] # total de itens na mochila
        best[2] = peso_total[pos_max] # peso da mochila
        best[3] = valor_total[pos_max] # melhor maximo da mochila
        for i in range(4, len(best), 1):
            best[i] = filho[pos_max][i-4]
    
    #print("geracao: " + str(g) + ": ")
    #print(filho)
    #print("peso: " + str(peso_total))
    #print("valor: " + str(valor_total) + "\n\n")

    pai = filho

print("Melhor solucao: ")
print(best)
