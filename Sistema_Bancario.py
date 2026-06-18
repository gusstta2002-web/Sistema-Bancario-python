AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR = 500

usuarios = []
contas = []


def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11


def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_usuario(usuarios):
    cpf = input("Informe o CPF, somente números: ")

    if not validar_cpf(cpf):
        print("CPF inválido. Digite exatamente 11 números.")
        return

    if filtrar_usuario(cpf, usuarios):
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereço: ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuário criado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        print("Conta criada com sucesso!")
    else:
        print("Usuário não encontrado. Crie o usuário antes de criar a conta.")


def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print("=" * 40)
        print(f"Agência: {conta['agencia']}")
        print(f"Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Valor inválido para depósito.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, numero_saques, limite_saques, limite_valor):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite_valor
    excedeu_saques = numero_saques >= limite_saques

    if valor <= 0:
        print("Valor inválido para saque.")
    elif excedeu_saldo:
        print("Saldo insuficiente.")
    elif excedeu_limite:
        print(f"O valor máximo por saque é R$ {limite_valor:.2f}.")
    elif excedeu_saques:
        print("Número máximo de saques atingido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=============================")


def ler_valor(mensagem):
    try:
        return float(input(mensagem))
    except ValueError:
        print("Valor inválido. Digite um número.")
        return 0


def menu():
    return """
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q] Sair

=> """


saldo = 0
extrato = ""
numero_saques = 0

while True:
    opcao = input(menu()).lower()

    if opcao == "d":
        valor = ler_valor("Informe o valor do depósito: ")
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = ler_valor("Informe o valor do saque: ")
        saldo, extrato, numero_saques = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
            limite_valor=LIMITE_VALOR
        )

    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)

    elif opcao == "nu":
        criar_usuario(usuarios)

    elif opcao == "nc":
        numero_conta = len(contas) + 1
        criar_conta(AGENCIA, numero_conta, usuarios, contas)

    elif opcao == "lc":
        listar_contas(contas)

    elif opcao == "q":
        print("Obrigado por usar nosso sistema bancário.")
        break

    else:
        print("Operação inválida. Tente novamente.")