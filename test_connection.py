import pyodbc

# Configuração da conexão
server = '144.217.146.55'
database = 'PS_UserData'
username = 'Valpassos'
password = 'Mr11011998#'

# String de conexão
conn_str = f"""
    DRIVER={{ODBC Driver 18 for SQL Server}};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    TrustServerCertificate=yes;  # Use apenas se o certificado for autoassinado
"""

try:
    # Conecta ao banco
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Executa uma query de teste
    cursor.execute("SELECT * FROM dbo.Users_Master")
    row = cursor.fetchone()
    print("Conexão bem-sucedida!")
    print("Primeira linha da tabela:", row)
    
except pyodbc.Error as e:
    print("Erro de conexão:", e)
finally:
    if 'conn' in locals():
        conn.close()