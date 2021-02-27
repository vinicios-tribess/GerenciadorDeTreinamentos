import sqlite3
from teste import LeiaInt, LeiaStr1, LeiaStr2

banco = sqlite3.connect('BancoDeDados.db')
cursor = banco.cursor()

n_pessoas = LeiaInt("\033[1;36mDigite o número de pessoas que participarão do evento: \033[m")

print("\033[1;32mDigite o nome e sobrenome de cada pessoa que participará do evento: \033[m")

for i in range (1, n_pessoas + 1):
    nome = LeiaStr1(f"\033[1;32mNome e sobrenome da {i}ª pessoa: \033[m")
    cursor.execute("CREATE TABLE IF NOT EXISTS pessoas (id_pessoa integer primary key, nome_pessoa text not null)")
    cursor.execute(f"INSERT INTO pessoas VALUES('{i}', '{nome}')")
    banco.commit()

n_salas = LeiaInt("\033[1;36mDigite o número de salas disponíveis: \033[m")

di = (n_pessoas // n_salas)
resto = (n_pessoas % n_salas)

c = True
while True:
    if c == True:
        try:
            while True:

                if resto != 0:
                    print(
                        f"\033[0;33mAtenção! Para que {n_pessoas} pessoas caibam em {n_salas} salas, com no máximo 1 pessoa de diferença entre cada sala,\033[m \n"
                        f"\033[0;33msão necessárias no mínimo {resto} sala(s) com lotação igual a {di + 1} e {n_salas - resto} sala(s) com lotação igual a {di}.\033[m"
                    )
                else:
                    print(
                        f"\033[0;33mAtenção! Para que {n_pessoas} pessoas caibam em {n_salas} salas, de maneira uniforme,\033[m \n"
                        f"\033[0;33mé necessário que cada uma das {n_salas} salas tenha lotação mínima de {di} pessoas.\033[m"
                    )

                print("\033[1;32mDigite o nome das salas e em seguida suas respectivas lotações: \033[m")

                lista_lotacoes = []
                for i in range (1, n_salas + 1):
                    nome_sala = LeiaStr2(f"\033[1;32mNome da {i}ª sala: \033[m")
                    lotacao = LeiaInt(f"\033[1;35mLotação da sala {i}ª: \033[m")
                    lista_lotacoes.append(lotacao)
                    cursor.execute("CREATE TABLE IF NOT EXISTS salas (id_sala integer not null, nome_sala text primary key, lotacao_sala integer not null)")
                    cursor.execute(f"INSERT INTO salas VALUES('{i}', '{nome_sala}', {lotacao})")
                    banco.commit()

                lista_ordenada = sorted(lista_lotacoes)
                menor_valor = lista_ordenada[0]

                if menor_valor >= di and sum(lista_ordenada) >= n_pessoas:  
                    c = False
                    break
                else:
                    cursor.execute("DROP TABLE IF EXISTS salas")
                    print("\033[0;31mOps! Algo deu errado no cadastro das salas. Verifique os dados e tente novamente.\033[m")

        except sqlite3.IntegrityError:
            print("\033[0;31mErro! Não podem haver salas com o mesmo nome. Tente Novamente.\033[m")
            cursor.execute("DROP TABLE IF EXISTS salas")
    else:
        break

print(
    "\033[1;32mDigite o nome dos espaços de café e em seguida suas respectivas lotações: \033[m \n"
    "\033[4;33mLembre-se de que a soma das lotações dos espaços de café deve ser maior ou igual ao número de pessoas\033[m"
)

resto = n_pessoas % 2

c = True
while True:
    if c == True:
        try:
            while True:

                if resto == 0:
                    print(
                        f"\033[0;33mAtenção! Para que {n_pessoas} pessoas caibam em 2 espaços de café, de maneira uniforme,\033[m \n"
                        f"\033[0;33mambos os espaços devem ter lotação mínima igual a {n_pessoas // 2}.\033[m"
                    )
                else:
                    print(
                        f"\033[0;33mAtenção! Para que {n_pessoas} pessoas caibam em 2 espaços de café, com no máximo 1 pessoa de diferença entre cada espaço,\033[m \n"
                        f"\033[0;33mé necessário que um espaço tenha lotação mínima de {(n_pessoas // 2) + 1} e outro tenha lotação mínima de {(n_pessoas // 2)}.\033[m"
                    )

                lista_lotacoes = []
                for i in range (1, 3):
                    nome_espaco = LeiaStr2(f"\033[1;32mNome do {i}º espaço de café: \033[m")
                    lotacao = LeiaInt(f"\033[1;35mLotação do {i}º espaço de café: \033[m")
                    lista_lotacoes.append(lotacao)
                    cursor.execute("CREATE TABLE IF NOT EXISTS espacos_cafe (id_espaco integer not null, nome_espaco text primary key, lotacao_espaco integer not null)")
                    cursor.execute(f"INSERT INTO espacos_cafe VALUES('{i}', '{nome_espaco}', {lotacao})")
                    banco.commit()

                lista_ordenada = sorted(lista_lotacoes)
                menor_valor = lista_ordenada[0]

                if sum(lista_lotacoes) >= n_pessoas and menor_valor >= (n_pessoas // 2):
                    c = False
                    break
                else:
                    cursor.execute("DROP TABLE IF EXISTS espacos_cafe")
                    print("\033[0;31mOps! Algo deu errado no cadastro dos espaços de café. Verifique os dados e tente novamente.\033[m")
                    print("\033[0;33mLembre-se de que a soma das lotações dos espaços de café deve ser maior ou igual ao número de pessoas.\033[m")

        except sqlite3.IntegrityError:
            print("\033[0;31mErro! Não podem haver espaços de café com o mesmo nome. Tente Novamente.\033[m")
            cursor.execute("DROP TABLE IF EXISTS espacos_cafe")
    else:
        break

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

banco.close()

print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

print(
    "Tudo pronto! Digite a opção do que você deseja fazer agora:\n"
    "1 - Consultar pessoa pelo nome.\n"
    "2 - Consultar sala pelo nome.\n"
    "3 - Consultar espaço de café pelo nome\n"
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
        print(f"{nome_pessoa}, ID {id_pessoa}, ficará na sala {nome_sala} durante a etapa 1 do treinamento.")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa1_espacos_cafe ON espacos_cafe.id_espaco = etapa1_espacos_cafe.id_espaco WHERE nome_pessoa = '{nome}'")
    dados = cursor.fetchall()
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        nome_espaco = i[2]
        print(f"{nome_pessoa}, ID {id_pessoa}, ficará no espaço de café {nome_espaco} durante a etapa 1 do treinamento.")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa2_salas ON salas.id_sala = etapa2_salas.id_sala WHERE nome_pessoa = '{nome}'")
    dados = cursor.fetchall()
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        nome_sala = i[2]
        print(f"{nome_pessoa}, ID {id_pessoa}, ficará na sala {nome_sala} durante a etapa 2 do treinamento.")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa2_espacos_cafe ON espacos_cafe.id_espaco = etapa2_espacos_cafe.id_espaco WHERE nome_pessoa = '{nome}'")
    dados = cursor.fetchall()
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        nome_espaco = i[2]
        print(f"{nome_pessoa}, ID {id_pessoa}, ficará no espaço de café {nome_espaco} durante a etapa 1 do treinamento.")

if escolha == 2:
    
    sala = str(input("Digite o nome da sala: "))

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa1_salas ON salas.id_sala = etapa1_salas.id_sala WHERE nome_sala = '{sala}'")
    dados = cursor.fetchall()
    print(f"Na sala {sala}, na etapa 1, ficarão as seguintes pessoas: ")
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        print(f"{nome_pessoa}; ID: {id_pessoa}")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa2_salas ON salas.id_sala = etapa2_salas.id_sala WHERE nome_sala = '{sala}'")
    dados = cursor.fetchall()
    print(f"Na sala {sala}, na etapa 2, ficarão as seguintes pessoas: ")
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        print(f"{nome_pessoa}; ID: {id_pessoa}")

if escolha == 3:
    
    espaco = str(input("Digite o nome do espaco de café: "))

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa1_espacos_cafe ON espacos_cafe.id_espaco = etapa1_espacos_cafe.id_espaco WHERE nome_espaco = '{espaco}'")
    dados = cursor.fetchall()
    print(f"No espaço de café {espaco}, na etapa 1, ficarão as seguintes pessoas: ")
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        print(f"{nome_pessoa}; ID: {id_pessoa}")

    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa2_espacos_cafe ON espacos_cafe.id_espaco = etapa2_espacos_cafe.id_espaco WHERE nome_espaco = '{espaco}'")
    dados = cursor.fetchall()
    print(f"No espaço de café {espaco}, na etapa 2, ficarão as seguintes pessoas: ")
    for i in dados:
        id_pessoa = i[0]
        nome_pessoa = i[1]
        print(f"{nome_pessoa}; ID: {id_pessoa}")

else:
    print("Essa não é uma opção válida. Tente novamente.")

banco.close()

print("Acabou!")
