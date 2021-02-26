import sqlite3

banco = sqlite3.connect('BancoDeDados.db')
cursor = banco.cursor()

n_pessoas = int(input("Digite o número de pessoas que participarão do evento: "))

print("Digite o nome e sobrenome de cada pessoa que participará do evento: ")

for i in range (1, n_pessoas + 1):
    nome = str(input(f"Nome e sobrenome da {i}ª pessoa: "))
    cursor.execute("CREATE TABLE IF NOT EXISTS pessoas (id_pessoa integer primary key, nome_pessoa text not null)")
    cursor.execute(f"INSERT INTO pessoas VALUES('{i}', '{nome}')")
    banco.commit()

n_salas = int(input("Digite o número de salas disponíveis: "))

print("Digite o nome das salas e em seguida suas respectivas lotações: ")

for i in range (1, n_salas + 1):
    nome_sala = str(input(f"Nome da {i}ª sala: "))
    lotacao = str(input(f"Lotação da sala {i}ª: "))
    cursor.execute("CREATE TABLE IF NOT EXISTS salas (id_sala integer primary key, nome_sala text not null, lotacao_sala integer not null)")
    cursor.execute(f"INSERT INTO salas VALUES('{i}', '{nome_sala}', {lotacao})")
    banco.commit()

print("Digite o nome dos espaços de café e em seguida suas respectivas lotações: ")

for i in range (1, 3):
    nome_espaco = str(input(f"Nome do {i}º espaço de café: "))
    lotacao = str(input(f"Lotação do {i}º espaço de café: "))
    cursor.execute("CREATE TABLE IF NOT EXISTS espacos_cafe (id_espaco integer primary key, nome_espaco text not null, lotacao_espaco integer not null)")
    cursor.execute(f"INSERT INTO espacos_cafe VALUES('{i}', '{nome_espaco}', {lotacao})")
    banco.commit()

# Essa parte separa as pessoas em salas para a etapa 1:

cursor.execute("SELECT * FROM pessoas ORDER BY id_pessoa")
dados = cursor.fetchall()

lista_nomes = []
for i in range(0, len(dados)):
    item = dados[i]
    lista_nomes.append(item[1])

cursor.execute("CREATE TABLE IF NOT EXISTS etapa1_salas (id_pessoa integer primary key, nome_pessoa text not null, id_sala integer)")

c = 0
while c <= n_pessoas:
    for i in range(1, n_salas + 1):
        if c < n_pessoas:
            sala = i
            item = dados[c]
            cursor.execute(f"INSERT INTO etapa1_salas VALUES({c + 1}, '{lista_nomes[c]}', {sala})" )
            banco.commit()
            c = c + 1
        else:
            c = c + 1

# Essa parte troca metade das pessoas de sala para a etapa 2:

