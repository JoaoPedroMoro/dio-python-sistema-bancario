saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    print("""Operações possíveis:
          Depositar
          Sacar
          Extrato
          Sair""")
    opcao = input("Digite qual operação você deseja realizar: ")

    if opcao == "Depositar":
        valor = float(input("Informe qual valor você deseja depositar: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "Sacar":
        valor = float(input("Informe qual valor você deseja sacar: "))

        if valor > saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "Extrato":
        print("\n---------------- EXTRATO ----------------")
        if extrato == "":
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
        print("------------------------------------------")
    elif opcao == "Sair":
        break

    else:
        print("Operação inválida, por favor digite novamente a operação desejada.")