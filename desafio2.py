def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("A operação de depósito foi realizada com sucesso!")
    else:
        print("O depósito falhou! O valor informado é inválido.")
        
    return saldo, extrato


def saque(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("A operação de saque foi realizada com sucesso!")
    else:
        print("A operação falhou! O valor informado é inválido.")
        
    return saldo, extrato


def extrato(saldo, /, *, extrato):
    print("\n---------------- EXTRATO ----------------")
    if extrato == "":
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
    print("------------------------------------------")


def novo_usuario(usuarios):
    cpf = input("Informe apenas os números do cpf: ")
    while len(cpf) != 11:
        print("CPF inválido! O CPF não tem 11 números.")
        cpf = input("Informe apenas os números do cpf: ")
        
    if filtro_usuarios(cpf, usuarios):
        print("Já existe conta criada com esse CPF")
        return usuarios
    
    nome = input("Informe seu nome completo: ")    
    
    data_nascimento = input("Forneça a data de nascimento no formato dd/mm/aaaa: ")
    while len(data_nascimento) != 10 and data_nascimento[2] != "/" and data_nascimento[5] != "/":
        data_nascimento = input("Data de nascimento inválida. Forneça a data de nascimento no formato dd/mm/aaaa: ")
    
    endereco = {}
    endereco["rua"] = input("Informe a rua de residência: ")
    endereco["numero"] = input("Informe o número da residência: ")
    endereco["bairro"] = input("Informe o bairro da residência: ")
    endereco["cidade"] = input("Informe a cidade da residência: ")
    endereco["estado"] = input("Informe o estado da residência: ")
    
    usuarios.append({"nome":nome, "cpf":cpf, "data de nascimento":data_nascimento, "endereço":endereco})
    
    print(f"O usuário de nome {usuarios} foi criado!")
    
    return usuarios


def criar_conta(agencia, nro_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário que irá abrir uma conta: ")
    usuario = filtro_usuarios(cpf, usuarios)
    
    if usuario is not None:
        contas.append({"agencia": agencia, "número da conta": nro_conta, "usuario":usuario})
        print(usuario)
        print(f"A conta para o usuário de nome {usuario['nome']} e cpf {usuario['cpf']} foi criada com sucesso!")
    else:
        print("O CPF informado é inválido ou não existe no sistema.")
        
    return 0


def filtro_usuarios(cpf, usuarios):
    for usuario in usuarios:
        print(usuario['cpf'])
        if usuario["cpf"] == cpf:
            return usuario
    return None


def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(f"""
              ------------ *** ------------
              CPF: {usuario['cpf']},
              Nome: {usuario['nome']},
              Data de nascimento: {usuario['data de nascimento']},
              Endereço: {usuario['endereço']}
              ------------ *** ------------
              """)
        

def listar_contas(contas):
    for conta in contas:
        print(f"""
              ------------ *** ------------
              Agência: {conta['agencia']},
              Número da conta: {conta['número da conta']},
              Usuário: {conta['usuario']['nome']}
              ------------ *** ------------
              """)


def menu():
    print("""Operações possíveis:
            Depósito - 1
            Saque - 2
            Extrato - 3 
            Cadastrar usuário - 4
            Nova conta - 5
            Listar usuários - 6
            Listar contas - 7
            Sair - 8""")

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    while True:
        menu()
        opcao = int(input("Digite o número da operação você deseja realizar: "))

        if opcao == 1:
            valor = float(input("Informe qual valor você deseja depositar: "))
            saldo, extrato = deposito(saldo, valor, extrato)
        elif opcao == 2:
            valor = float(input("Informe qual valor você deseja sacar: "))
            saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite,
                                   numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        elif opcao == 3:
            extrato(saldo, extrato=extrato)
        elif opcao == 4:
            usuarios = novo_usuario(usuarios)
        elif opcao == 5:
            num_conta = len(contas) + 1
            criar_conta(AGENCIA, num_conta, usuarios, contas)
        elif opcao == 6:
            listar_usuarios(usuarios)   
        elif opcao == 7:
            listar_contas(contas) 
        elif opcao == 8:
            break
        else:
            print("Operação inválida, por favor digite novamente a operação desejada.")
        
        
if __name__ == '__main__':
    main()