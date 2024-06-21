import pandas as pd
import psycopg2
import os

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

# Consulta para obter Mortalidade Masculina por mesorregião em relação à população
query_mortalidade_masculina_pop = """
SELECT m.nome_mesorregiao, 
       SUM(mu.mortalidade_masculina) AS mortalidade_masculina_total,
       SUM(mu.populacao) AS populacao_total,
       (SUM(mu.mortalidade_masculina)::float / SUM(mu.populacao)::float) AS mortalidade_masculina_percent
FROM municipios mu
JOIN mesorregioes m ON mu.id_mesorregiao = m.id
WHERE mu.mortalidade_masculina IS NOT NULL AND mu.populacao IS NOT NULL
GROUP BY m.nome_mesorregiao
ORDER BY mortalidade_masculina_percent DESC;
"""
df_mortalidade_masculina_pop = executar_consulta(query_mortalidade_masculina_pop, conn)

# Consulta para obter Mortalidade Feminina por mesorregião em relação à população
query_mortalidade_feminina_pop = """
SELECT m.nome_mesorregiao, 
       SUM(mu.mortalidade_feminina) AS mortalidade_feminina_total,
       SUM(mu.populacao) AS populacao_total,
       (SUM(mu.mortalidade_feminina)::float / SUM(mu.populacao)::float) AS mortalidade_feminina_percent
FROM municipios mu
JOIN mesorregioes m ON mu.id_mesorregiao = m.id
WHERE mu.mortalidade_feminina IS NOT NULL AND mu.populacao IS NOT NULL
GROUP BY m.nome_mesorregiao
ORDER BY mortalidade_feminina_percent DESC;
"""
df_mortalidade_feminina_pop = executar_consulta(query_mortalidade_feminina_pop, conn)

# Consulta para obter Mortalidade Total por mesorregião em relação à população
query_mortalidade_total_pop = """
SELECT m.nome_mesorregiao, 
       SUM(mu.mortalidade_geral) AS mortalidade_geral_total,
       SUM(mu.populacao) AS populacao_total,
       (SUM(mu.mortalidade_geral)::float / SUM(mu.populacao)::float) AS mortalidade_geral_percent
FROM municipios mu
JOIN mesorregioes m ON mu.id_mesorregiao = m.id
WHERE mu.mortalidade_geral IS NOT NULL AND mu.populacao IS NOT NULL
GROUP BY m.nome_mesorregiao
ORDER BY mortalidade_geral_percent DESC;
"""
df_mortalidade_total_pop = executar_consulta(query_mortalidade_total_pop, conn)

# Fechar conexão com o banco de dados
conn.close()

# Exibir resultados
print("Mortalidade Masculina por Mesorregião em relação à População")
print(df_mortalidade_masculina_pop)

print("\nMortalidade Feminina por Mesorregião em relação à População")
print(df_mortalidade_feminina_pop)

print("\nMortalidade Total por Mesorregião em relação à População")
print(df_mortalidade_total_pop)

# Criar a pasta "graficos" se não existir
if not os.path.exists("graficos"):
    os.makedirs("graficos")

# Salvar resultados em arquivos Excel para análise adicional
df_mortalidade_masculina_pop.to_excel("graficos/MortalidadeMasculinaPorMesorregiaoPorPopulacao.xlsx", index=False)
df_mortalidade_feminina_pop.to_excel("graficos/MortalidadeFemininaPorMesorregiaoPorPopulacao.xlsx", index=False)
df_mortalidade_total_pop.to_excel("graficos/MortalidadeTotalPorMesorregiaoPorPopulacao.xlsx", index=False)

print("Resultados salvos em arquivos Excel na pasta 'graficos'.")
