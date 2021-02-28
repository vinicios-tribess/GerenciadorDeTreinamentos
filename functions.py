import colorama
from colorama import Fore, Back, Style

def LeiaInt(msg):
    ok = False
    valor = 0
    while True:
        n = str(input(msg))
        if n.isnumeric() and int(n) > 0:
            valor = int(n)
            ok = True
        else:
            print(Fore.RED + Style.BRIGHT + 'Erro: Entrada inválida! Digite um número inteiro maior que 0.')
        if ok:
            break
    return valor

def LeiaInt1ou2(msg):
    ok = False
    valor = 0
    while True:
        n = str(input(msg))
        if n.isnumeric() and int(n) > 0 and int(n) < 3:
            valor = int(n)
            ok = True
        else:
            print(Fore.RED + Style.BRIGHT + 'Erro: Entrada inválida! Digite 1 ou 2, de acordo com sua opção.')
        if ok:
            break
    return valor

def LeiaInt123ou4(msg):
    ok = False
    valor = 0
    while True:
        n = str(input(msg))
        if n.isnumeric() and int(n) > 0 and int(n) < 5:
            valor = int(n)
            ok = True
        else:
            print(Fore.RED + Style.BRIGHT + 'Erro: Entrada inválida! Digite 1, 2 ou 3, de acordo com sua opção.')
        if ok:
            break
    return valor

def LeiaStr1(msg):
    ok = False
    valor = 0
    while True:
        n = str(input(msg))
        n.strip()
        split = n.split()
        if len(split) >= 2 and ("".join(split)).isalpha():
            nome = " ".join(split)
            valor = str(nome)
            ok = True
        else: 
            print(Fore.RED + Style.BRIGHT + 'Erro: Entrada inválida! Digite utilizando apenas letras.')
        if ok:
            break
    return valor.title()

def LeiaStr2(msg):
    ok = False
    valor = 0
    while True:
        n = str(input(msg))
        n.strip()
        split = n.split()
        if ("".join(split)).isalnum():
            nome = " ".join(split)
            valor = str(nome)
            ok = True
        else: 
            print(Fore.RED + Style.BRIGHT + 'Erro: Entrada inválida! Tente Novamente utilizando apenas letras e números.')
        if ok:
            break
    return valor.title()
