# Simulação SIR
# Gillespie
# Fortaleza-CE Simula para comparar com dados reais com subnotificação de 90%
# -----------------------------------------------------------------------------

import EoN
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np

N = 270000  # População de fortaleza
print('Gerando simulaçao com {} nós'.format(N))
G = nx.fast_gnp_random_graph(N, 5. / (N - 1))

node_attribute_dict = {node: 0.5 + random.random() for node in G.nodes()}
edge_attribute_dict = {edge: 0.5 + random.random() for edge in G.edges()}
nx.set_node_attributes(G, values=node_attribute_dict, name='expose2infect_weight')
nx.set_edge_attributes(G, values=edge_attribute_dict, name='transmission_weight')

H = nx.DiGraph()  # Transmissão espontânea
H.add_node('S')
H.add_edge('E', 'I', rate=0.1809, weight_label='expose2infect_weight')
H.add_edge('I', 'R', rate=0.090)

J = nx.DiGraph()  # Transmissão induzida
J.add_edge(('I', 'S'), ('I', 'E'), rate=0.0933, weight_label='transmission_weight')
IC = defaultdict(lambda: 'S')

for node in range(50):
    IC[node] = 'I'
return_statuses = ('S', 'E', 'I', 'R')
print('Realizando a simulação de Gillespie')
t, S, E, I, R = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses, tmax=float(150))

# Pega dados reais
result = pd.read_csv('arquivos/CovidCE.csv', sep=';')
# print(result)

# print(result.values.transpose()[0])
# print(result.values.transpose()[1])

# ----------------------------------
# Salva dados em csv Simulação_COVID
# ----------------------------------
Ob = np.array(0.065 * (R + I))
Ob = np.around(Ob)
Ob = Ob.astype(int)

Simulacao = {'dias': t, 'Infectados': I, 'Obitos': Ob, 'Confirmados': I + R}

# print(t)

QF = pd.DataFrame(data=Simulacao)
# QF.to_csv('arquivos/SimulacaoCovidCE.csv', index=False, sep=";", decimal=",")

QF['dias'] = QF['dias'].astype(int)
QF['date'] = pd.to_datetime(QF['dias']+18336, unit='d')
QF = QF.set_index(['date'])

tabela = pd.concat([QF.groupby(pd.Grouper(freq='D'))['Obitos'].mean(),
                    QF.groupby(pd.Grouper(freq='D'))['Confirmados'].mean(),
                    QF.groupby(pd.Grouper(freq='D'))['Infectados'].mean()],
                    axis=1, sort=False)
tabela = tabela.dropna()
tabela['Obitos'] = tabela['Obitos'].astype(int)
tabela['Confirmados'] = tabela['Confirmados'].astype(int)
tabela['Infectados'] = tabela['Infectados'].astype(int)

tabela.to_csv('arquivos/SimulacaoCovidCE.csv', sep=';', decimal=',')

print(tabela)

# ----------------------------------
# Plota Simulação
# ----------------------------------

print('Simulação concluida, plotando ...')
# plt.plot(t, S, label='Suscetiveis')
plt.plot(t, E, label='Expostos')
plt.plot(t, I, label='Infectados')
# plt.plot(t, 0.935*R, label='Recuperados')
plt.plot(t, Ob, label='Obitos')
plt.plot(result.values.transpose()[0], result.values.transpose()[1], label='Real_casos', linewidth=4.0)
plt.plot(result.values.transpose()[0], result.values.transpose()[2], label='Real_Obitos', linewidth=4.0)
plt.plot(t, I + R, label='I+R+O')
plt.xlabel('$t$')
plt.ylabel('Simulação')
plt.legend()
plt.show()
