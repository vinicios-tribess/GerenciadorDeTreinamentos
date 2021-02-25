import sqlite3

banco = sqlite3.connect('BancoDeDados.db')
cursor = banco.cursor()

n_pessoas = int(input("Digite o número de pessoas que participarão do treinamento: "))

print("Digite o nome e sobrenome de cada pessoa que participará do treinamento: ")

for i in range (1, n_pessoas + 1):
    nome = str(input(f"Digite o nome e sobrenome da {i}ª pessoa: "))
    cursor.execute("CREATE TABLE IF NOT EXISTS pessoas (id_pessoa integer primary key, nome_pessoa text not null)")
    cursor.execute(f"INSERT INTO pessoas VALUES('{i}', '{nome}')")
    banco.commit()

n_salas = int(input("Digite o número de salas onde o treinamento será realizado: "))

print("Digite o nome das salas e em seguida suas respectivas lotações: ")

for i in range (1, n_salas + 1):
    nome_sala = str(input(f"Digite o nome da sala {i}: "))
    lotacao = str(input(f"Digite a lotação da sala {i}: "))
    cursor.execute("CREATE TABLE IF NOT EXISTS salas (id_sala integer primary key, nome_sala text not null, lotacao_sala integer not null)")
    cursor.execute(f"INSERT INTO salas VALUES('{i}', '{nome_sala}', {lotacao})")
    banco.commit()

print("Digite o nome dos espaços de café e em seguida suas respectivas lotações: ")

for i in range (1, 3):
    nome_espaco = str(input(f"Digite o nome do espaço de café {i}: "))
    lotacao = str(input(f"Digite a lotação do espaço de café {i}: "))
    cursor.execute("CREATE TABLE IF NOT EXISTS espacos (id_espaco integer primary key, nome_espaco text not null, lotacao_espaco integer not null)")
    cursor.execute(f"INSERT INTO espacos VALUES('{i}', '{nome_espaco}', {lotacao})")
    banco.commit()

banco.close()

print("Acabou!")