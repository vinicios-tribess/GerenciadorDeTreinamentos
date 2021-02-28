import sqlite3
import colorama
from colorama import Fore, Back, Style
from functions import LeiaInt, LeiaInt1ou2, LeiaInt123ou4, LeiaStr1, LeiaStr2

colorama.init(autoreset=True)

banco = sqlite3.connect('BancoDeDados.db')
cursor = banco.cursor()

print(Fore.YELLOW + Style.BRIGHT + "Bem-vindo ao Gerenciador de Treinamentos Versão 5.0!")

try:
    cursor.execute("SELECT * FROM controle")
    dado = cursor.fetchall()

    if not dado:
        print(
            "\033[1;36mForam encontrados registros de uma utilização anterior. O que você deseja fazer?\033[m\n"
            "1\033[1;36m - Usar estes registros para fazer consultas.\033[m\n"
            "2\033[1;36m - Deletar todos os registros existentes para cadastrar novos.\033[m\n"
        )

        print(Fore.MAGENTA + Style.BRIGHT + "Sua opção")
        opcao = LeiaInt1ou2("->")

        if opcao == 1:
            print(Fore.CYAN + Style.BRIGHT + "Usando os registros existentes...")
        else:
            cursor.execute("SELECT * FROM tabela_inexistente")
            erro = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM tabela_inexistente")
        erro = cursor.fetchall()

