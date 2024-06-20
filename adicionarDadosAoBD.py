import pandas as pd
import psycopg2

def conectar_bd():
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='postgres',
        dbname='tp2_ibd',
        port="5432"
    )
    return connection

# Conectar ao banco de dados PostgreSQL
conn = conectar_bd()

# Adiciona extensão que ignora acentos no BD
cursor = conn.cursor()
cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")
conn.commit()

#------------------------------------------------------------------------------------------------------------
#-------------------------------------------CRIA TABELAS-----------------------------------------------------
#------------------------------------------------------------------------------------------------------------

# Caminho para o arquivo SQL
caminho_script_sql = 'creating-db.sql'

# Abrir o arquivo SQL e ler o conteúdo
with open(caminho_script_sql, 'r') as arquivo:
    script_sql = arquivo.read()

# Executar o script SQL
cursor = conn.cursor()
cursor.execute(script_sql)
conn.commit()

#------------------------------------------------------------------------------------------------------------
#-------------------------------------------INSERE MESORREGIOES----------------------------------------------
#------------------------------------------------------------------------------------------------------------
# Ler o arquivo xlsx
xlsx_file = 'mesorregioes.xlsx'
df_meso = pd.read_excel(xlsx_file)

# Passo 2: Obter valores únicos usando um set
valores_unicos = set(df_meso[df_meso.columns[0]])

# Passo 3: Gerar scripts SQL para cada valor único
for valor in valores_unicos:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO public.mesorregioes (nome_mesorregiao) VALUES (%s)", (valor,))  # Note a vírgula após (valor,) para criar uma tupla
    conn.commit()

#------------------------------------------------------------------------------------------------------------
#--------------------------------INSERE MUNICIPIOS, PIB E ID_MESORREGIAO-------------------------------------
#------------------------------------------------------------------------------------------------------------

# Função para consultar o ID da mesorregião no banco de dados
def consultar_id_mesorregiao(nome_mesorregiao, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM mesorregioes WHERE nome_mesorregiao = %s", (nome_mesorregiao,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None

# Ler o arquivo Excel
df_muni = pd.read_excel("municipios-pib.xlsx", header=None)

# Iterar sobre as linhas do DataFrame
for indice, linha in df_muni.iterrows():
    nome_mesorregiao = linha[2]  # Ajuste para o nome exato da coluna no seu Excel
    id_mesorregiao = consultar_id_mesorregiao(nome_mesorregiao, conn)
    
    if id_mesorregiao:
        # Substitua 'tabela_principal' pelo nome da sua tabela principal no banco de dados
        # Substitua 'nome_municipio', 'pib', 'id_mesorregiao' pelos nomes corretos das colunas
        cursor = conn.cursor()
        cursor.execute("INSERT INTO municipios (nome_municipio, pib, id_mesorregiao) VALUES (%s, %s, %s)", (linha[0], linha[1], id_mesorregiao))
        conn.commit()

#------------------------------------------------------------------------------------------------------------
#-------------------------------------------INSERE POPULACAO-------------------------------------------------
#------------------------------------------------------------------------------------------------------------

# Função para consultar o ID da mesorregião no banco de dados
def consultar_id_municipio(nome_municipio, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM municipios WHERE nome_municipio = %s", (nome_municipio,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None

# Ler o arquivo Excel
df_pop = pd.read_excel("populacao.xlsx", header=None)

# Iterar sobre as linhas do DataFrame
for indice, linha in df_pop.iterrows():
    nome_municipio = linha[0]  # Ajuste para o nome exato da coluna no seu Excel
    id_municipio = consultar_id_municipio(nome_municipio, conn)
    
    if id_municipio:
        # Substitua 'tabela_principal' pelo nome da sua tabela principal no banco de dados
        # Substitua 'nome_municipio', 'pib', 'id_mesorregiao' pelos nomes corretos das colunas
        cursor = conn.cursor()
        cursor.execute("UPDATE municipios SET populacao = %s where id = %s", (linha[1],id_municipio))
        conn.commit()

#------------------------------------------------------------------------------------------------------------
#-------------------------------------INSERE MORTALIDADE GERAL-----------------------------------------------
#------------------------------------------------------------------------------------------------------------

def consultar_id_municipio_mortalidades(nome_municipio, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM municipios WHERE unaccent(nome_municipio) ILIKE %s", (nome_municipio,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None


# Ler o arquivo Excel
df_mort_geral = pd.read_excel("mortalidade-geral.xlsx", header=None)

# Iterar sobre as linhas do DataFrame
for indice, linha in df_mort_geral.iterrows():
    nome_municipio = linha[0]  # Ajuste para o nome exato da coluna no seu Excel
    nome_municipio_certo = nome_municipio.split(maxsplit=1)[1]
    id_municipio = consultar_id_municipio_mortalidades(nome_municipio_certo, conn)
    
    if id_municipio:
        # Substitua 'tabela_principal' pelo nome da sua tabela principal no banco de dados
        # Substitua 'nome_municipio', 'pib', 'id_mesorregiao' pelos nomes corretos das colunas
        cursor = conn.cursor()
        cursor.execute("UPDATE municipios SET mortalidade_geral = %s where id = %s", (linha[1],id_municipio))
        conn.commit()

#------------------------------------------------------------------------------------------------------------
#-------------------------------------INSERE MORTALIDADE FEMININA--------------------------------------------
#------------------------------------------------------------------------------------------------------------

# Ler o arquivo Excel
df_mort_geral = pd.read_excel("mortalidade-feminina.xlsx", header=None)

# Iterar sobre as linhas do DataFrame
for indice, linha in df_mort_geral.iterrows():
    nome_municipio = linha[0]  # Ajuste para o nome exato da coluna no seu Excel
    nome_municipio_certo = nome_municipio.split(maxsplit=1)[1]
    id_municipio = consultar_id_municipio_mortalidades(nome_municipio_certo, conn)
    
    if id_municipio:
        # Substitua 'tabela_principal' pelo nome da sua tabela principal no banco de dados
        # Substitua 'nome_municipio', 'pib', 'id_mesorregiao' pelos nomes corretos das colunas
        cursor = conn.cursor()
        cursor.execute("UPDATE municipios SET mortalidade_feminina = %s where id = %s", (linha[1],id_municipio))
        conn.commit()

#------------------------------------------------------------------------------------------------------------
#-------------------------------------INSERE MORTALIDADE MASCULINA-------------------------------------------
#------------------------------------------------------------------------------------------------------------

# Ler o arquivo Excel
df_mort_geral = pd.read_excel("mortalidade-masculina.xlsx", header=None)

# Iterar sobre as linhas do DataFrame
for indice, linha in df_mort_geral.iterrows():
    nome_municipio = linha[0]  # Ajuste para o nome exato da coluna no seu Excel
    nome_municipio_certo = nome_municipio.split(maxsplit=1)[1]
    id_municipio = consultar_id_municipio_mortalidades(nome_municipio_certo, conn)
    
    if id_municipio:
        # Substitua 'tabela_principal' pelo nome da sua tabela principal no banco de dados
        # Substitua 'nome_municipio', 'pib', 'id_mesorregiao' pelos nomes corretos das colunas
        cursor = conn.cursor()
        cursor.execute("UPDATE municipios SET mortalidade_masculina = %s where id = %s", (linha[1],id_municipio))
        conn.commit()
# Fechar conexão com o banco de dados
conn.close()

print("Criação feita com sucesso!")