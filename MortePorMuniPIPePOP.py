import pandas as pd
import psycopg2
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def conectar_bd():
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='0828',
        dbname='tp2_ibd',
        port="5432"
    )
    return connection

# Função para executar uma consulta SQL e retornar os resultados como um DataFrame
def executar_consulta(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    colnames = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(rows, columns=colnames)

# Conectar ao banco de dados
conn = conectar_bd()

# Consulta para obter Mortalidade Total por município em relação ao PIB e População
query_mortalidade_total_pib_pop = """
SELECT nome_municipio, pib, populacao, mortalidade_geral,
       (mortalidade_geral::float / populacao::float) AS mortalidade_geral_percent
FROM municipios
WHERE mortalidade_geral IS NOT NULL AND pib IS NOT NULL AND populacao IS NOT NULL
ORDER BY mortalidade_geral_percent DESC;
"""
df_mortalidade_total_pib_pop = executar_consulta(query_mortalidade_total_pib_pop, conn)

# Fechar conexão com o banco de dados
conn.close()

# Exibir resultados
print("Mortalidade Total por Município em relação ao PIB e População")
print(df_mortalidade_total_pib_pop)

# Criar a pasta "graficos" se não existir
if not os.path.exists("graficos"):
    os.makedirs("graficos")

# Salvar resultados em arquivos Excel para análise adicional
df_mortalidade_total_pib_pop.to_excel("graficos/MortalidadeTotalPorMunicipioPorPIBePop.xlsx", index=False)

print("Resultados salvos em arquivos Excel na pasta 'graficos'.")

# Plotar gráfico de linhas para população, PIB e taxa de mortalidade
fig, ax1 = plt.subplots(figsize=(14, 8))

# Eixo X
indices = range(len(df_mortalidade_total_pib_pop))

# Linha de População
ax1.plot(indices, df_mortalidade_total_pib_pop['populacao'], label='População', color='b')

# Linha de PIB
ax1.plot(indices, df_mortalidade_total_pib_pop['pib'], label='PIB', color='g')

# Configurações do eixo Y à esquerda (População e PIB)
ax1.set_ylabel('População e PIB')
ax1.set_ylim(0, 2500000)
ax1.set_xlabel('Municípios')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax1.tick_params(axis='y', colors='b')

# Segundo eixo Y para a taxa de mortalidade
ax2 = ax1.twinx()
ax2.plot(indices, df_mortalidade_total_pib_pop['mortalidade_geral_percent'], label='Taxa de Mortalidade (%)', color='r')

# Configurações do eixo Y à direita (Taxa de Mortalidade)
ax2.set_ylabel('Taxa de Mortalidade (%)')
ax2.set_ylim(0, 0.02)
ax2.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
ax2.tick_params(axis='y', colors='r')

# Adicionar legendas
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

# Configurar título do gráfico
ax1.set_title('População, PIB e Taxa de Mortalidade por Município')

# Configurar eixos X
ax1.set_xticks(indices)
ax1.set_xticklabels(df_mortalidade_total_pib_pop['nome_municipio'], rotation=90)
ax1.set_xticklabels([])  # Ocultar labels dos municípios

# Ajustar layout e salvar gráfico
fig.tight_layout()
plt.savefig("graficos/Populacao_PIB_TaxaMortalidade.png")

# Mostrar gráfico
plt.show()
