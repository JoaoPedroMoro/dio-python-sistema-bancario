import textwrap
from abc import ABC, abstractmethod
from datetime import  datetime

class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""
            Agência da conta: {conta.agencia}, \n
            Número da conta: {conta.numero}, \n
            Titular da conta: {conta.cliente.nome}, \n
            Saldo da conta: R$ {conta.saldo:.2f}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class UsuarioIterador:
    def __init__(self, usuarios):
        self.usuarios = usuarios
        self._index = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            usuario = self.usuarios[self._index]
            return f"""
            CPF: {usuario.cpf},\n
            Nome: {usuario.nome},\n
            Data de nascimento: {usuario.data_nascimento},\n
            Endereço: {usuario.endereco}
              """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0
        
    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("Você excedeu o número de transações permitidas para hoje!")
            return
            
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
    def __str__(self):
        return f"""
              CPF: {self.cpf},\n
              Nome: {self.nome},\n
              Data de nascimento: {self.data_nascimento},\n
              Endereço: {self.endereco}
              """


class Conta:
    
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        
        if valor > saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("A operação de saque foi realizada com sucesso!")
            return True
        else:
            print("A operação falhou! O valor informado é inválido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("A operação de depósito foi realizada com sucesso!")
            return True
        else:
            print("O depósito falhou! O valor informado é inválido.")
            return False
 
          
class ContaCorrente(Conta):
    
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque
        
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        if numero_saques > self._limite_saque:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > self._limite:
            print("Operação falhou! O valor do saque excede o limite.")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
        Agência: {self.agencia},\n
        Conta corrente: {self.numero},\n
        Cliente: {self.cliente.nome}
        """


class Historico:
    
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao
                
    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d-%m-%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):
    
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    
class Deposito(Transacao):
    
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return envelope
    

@log_transacao
def deposito(usuarios):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtro_usuarios(cpf, usuarios)
    
    if not cliente:
        print(f"O cliente com o cpf {cpf} não foi encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)   


@log_transacao
def saque(usuarios):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtro_usuarios(cpf, usuarios)
    
    if not cliente:
        print(f"O cliente com o cpf {cpf} não foi encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao) 


@log_transacao
def extrato(usuarios):
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtro_usuarios(cpf, usuarios)
    
    if not cliente:
        print(f"O cliente com o cpf {cpf} não foi encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n---------------- EXTRATO ----------------")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n R$ {transacao['valor']:.2f}"
            
    if not tem_transacao:
        extrato = "Não foram realizadas transações."
            
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("------------------------------------------")


@log_transacao
def criar_conta(numero_conta, usuarios, contas):
    
    cpf = input("Informe o CPF do usuário que irá abrir uma conta: ")
    usuario = filtro_usuarios(cpf, usuarios)
    
    if not usuario:
        print(f"O cliente com o CPF {cpf} não foi encontrado.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=usuario, numero=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    
    print(f"A conta para o CPF {cpf} foi criada com sucesso!")


@log_transacao
def criar_cliente(usuarios):
    
    cpf = input("Informe o CPF do usuário que irá abrir uma conta: ")
    while len(cpf) != 11:
        print("CPF inválido! O CPF não tem 11 números.")
        cpf = input("Informe apenas os números do cpf: ")
        
    usuario = filtro_usuarios(cpf, usuarios)
    
    if usuario:
        print(f"O cliente com o CPF {cpf} já existe.")
        return

    nome = input("Informe o nome completo: ")
    
    data_nascimento = input("Forneça a data de nascimento no formato dd/mm/aaaa: ")
    while len(data_nascimento) != 10 and data_nascimento[2] != "/" and data_nascimento[5] != "/":
        data_nascimento = input("Data de nascimento inválida. Forneça a data de nascimento no formato dd/mm/aaaa: ")
    
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    usuarios.append(cliente)

    print(f"O cliente com o CPF {cpf} foi criado com sucesso!")


def filtro_usuarios(cpf, usuarios):
    clientes_filtrados = [cliente for cliente in usuarios if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Esse cliente não tem conta")
        return 
    
    return cliente.contas[0]


def listar_contas(contas):
    for conta in ContaIterador(contas):
        print(f"""
              ------------ *** ------------
              {conta}
              ------------ *** ------------
              """)


def listar_usuarios(usuarios):
    for usuario in UsuarioIterador(usuarios):
        print(f"""
              ------------ *** ------------
              {usuario}
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
    usuarios = []
    contas = []
    
    while True:
        menu()
        opcao = int(input("Digite o número da operação você deseja realizar: "))

        if opcao == 1:
            deposito(usuarios)
        elif opcao == 2:
            saque(usuarios)
        elif opcao == 3:
            extrato(usuarios)
        elif opcao == 4:
            criar_cliente(usuarios)
        elif opcao == 5:
            num_conta = len(contas) + 1
            criar_conta(num_conta, usuarios, contas)
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
