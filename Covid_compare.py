import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Lê dados reais
result = pd.read_csv('arquivos/CovidCE.csv', sep=';')

# Lê dados da simulação
Simulacao = pd.read_csv('arquivos/SimulacaoCovidCE.csv', decimal=",", sep=";")

# Simulacao = {'dias': t, 'Infectados': I, 'Obitos': Ob, 'Confirmados': I+R}
print(Simulacao)

# Plota dados reais
plt.plot(result.values.transpose()[0], result.values.transpose()[1], label='Real_Confirmados', linewidth=3.0)
plt.plot(result.values.transpose()[0], result.values.transpose()[2], label='Real_Obitos', linewidth=3.0)

# Plota dados da simulação
plt.plot(Simulacao.values.transpose()[0], Simulacao.values.transpose()[1], label='SIM_Obitos', linewidth=1.0)
plt.plot(Simulacao.values.transpose()[0], Simulacao.values.transpose()[2], label='SIM_Confirmados', linewidth=1.0)
plt.plot(Simulacao.values.transpose()[0], Simulacao.values.transpose()[3], label='SIM_Infectados', linewidth=1.0)

plt.xticks(np.arange(0, 150, 4.0))
plt.xlabel('$t$')
plt.ylabel('Simulação')
plt.legend()
plt.tick_params(axis='x', rotation=90)
plt.show()
