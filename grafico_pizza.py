import pandas as pd
import matplotlib.pyplot as plt
import os

# Obter o diretório atual onde o script está localizado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Carregar os dados das bases CSV (usando caminho relativo)
caminho_base_inventario = os.path.join(diretorio_atual, "BaseInventario.csv")
caminho_base_inventario_pronta = os.path.join(diretorio_atual, "BaseInventario_pronta.csv")

df_original = pd.read_csv(caminho_base_inventario)
df_atualizado = pd.read_csv(caminho_base_inventario_pronta)

# Contar a quantidade de modelos únicos na coluna "Descricao" em cada arquivo
modelos_unicos_original = df_original['Descricao'].nunique()
modelos_unicos_atualizado = df_atualizado['Descricao'].nunique()

# Prepara os dados para o gráfico de pizza
dados = [modelos_unicos_original, modelos_unicos_atualizado]
labels = ['Modelos Originais', 'Modelos Após Tratamento']

# Exibe o gráfico de pizza
plt.figure(figsize=(8, 6))
plt.pie(dados, labels=labels, startangle=140, colors=['#66c2a5', '#fc8d62'], 
        wedgeprops={'edgecolor': 'black'}, autopct=lambda p: f'{int(p/100.*sum(dados))}')  # Mostrar os valores reais
plt.title('Comparativo de Quantidade de Modelos Únicos Antes e Depois do Tratamento')
plt.show()