except sqlite3.OperationalError:

    lista_tabelas = ["espacos_cafe", "etapa1_espacos_cafe", "etapa1_salas", "etapa2_espacos_cafe", "etapa2_salas", "pessoas", "salas", "controle"]

    for i in range(0, 8):
        cursor.execute(f"DROP TABLE IF EXISTS {lista_tabelas[i]}")

    print(Fore.CYAN + Style.BRIGHT + "Digite o número de pessoas que participarão do evento: ")
    n_pessoas = LeiaInt("->")

    print(Fore.GREEN + Style.BRIGHT +"Digite o nome e sobrenome de cada pessoa que participará do evento: ")

    for i in range (1, n_pessoas + 1):
        print(Fore.GREEN + Style.BRIGHT + f"Nome e sobrenome da {i}ª pessoa: ")
        nome = LeiaStr1("->")
        cursor.execute("CREATE TABLE IF NOT EXISTS pessoas (id_pessoa integer primary key, nome_pessoa text not null)")
        cursor.execute(f"INSERT INTO pessoas VALUES('{i}', '{nome}')")
        banco.commit()

    while True:
        print(Fore.CYAN + Style.BRIGHT + "Digite o número de salas disponíveis: ")
        n_salas = LeiaInt("->")
        if n_salas > n_pessoas:
            print(Fore.RED + Style.BRIGHT + "Erro! o número de salas não pode ser superior ao número de pessoas.")
        else:
            break

    di = (n_pessoas // n_salas)
    resto = (n_pessoas % n_salas)

    c = True
    while True:
        if c == True:
            try:
                while True:

                    controle_lotacoes = []

                    if resto != 0:
                        print(Fore.YELLOW + Style.BRIGHT + f"Atenção! Para que {n_pessoas} pessoas caibam em {n_salas} salas, com no máximo 1 pessoa de diferença entre cada sala,")
                        print(Fore.YELLOW + Style.BRIGHT + f"são necessárias no mínimo {resto} sala(s) com lotação igual a {di + 1} e {n_salas - resto} sala(s) com lotação igual a {di}.")
                        for i in range(0, resto):
                            controle_lotacoes.append(di + 1)
                        for i in range(0, n_salas - resto):
                            controle_lotacoes.append(di)

                    else:
                        print(Fore.YELLOW + Style.BRIGHT + f"Atenção! Para que {n_pessoas} pessoas caibam em {n_salas} salas, de maneira uniforme,")
                        print(Fore.YELLOW + Style.BRIGHT + f"é necessário que cada uma das {n_salas} salas tenha lotação mínima de {di} pessoas.")
                        for i in range(0, n_salas):
                            controle_lotacoes.append(di)

                    sorted(controle_lotacoes)
                    controle_lotacoes.reverse

                    print(Fore.GREEN + Style.BRIGHT + "Digite o nome das salas e em seguida suas respectivas lotações: ")

                    lista_lotacoes = []
                    for i in range (1, n_salas + 1):
                        print(Fore.GREEN + Style.BRIGHT + f"Nome da {i}ª sala: ")
                        nome_sala = LeiaStr2("->")
                        while True:
                            print(Fore.MAGENTA + Style.BRIGHT + f"Lotação da {i}ª sala (mín. {controle_lotacoes[i - 1]}): ")
                            lotacao = LeiaInt("->")
                            if lotacao < controle_lotacoes[i - 1]:
                                print(Fore.RED + Style.BRIGHT + "Erro! Respeite o número mínimo para a lotação da sala.")
                            else:
                                break
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
                        print(Fore.RED + Style.BRIGHT + "Ops! Algo deu errado no cadastro das salas. Verifique os dados e tente novamente.")

            except sqlite3.IntegrityError:
                print(Fore.RED + Style.BRIGHT + "Erro! Não podem haver salas com o mesmo nome. Tente Novamente.")
                cursor.execute("DROP TABLE IF EXISTS salas")
        else:
            break

    resto = n_pessoas % 2

    c = True
    while True:
        if c == True:
            try:
                while True:

                    controle_lotacoes2 = []

                    if resto == 0:
                        print(Fore.YELLOW + Style.BRIGHT + f"Atenção! Para que {n_pessoas} pessoas caibam em 2 espaços de café, de maneira uniforme,")
                        print(Fore.YELLOW + Style.BRIGHT + f"ambos os espaços devem ter lotação mínima igual a {n_pessoas // 2}.")
                        for i in range(0, 2):
                            controle_lotacoes2.append(n_pessoas // 2)

                    else:
                        print(Fore.YELLOW + Style.BRIGHT + f"Atenção! Para que {n_pessoas} pessoas caibam em 2 espaços de café, com no máximo 1 pessoa de diferença entre cada espaço,")
                        print(Fore.YELLOW + Style.BRIGHT + f"é necessário que um espaço tenha lotação mínima de {(n_pessoas // 2) + 1} e outro tenha lotação mínima de {(n_pessoas // 2)}.")
                        
                        controle_lotacoes2.append((n_pessoas // 2) + 1)
                        controle_lotacoes2.append(n_pessoas // 2)

                    print(Fore.GREEN + Style.BRIGHT + "Digite o nome dos espaços de café e em seguida suas respectivas lotações: ")

                    lista_lotacoes = []
                    for i in range (1, 3):
                        print(Fore.GREEN + Style.BRIGHT + f"Nome do {i}º espaço de café: ")
                        nome_espaco = LeiaStr2("->")
                        while True:
                            print(Fore.MAGENTA + Style.BRIGHT + f"Lotação do {i}º espaço de café (mín. {controle_lotacoes2[i - 1]}): ")
                            lotacao = LeiaInt("->")
                            if lotacao < controle_lotacoes2[i - 1]:
                                print(Fore.RED + Style.BRIGHT + "Erro! Respeite o número mínimo para a lotação da sala.")
                            else:
                                break
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
                        print(Fore.RED + Style.BRIGHT + "Ops! Algo deu errado no cadastro dos espaços de café. Verifique os dados e tente novamente.")

            except sqlite3.IntegrityError:
                print(Fore.RED + Style.BRIGHT + "Erro! Não podem haver espaços de café com o mesmo nome. Tente Novamente.")
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

    cursor.execute("CREATE TABLE IF NOT EXISTS controle (controle1 integer primary key, controle2 text not null)")
    banco.commit()

finally:
    print(Fore.YELLOW + Style. BRIGHT + "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("\033[1;36mTudo pronto! Os dados estão salvos e já podem ser utilizados.\033[m")

    while True:
        print(
            "\033[1;36mDigite a opção do que você deseja fazer agora:\033[m\n"
            "1\033[1;36m - Consultar pessoa pelo nome.\033[m\n"
            "2\033[1;36m - Consultar sala pelo nome.\033[m\n"
            "3\033[1;36m - Consultar espaço de café pelo nome.\033[m\n"
            "4\033[1;36m - Sair (encerrar o programa).\033[m\n"
        )

        print(Fore.MAGENTA + Style.BRIGHT + "Sua opção: ")
        escolha = LeiaInt123ou4("->")

        if escolha == 1:
            while True:
                print(Fore.MAGENTA + Style.BRIGHT + "Digite o nome da pessoa: ")
                nome = LeiaStr1("->")

                cursor.execute(f"select * from pessoas where nome_pessoa = '{nome}'")
                verificacao = cursor.fetchall()

                if not verificacao:
                    print(Fore.RED + Style.BRIGHT + "Erro! Não foram encontrados dados para o parâmetro informado. Tente novamente.")
                else:
                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa1_salas ON salas.id_sala = etapa1_salas.id_sala WHERE nome_pessoa = '{nome}'")
                    dados = cursor.fetchall()
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        nome_sala = i[2]
                        print(Fore.GREEN + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}, ficará na sala {nome_sala} durante a etapa 1 do treinamento.")

                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa1_espacos_cafe ON espacos_cafe.id_espaco = etapa1_espacos_cafe.id_espaco WHERE nome_pessoa = '{nome}'")
                    dados = cursor.fetchall()
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        nome_espaco = i[2]
                        print(Fore.WHITE + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}, ficará no espaço de café {nome_espaco} durante a etapa 1 do treinamento.")

                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa2_salas ON salas.id_sala = etapa2_salas.id_sala WHERE nome_pessoa = '{nome}'")
                    dados = cursor.fetchall()
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        nome_sala = i[2]
                        print(Fore.GREEN + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}, ficará na sala {nome_sala} durante a etapa 2 do treinamento.")

                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa2_espacos_cafe ON espacos_cafe.id_espaco = etapa2_espacos_cafe.id_espaco WHERE nome_pessoa = '{nome}'")
                    dados = cursor.fetchall()
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        nome_espaco = i[2]
                        print(Fore.WHITE + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}, ficará no espaço de café {nome_espaco} durante a etapa 2 do treinamento.")

                    print(
                        "\033[1;36mO que você deseja fazer agora?\033[m\n"
                        "1\033[1;36m - Nova consulta\033[m\n"
                        "2\033[1;36m - Voltar ao menu\033[m\n"
                    )

                    print(Fore.MAGENTA + Style.BRIGHT + "Sua opção: ")
                    escolha_nome = LeiaInt1ou2("->")

                    if escolha_nome == 1:
                        print(Fore.CYAN + Style.BRIGHT + "Fazendo uma nova consulta...")
                    if escolha_nome == 2:
                        break

        if escolha == 2:
            while True:
                print(Fore.MAGENTA + Style.BRIGHT + "Digite o nome da sala: ")
                sala = LeiaStr2("->")

                cursor.execute(f"select * from salas where nome_sala = '{sala}'")
                verificacao = cursor.fetchall()

                if not verificacao:
                    print(Fore.RED + Style.BRIGHT + "Erro! Não foram encontrados dados para o parâmetro informado. Tente novamente.")
                else:
                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa1_salas ON salas.id_sala = etapa1_salas.id_sala WHERE nome_sala = '{sala}'")
                    dados = cursor.fetchall()
                    print(Fore.CYAN + Style.BRIGHT + f"Na sala {sala}, na etapa 1, ficarão as seguintes pessoas: ")
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        print(Fore.GREEN + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}")

                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_sala FROM salas INNER JOIN etapa2_salas ON salas.id_sala = etapa2_salas.id_sala WHERE nome_sala = '{sala}'")
                    dados = cursor.fetchall()
                    print(Fore.CYAN + Style.BRIGHT + f"Na sala {sala}, na etapa 2, ficarão as seguintes pessoas: ")
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        print(Fore.WHITE + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}")

                    print(
                        "\033[1;36mO que você deseja fazer agora?\033[m\n"
                        "1\033[1;36m - Nova consulta\033[m\n"
                        "2\033[1;36m - Voltar ao menu\033[m\n"
                    )

                    print(Fore.MAGENTA + Style.BRIGHT + "Sua opção: ")
                    escolha_sala = LeiaInt1ou2("->")

                    if escolha_sala == 1:
                        print(Fore.CYAN + Style.BRIGHT + "Fazendo uma nova consulta...")
                    if escolha_sala == 2:
                        break

        if escolha == 3:
            while True:
                print(Fore.MAGENTA + Style.BRIGHT + "Digite o nome do espaco de café: ")
                espaco = LeiaStr2("->")

                cursor.execute(f"select * from espacos_cafe where nome_espaco = '{espaco}'")
                verificacao = cursor.fetchall()

                if not verificacao:
                    print(Fore.RED + Style.BRIGHT + "Não foram encontrados dados para o parâmetro informado. Tente novamente.")
                else:
                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa1_espacos_cafe ON espacos_cafe.id_espaco = etapa1_espacos_cafe.id_espaco WHERE nome_espaco = '{espaco}'")
                    dados = cursor.fetchall()
                    print(Fore.CYAN + Style.BRIGHT + f"No espaço de café {espaco}, na etapa 1, ficarão as seguintes pessoas: ")
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        print(Fore.GREEN + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}")

                    cursor.execute(f"SELECT id_pessoa, nome_pessoa, nome_espaco FROM espacos_cafe INNER JOIN etapa2_espacos_cafe ON espacos_cafe.id_espaco = etapa2_espacos_cafe.id_espaco WHERE nome_espaco = '{espaco}'")
                    dados = cursor.fetchall()
                    print(Fore.CYAN + Style.BRIGHT + f"No espaço de café {espaco}, na etapa 2, ficarão as seguintes pessoas: ")
                    for i in dados:
                        id_pessoa = i[0]
                        nome_pessoa = i[1]
                        print(Fore.WHITE + Style.BRIGHT + f"(ID {id_pessoa}), {nome_pessoa}")

                    print(
                        "\033[1;36mO que você deseja fazer agora?\033[m\n"
                        "1\033[1;36m - Nova consulta\033[m\n"
                        "2\033[1;36m - Voltar ao menu\033[m\n"
                    )

                    print(Fore.MAGENTA + Style.BRIGHT + "Sua opção: ")
                    escolha_espaco = LeiaInt1ou2("->")

                    if escolha_espaco == 1:
                        print(Fore.CYAN + Style.BRIGHT + "Fazendo uma nova consulta...")
                    if escolha_espaco == 2:
                        break
        if escolha == 4:
            print(Fore.CYAN + Style.BRIGHT + "Programa encerrado! Volte sempre!")
            banco.close()
            break