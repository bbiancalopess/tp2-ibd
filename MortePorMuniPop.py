import pandas as pd
import psycopg2

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

# Consulta para obter Mortalidade Masculina por município por População
query_mortalidade_masculina_pop = """
SELECT nome_municipio, populacao, mortalidade_masculina, 
       (mortalidade_masculina::float / populacao::float) AS mortalidade_masculina_percent
FROM municipios
WHERE mortalidade_masculina IS NOT NULL AND populacao IS NOT NULL
ORDER BY mortalidade_masculina_percent DESC;
"""
df_mortalidade_masculina_pop = executar_consulta(query_mortalidade_masculina_pop, conn)

# Consulta para obter Mortalidade Feminina por município por População
query_mortalidade_feminina_pop = """
SELECT nome_municipio, populacao, mortalidade_feminina,
       (mortalidade_feminina::float / populacao::float)  AS mortalidade_feminina_percent
FROM municipios
WHERE mortalidade_feminina IS NOT NULL AND populacao IS NOT NULL
ORDER BY mortalidade_feminina_percent DESC;
"""
df_mortalidade_feminina_pop = executar_consulta(query_mortalidade_feminina_pop, conn)

# Consulta para obter Mortalidade Total por município por População
query_mortalidade_total_pop = """
SELECT nome_municipio, populacao, mortalidade_geral,
       (mortalidade_geral::float / populacao::float)  AS mortalidade_geral_percent
FROM municipios
WHERE mortalidade_geral IS NOT NULL AND populacao IS NOT NULL
ORDER BY mortalidade_geral_percent DESC;
"""
df_mortalidade_total_pop = executar_consulta(query_mortalidade_total_pop, conn)

# Fechar conexão com o banco de dados
conn.close()

# Exibir resultados
print("Mortalidade Masculina por Município por População")
print(df_mortalidade_masculina_pop)

print("\nMortalidade Feminina por Município por População")
print(df_mortalidade_feminina_pop)

print("\nMortalidade Total por Município por População")
print(df_mortalidade_total_pop)

# # Salvar resultados em arquivos Excel para análise adicional
df_mortalidade_masculina_pop.to_excel("graficos/MortalidadeMasculinaPorMunicipioPorPopulacao.xlsx", index=False)
df_mortalidade_feminina_pop.to_excel("graficos/MortalidadeFemininaPorMunicipioPorPopulacao.xlsx", index=False)
df_mortalidade_total_pop.to_excel("graficos/MortalidadeTotalPorMunicipioPorPopulacao.xlsx", index=False)

print("Resultados salvos em arquivos Excel.")
