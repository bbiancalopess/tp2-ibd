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

# Consulta para obter Mortalidade Geral por mesorregião em relação ao PIB e População
query_mortalidade_geral_pip_pop = """
SELECT m.nome_mesorregiao, 
       SUM(mu.pib) AS pib_total, 
       SUM(mu.populacao) AS populacao_total,
       (SUM(mu.mortalidade_geral)::float / SUM(mu.populacao)::float) AS mortalidade_geral_percent
FROM municipios mu
JOIN mesorregioes m ON mu.id_mesorregiao = m.id
WHERE mu.mortalidade_geral IS NOT NULL AND mu.pib IS NOT NULL AND mu.populacao IS NOT NULL
GROUP BY m.nome_mesorregiao
ORDER BY mortalidade_geral_percent DESC;
"""
df_mortalidade_geral_pip_pop = executar_consulta(query_mortalidade_geral_pip_pop, conn)

# Fechar conexão com o banco de dados
conn.close()

# Exibir resultados
print("Mortalidade Geral por Mesorregião em relação ao PIB e População")
print(df_mortalidade_geral_pip_pop)

# Criar a pasta "graficos" se não existir
if not os.path.exists("graficos"):
    os.makedirs("graficos")

# Salvar resultados em arquivos Excel para análise adicional
df_mortalidade_geral_pip_pop.to_excel("graficos/MortalidadeGeralPorMesorregiaoPorPIBePop.xlsx", index=False)

print("Resultados salvos em arquivos Excel na pasta 'graficos'.")

# Plotar gráfico de linhas para População, PIB e taxa de mortalidade
fig, ax1 = plt.subplots(figsize=(12, 8))

# Eixo X
indices = range(len(df_mortalidade_geral_pip_pop))

# Linha de População
ax1.plot(indices, df_mortalidade_geral_pip_pop['populacao_total'], label='População', color='b')

# Linha de PIB
ax1.plot(indices, df_mortalidade_geral_pip_pop['pib_total'], label='PIB', color='g')

# Configurações do eixo Y à esquerda (População e PIB)
max_left_y = max(df_mortalidade_geral_pip_pop['populacao_total'].max(), df_mortalidade_geral_pip_pop['pib_total'].max())
ax1.set_ylim(0, max_left_y * 1.1)  # Ajuste para dar espaço ao máximo valor
ax1.set_ylabel('População e PIB')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax1.tick_params(axis='y', colors='b')

# Segundo eixo Y para a taxa de mortalidade
ax2 = ax1.twinx()
ax2.plot(indices, df_mortalidade_geral_pip_pop['mortalidade_geral_percent'], label='Taxa de Mortalidade (%)', color='r')

# Configurações do eixo Y à direita (Taxa de Mortalidade)
ax2.set_ylabel('Taxa de Mortalidade (%)')
ax2.set_ylim(0, 0.02)  # Máximo de 2% para a taxa de mortalidade
ax2.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
ax2.tick_params(axis='y', colors='r')

# Adicionar legendas
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

# Configurar título do gráfico
ax1.set_title('População, PIB e Taxa de Mortalidade por Mesorregião')

# Configurar eixos X
ax1.set_xticks(indices)
ax1.set_xticklabels(df_mortalidade_geral_pip_pop['nome_mesorregiao'], rotation=90)
ax1.set_xlabel('Mesorregião')

# Ajustar layout e salvar gráfico
fig.tight_layout()
plt.savefig("graficos/Populacao_PIB_TaxaMortalidade.png")

# Mostrar gráfico
plt.show()
