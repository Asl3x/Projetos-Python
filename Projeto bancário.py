menu = """

[0] Depositar
[1] Sacar
[2] Extrato
[3] Limites Diários
[s] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
numero_deposito = 0
LIMITE_SAQUES = 3
LIMITE_DEPOSITO = 3

while True:

    opcao = input(menu)

    if opcao == "0":
        valor = float(input("Informe o valor do depósito: "))
        
        excedeu_deposito = numero_deposito >= LIMITE_DEPOSITO        
        
        if excedeu_deposito:
            print("Número de depósitos diário excedido!")
        
        elif valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            numero_deposito +=1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "1":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite por operação.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques diário excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")


    elif opcao == "3":
        print(f"\nSua conta tem o limite de {LIMITE_SAQUES} saques diários", f"e no máximo {LIMITE_DEPOSITO} operações de depósitos diários." )

    elif opcao == "s":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