def metade_cheia(n):
    resultado = n % 2
    if resultado == 0:
        return int(n / 2)
    else:
        return int((n // 2) + 1)

cursor.execute("SELECT * FROM etapa1_salas ORDER BY id_pessoa")
etapa1_dados = cursor.fetchall()

c = 2
for i in range(0, metade_cheia(n_pessoas)):
    lista = list(etapa1_dados.pop(i))
    lista.pop()
    sala_etapa2 = c
    if i == metade_cheia(n_pessoas) - 1:
        lista.append(1)
        registro = tuple(lista)
        etapa1_dados.insert(i, registro)
    elif sala_etapa2 <= n_salas:
        lista.append(sala_etapa2)
        registro = tuple(lista)
        etapa1_dados.insert(i, registro)
        c = c + 1
    else:
        c = 1
        lista.append(c)
        registro = tuple(lista)
        etapa1_dados.insert(i, registro)
        c = c + 1

etapa2_dados = etapa1_dados

cursor.execute("CREATE TABLE IF NOT EXISTS etapa2_salas (id_pessoa integer primary key, nome_pessoa text not null, id_sala integer not null)")
cursor.executemany("INSERT INTO etapa2_salas (id_pessoa, nome_pessoa, id_sala) VALUES (?, ?, ?)", etapa2_dados)
banco.commit()

# Essa parte separa as pessoas para o intervalo de café da etapa 1:

cursor.execute("SELECT * FROM pessoas ORDER BY id_pessoa")
dados = cursor.fetchall()

lista_nomes = []
for i in range(0, len(dados)):
    item = dados[i]
    lista_nomes.append(item[1])

cursor.execute("CREATE TABLE IF NOT EXISTS etapa1_espacos_cafe (id_pessoa integer primary key, nome_pessoa text not null, id_espaco integer)")

c = 0
while c <= n_pessoas:
    for i in range(1, 3):
        if c < n_pessoas:
            id_espaco = i
            item = dados[c]
            cursor.execute(f"INSERT INTO etapa1_espacos_cafe VALUES({c + 1}, '{lista_nomes[c]}', {id_espaco})" )
            banco.commit()
            c = c + 1
        else:
            c = c + 1

# Essa parte troca metade das pessoas para o intervalo de café da etapa 1:

cursor.execute("SELECT * FROM etapa1_espacos_cafe ORDER BY id_pessoa")
dados = cursor.fetchall()

for i in range(0, len(dados)):
    lista = list(dados.pop(i))
    espaco_cafe = lista.pop()
    if espaco_cafe == 1:
        lista.append(2)
        registro = tuple(lista)
        dados.insert(i, registro)
    else:
        lista.append(1)
        registro = tuple(lista)
        dados.insert(i, registro)

espaco_cafe2 = dados

cursor.execute("CREATE TABLE IF NOT EXISTS etapa2_espacos_cafe (id_pessoa integer primary key, nome_pessoa text not null, id_espaco integer not null)")
cursor.executemany("INSERT INTO etapa2_espacos_cafe (id_pessoa, nome_pessoa, id_espaco) VALUES (?, ?, ?)", espaco_cafe2)
banco.commit()

print(
    "Tudo pronto! Digite a opção do que você deseja fazer agora:\n"
    "1 - Consultar pessoa pelo nome.\n"
    "2 - Consultar sala ou espaço de café pelo nome.\n"
)

escolha = int(input("Sua opção: "))

if escolha == 1:

    nome = str(input("Digite o nome da pessoa: "))

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa1_salas ON salas.id_sala = etapa1_salas.id_sala WHERE nome_pessoa = '{nome}'")
    dados = cursor.fetchall()
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        nome_sala = i[2]
        print(f"{nome_pessoa}, de ID nº {id_pessoa}, ficará na sala {nome_sala} durante a etapa 1 do treinamento.")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa2_salas ON salas.id_sala = etapa2_salas.id_sala WHERE nome_pessoa = '{nome}'")
    dados = cursor.fetchall()
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        nome_sala = i[2]
        print(f"{nome_pessoa}, de ID nº {id_pessoa}, ficará na sala {nome_sala} durante a etapa 2 do treinamento.")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa1_espacos_cafe ON espacos_cafe.id_espaco = etapa1_espacos_cafe.id_espaco WHERE nome_pessoa = '{nome}'")
    dados = cursor.fetchall()
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        nome_espaco = i[2]
        print(f"{nome_pessoa}, de ID nº {id_pessoa}, ficará no espaço de café {nome_espaco} durante a etapa 1 do treinamento.")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa2_espacos_cafe ON espacos_cafe.id_espaco = etapa2_espacos_cafe.id_espaco WHERE nome_pessoa = '{nome}'")
    dados = cursor.fetchall()
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        nome_espaco = i[2]
        print(f"{nome_pessoa}, de ID nº {id_pessoa}, ficará no espaço de café {nome_espaco} durante a etapa 1 do treinamento.")

elif escolha == 2:
    print("Ainda falta fazer.")
else:
    print("Essa não é uma opção válida. Tente novamente.")

banco.close()

print("Acabou!")
