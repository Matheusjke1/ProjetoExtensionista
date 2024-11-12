import pandas as pd
import matplotlib.pyplot as plt
import os

# Obter o diretório atual onde o script está localizado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Carregar os dados da base CSV (usando caminho relativo)
caminho_base_inventario_pronta = os.path.join(diretorio_atual, "BaseInventario_pronta.csv")
df_atualizado = pd.read_csv(caminho_base_inventario_pronta)

# Função para verificar anomalias
def detectar_anomalias(row):
    descricao = row['Descricao'].lower()
    num_serie = str(row['NumSerie'])
    
    if "dell" in descricao and not (len(num_serie) == 7 and num_serie.isalnum()):
        return "Anomalia: DELL com NumSerie inválido"
    
    if "hp" in descricao and not (num_serie.startswith("BR") and len(num_serie) == 10 and num_serie[2:].isalnum()):
        return "Anomalia: HP com NumSerie inválido"
    
    if "lenovo" in descricao and not (num_serie.startswith("PE") and len(num_serie) == 8 and num_serie[2:].isalnum()):
        return "Anomalia: Lenovo com NumSerie inválido"
    
    if "monitor" in descricao:
        return "Anomalia: Monitor listado como Notebook"
    
    return None

# Função de detecção de anomalias a cada linha
df_atualizado['Anomalia'] = df_atualizado.apply(detectar_anomalias, axis=1)

# Conta as anomalias
anomalias = df_atualizado['Anomalia'].notnull().sum()

# Filtra para incluir apenas Notebooks
df_notebooks = df_atualizado[df_atualizado['Tipo'].str.lower() == "notebook"]

# Verifica duplicatas com base na chave primária
duplicatas = df_notebooks[df_notebooks.duplicated(subset='NumSerie', keep=False)].shape[0]

# Verifica monitores na base de dados errada
monitores_errados = df_atualizado[df_atualizado['Tipo'].str.lower() == "monitor"].shape[0]

# Prepara os dados para o gráfico de barras
categorias = ['Anomalias', 'Notebooks com Duplicata de NumSerie', 'Monitores Errados']
quantidades = [anomalias, duplicatas, monitores_errados]

# Exibir o gráfico de barras
plt.figure(figsize=(8, 6))
plt.bar(categorias, quantidades, color=['#66c2a5', '#fc8d62', '#8c6bb1'])
plt.title('Quantidade de Anomalias, Duplicatas e Monitores Errados')
plt.ylabel('Quantidade')
plt.show()
