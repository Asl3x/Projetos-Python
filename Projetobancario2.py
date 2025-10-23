import textwrap

# Constantes (Melhor usar variáveis globais para os limites, mas vamos passar nas funções para modularizar)
LIMITE_SAQUES = 3
LIMITE_DEPOSITOS = 3
AGENCIA = "0001"

# ==============================================================================
# FUNÇÕES DE OPERAÇÃO BANCÁRIA
# ==============================================================================

def depositar(saldo, valor, extrato, numero_deposito, limite_deposito):
    """Realiza a operação de depósito na conta."""
    
    # Tentativa de converter o valor para float
    try:
        valor = float(valor)
    except ValueError:
        print("\n@@@ Operação falhou! Valor informado é inválido. Digite um número. @@@")
        return saldo, extrato, numero_deposito

    excedeu_deposito = numero_deposito >= limite_deposito
    
    if excedeu_deposito:
        print("\n@@@ Operação falhou! Número de depósitos diário excedido. @@@")
    
    elif valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        numero_deposito += 1
        print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
    
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido (deve ser positivo). @@@")

    return saldo, extrato, numero_deposito


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Realiza a operação de saque na conta."""
    
    # Tentativa de converter o valor para float
    try:
        valor = float(valor)
    except ValueError:
        print("\n@@@ Operação falhou! Valor informado é inválido. Digite um número. @@@")
        # Retorna os valores inalterados
        return saldo, extrato, numero_saques

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite por operação (R$ 500.00). @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques diário excedido (3 saques). @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
    
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido (deve ser positivo). @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """Exibe o extrato da conta, mostrando todas as movimentações e o saldo atual."""
    
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


# ==============================================================================
# FUNÇÕES DE CADASTRO
# ==============================================================================

def filtrar_usuario(cpf, usuarios):
    """Retorna o usuário que possui o CPF informado, ou None."""
    
    # Remove pontos e traços do CPF para comparação
    cpf = cpf.replace(".", "").replace("-", "")
    
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios):
    """Permite o cadastro de um novo usuário (cliente)."""
    
    # Garante que o CPF tenha o formato para fácil visualização
    cpf = input("Informe o CPF (somente números): ")
    
    # Tenta remover os caracteres para padronizar
    cpf_limpo = cpf.replace(".", "").replace("-", "")

    # Verifica se o CPF já existe
    usuario = filtrar_usuario(cpf_limpo, usuarios)

    if usuario:
        print("\n@@@ Operação falhou! Já existe usuário com este CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf_limpo, "endereco": endereco})

    print("\n=== Usuário criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios):
    """Permite a criação de uma nova conta corrente vinculada a um usuário existente."""
    
    cpf = input("Informe o CPF do usuário (somente números): ")
    
    # Tenta remover os caracteres para padronizar
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    
    usuario = filtrar_usuario(cpf_limpo, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None


def listar_contas(contas):
    """Exibe a lista de todas as contas criadas."""
    
    if not contas:
        print("\n@@@ Não há contas cadastradas. @@@")
        return

    for conta in contas:
        # Usa textwrap.dedent para formatar a string de forma limpa
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 30)
        print(textwrap.dedent(linha))

# ==============================================================================
# MENU E PROGRAMA PRINCIPAL
# ==============================================================================

def menu():
    """Função para exibir e retornar a opção escolhida no menu."""
    
    menu_str = """\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [c]\tCriar Usuário
    [n]\tNova Conta
    [l]\tListar Contas
    [q]\tSair
    => """
    
    # textwrap.dedent remove a indentação excessiva da string do menu
    return input(textwrap.dedent(menu_str))


def main():
    """Função principal do programa."""
    
    # Inicializando as estruturas de dados
    usuarios = []
    contas = []
    
    # Variáveis da conta
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    numero_deposito = 0
    numero_conta = 1 # Contador para o número da próxima conta

    while True:
        opcao = menu()

        if opcao == "d":
            valor = input("Informe o valor do depósito: ")
            saldo, extrato, numero_deposito = depositar(saldo, valor, extrato, numero_deposito, LIMITE_DEPOSITOS)

        elif opcao == "s":
            valor = input("Informe o valor do saque: ")
            # Usando kwargs (argumentos nomeados) para facilitar a leitura e evitar erros
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            # Usando positional-only (/) e keyword-only (*) para reforçar a assinatura
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "c":
            criar_usuario(usuarios)

        elif opcao == "n":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                numero_conta += 1 # Incrementa o contador da conta para a próxima

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por utilizar nossos serviços!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


# Execução do programa
if __name__ == "__main__":
    main()