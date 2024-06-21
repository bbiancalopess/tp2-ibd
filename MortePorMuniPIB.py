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

# Consulta para obter Mortalidade Masculina por município por PIB
query_mortalidade_masculina = """
SELECT nome_municipio, pib, mortalidade_masculina, 
       (mortalidade_masculina::float / populacao::float) AS mortalidade_masculina_percent
FROM municipios
WHERE mortalidade_masculina IS NOT NULL AND pib IS NOT NULL AND populacao IS NOT NULL
ORDER BY mortalidade_masculina_percent DESC;
"""
df_mortalidade_masculina = executar_consulta(query_mortalidade_masculina, conn)

# Consulta para obter Mortalidade Feminina por município por PIB
query_mortalidade_feminina = """
SELECT nome_municipio, pib, mortalidade_feminina,
       (mortalidade_feminina::float / populacao::float)  AS mortalidade_feminina_percent
FROM municipios
WHERE mortalidade_feminina IS NOT NULL AND pib IS NOT NULL AND populacao IS NOT NULL
ORDER BY mortalidade_feminina_percent DESC;
"""
df_mortalidade_feminina = executar_consulta(query_mortalidade_feminina, conn)

# Consulta para obter Mortalidade Total por município por PIB
query_mortalidade_total = """
SELECT nome_municipio, pib, mortalidade_geral,
       (mortalidade_geral::float / populacao::float)  AS mortalidade_geral_percent
FROM municipios
WHERE mortalidade_geral IS NOT NULL AND pib IS NOT NULL AND populacao IS NOT NULL
ORDER BY mortalidade_geral_percent DESC;
"""
df_mortalidade_total = executar_consulta(query_mortalidade_total, conn)

# Fechar conexão com o banco de dados
conn.close()
# Exibir resultados
print("Mortalidade Masculina por Município por PIB")
print(df_mortalidade_masculina)

print("\nMortalidade Feminina por Município por PIB")
print(df_mortalidade_feminina)

print("\nMortalidade Total por Município por PIB")
print(df_mortalidade_total)

# Salvar resultados em arquivos Excel para análise adicional
df_mortalidade_masculina.to_excel("MortalidadeMasculinaPorMunicipioPorPIB.xlsx", index=False)
df_mortalidade_feminina.to_excel("MortalidadeFemininaPorMunicipioPorPIB.xlsx", index=False)
df_mortalidade_total.to_excel("MortalidadeTotalPorMunicipioPorPIB.xlsx", index=False)

print("Resultados salvos em arquivos Excel.")
