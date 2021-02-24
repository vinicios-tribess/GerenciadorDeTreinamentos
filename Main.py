import sqlite3

print(
    "Digite o nome e sobrenome de cada pessoa que participará do treinamento. \n"
    "Quando tiver terminado de digitar um nome, pressione Enter para digitar o próximo. \n"
    "Quando tiver terminado de digitar todos os nomes, pressione Tab para prosseguir."
)

banco = sqlite3.connect('Pessoas.db')
cursor = banco.cursor()

resposta = "S"
while resposta == "S":
    nome = str(input("Digite um valor: "))
    cursor.execute("CREATE TABLE IF NOT EXISTS pessoas (nomes text not null)")
    cursor.execute(f"INSERT INTO pessoas VALUES('{nome}')")
    banco.commit()
    resposta = (str(input("Quer digitar mais algum nome? [S/N]"))).upper()

banco.close()

print("Acabou!")