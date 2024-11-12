import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração do pandas para exibir todas as linhas no terminal
pd.set_option('display.max_rows', None)  # Remove qualquer limitação de exibição de linhas

# Obter o diretório atual onde o script está localizado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Carregar os dados do arquivo CSV (usando caminho relativo)
caminho_base_inventario = os.path.join(diretorio_atual, "BaseInventario.csv")
df = pd.read_csv(caminho_base_inventario)

# Converter todas as descrições para minúsculo (mantendo a comparação case insensitive)
df['Descricao'] = df['Descricao'].str.lower()

# Filtrar para incluir apenas Notebooks
df_notebooks = df[df['Tipo'].str.lower() == "notebook"]

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

# Aplica a função de detecção de anomalias a cada linha
df_notebooks['Anomalia'] = df_notebooks.apply(detectar_anomalias, axis=1)

# Filtra as linhas que possuem anomalias
anomalias = df_notebooks[df_notebooks['Anomalia'].notnull()]

# Exibe as anomalias encontradas
if not anomalias.empty:
    print("\nAnomalias detectadas:")
    print(anomalias[['Descricao', 'NumSerie', 'Anomalia']])
else:
    print("\nNenhuma anomalia detectada.")

# Conta a quantidade de notebooks por descrição (antes do tratamento)
model_counts_before = df_notebooks['Descricao'].value_counts().reset_index()
model_counts_before.columns = ['Descricao', 'Quantidade']
model_counts_before = model_counts_before.sort_values(by='Quantidade', ascending=False)

# Exibe todos os modelos e quantidades antes do tratamento
print("\nModelos de notebooks e suas quantidades (antes do tratamento):")
print(model_counts_before)

# Verificar duplicatas (caso haja inconsistências em NumSerie)
duplicates = df_notebooks[df_notebooks.duplicated(subset='NumSerie', keep=False)]
if not duplicates.empty:
    print("\nModelos com duplicatas:")
    print(duplicates[['Descricao', 'NumSerie']].drop_duplicates())

# while para permitir múltiplas correções manuais
while True:
    palavra_chave = input("\nDigite a palavra-chave do modelo que deseja corrigir (ex: 'g7', 'xps', 'g9') ou 'sair' para finalizar: ").strip().lower()
    
    if palavra_chave == 'sair':
        print("Finalizando a atualização dos dados.")
        break

    # Encontra os modelos que contêm a palavra-chave
    modelos_para_corrigir = df_notebooks[df_notebooks['Descricao'].str.contains(palavra_chave)]

    if modelos_para_corrigir.empty:
        print(f"Nenhum modelo encontrado com a palavra-chave '{palavra_chave}'.")
        continue

    print(f"\nModelos encontrados para a palavra-chave '{palavra_chave}':")
    print(modelos_para_corrigir[['Descricao', 'NumSerie']])

    # Pergunta o novo valor da descrição
    novo_valor = input(f"Digite o novo valor para os modelos encontrados: ").strip()
    
    # Atualiza a base de dados corrigida com o novo valor de descrição
    df_notebooks.loc[df_notebooks['Descricao'].str.contains(palavra_chave), 'Descricao'] = novo_valor
    
    # Pergunta se deseja continuar
    continuar = input("\nDeseja corrigir outro modelo? (sim/não): ").strip().lower()
    
    if continuar != 'sim':
        print("Finalizando a atualização dos dados.")
        break

# Contar a quantidade de notebooks por descrição após o tratamento
model_counts_after = df_notebooks['Descricao'].value_counts().reset_index()
model_counts_after.columns = ['Descricao', 'Quantidade']
model_counts_after = model_counts_after.sort_values(by='Quantidade', ascending=False)

# Exibe todos os modelos e quantidades após o tratamento
print("\nModelos de notebooks e suas quantidades (após o tratamento):")
print(model_counts_after)

# Função para selecionar diretório de destino
def selecionar_diretorio():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    caminho = filedialog.askdirectory()  # Abrir o explorador de arquivos
    return caminho

# Solicitar ao usuário um diretório para salvar o arquivo
diretorio = selecionar_diretorio()

if diretorio:
    caminho_arquivo = os.path.join(diretorio, "BaseInventario_atualizado.csv")
    df_notebooks.to_csv(caminho_arquivo, index=False)
    print(f"\nBase de dados atualizada com sucesso! O arquivo foi salvo em '{caminho_arquivo}'.")
else:
    print("Nenhum diretório selecionado. O arquivo não foi salvo.")
