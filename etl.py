import pymysql
from datetime import datetime

print("=== Iniciando o pipeline de ETL Multi-Usuários ===")

try:
    conexao = pymysql.connect(
        host="localhost",
        user="root",
        password="digite_sua_senha_aqui", 
        database="integracao_estagio"
    )
    print("✓ Conexão com o MySQL realizada com sucesso!")
except Exception as e:
    print(f"✗ Erro ao conectar no banco: {e}")
    exit()

# aqui estou simulando uma lista de novas entradas enviadas por um sistema.

novas_entradas = [
    {"id": 81, "nome": "Clarisse Ferreira", "email": "cLARISSE01.amaral@gmail.com", "cidade": "Brasilia", "empresa": "Barbie Tech"},
    {"id": 89, "nome": "Arthur da Silva", "email": "Arthursales@OUTLOOK.com", "cidade": "Brasília", "empresa": "Inovacao Digital"},
    {"id": 98, "nome": "Davi Ferreira", "email": "Davi.ferreira@gmail.com", "cidade": "Brasilia", "empresa": "Gauss tecnologias"}
]
print(f"✓ {len(novas_entradas)} registros brutos extraídos da origem.")

# conectando com o banco de dados

cursor = conexao.cursor()

query = """
INSERT INTO tb_usuarios_tratados (id, nome, email, cidade, empresa, data_importacao) 
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE nome=%s, email=%s, cidade=%s, empresa=%s, data_importacao=%s; 
"""
# O "duplicate key update" não permite que duplique os dados que vem de um mesmo ID, e sim que os atualize.

sucessos = 0

for usuario in novas_entradas:
    try:
        
        id_bruto = usuario["id"]
        nome_tratado = usuario["nome"].upper()
        email_tratado = usuario["email"].lower()
        cidade_tratada = usuario["cidade"]
        empresa_tratada = usuario["empresa"].upper() 
        agora = datetime.now()

        cursor.execute(query, (
            id_bruto, nome_tratado, email_tratado, cidade_tratada, empresa_tratada, agora, 
            nome_tratado, email_tratado, cidade_tratada, empresa_tratada, agora
        ))
        sucessos += 1
        print(f"   -> Usuário ID {id_bruto} tratado e carregado.")

    except Exception as erro_linha:
        print(f"   ✗ Erro ao processar o ID {usuario['id']}: {erro_linha}")

# Um commit que confirma e salva todas as alterações de uma vez só no banco de dados

conexao.commit()

print(f"\n✓ Processo concluído! {sucessos} de {len(novas_entradas)} registros carregados.")

 # fechando a conexão com o banco e encerrando o pipeline
conexao.close()
print("=== Pipeline Python Finalizado ===")
