from abc import ABC, abstractmethod
from datetime import datetime

# ========== Histórico ==========
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

# ========== Transação ==========
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

# ========== Conta ==========
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        if valor <= 0 or valor > self.saldo:
            print("Saque inválido ou saldo insuficiente.")
            return False
        self.saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Depósito inválido.")
            return False
        self.saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        return True

# ========== Conta Corrente ==========
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques excedido.")
            return False
        if valor > self.limite:
            print("Valor excede o limite por saque.")
            return False
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False

# ========== Cliente e Pessoa Física ==========
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# ========== Funções auxiliares ==========
def localizar_cliente(cpf, clientes):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def menu():
    print("\n=========== MENU BANCO ==========")
    print("[1] Novo usuário")
    print("[2] Nova conta")
    print("[3] Depositar")
    print("[4] Sacar")
    print("[5] Extrato")
    print("[6] Listar contas")
    print("[0] Sair")
    return input("Escolha uma opção: ")

# ========== Menu principal ==========
def main():
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "1":
            cpf = input("CPF: ")
            if localizar_cliente(cpf, clientes):
                print("Usuário já cadastrado.")
                continue

            nome = input("Nome: ")
            nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço: ")

            cliente = PessoaFisica(nome, cpf, nascimento, endereco)
            clientes.append(cliente)
            print("Usuário criado com sucesso!")

        elif opcao == "2":
            cpf = input("CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente:
                print("Cliente não encontrado.")
                continue

            conta = ContaCorrente(cliente, numero=numero_conta)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            numero_conta += 1
            print("Conta criada com sucesso!")

        elif opcao == "3":
            cpf = input("CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada.")
                continue

            valor = float(input("Valor do depósito: "))
            transacao = Deposito(valor)
            cliente.realizar_transacao(cliente.contas[0], transacao)

        elif opcao == "4":
            cpf = input("CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada.")
                continue

            valor = float(input("Valor do saque: "))
            transacao = Saque(valor)
            cliente.realizar_transacao(cliente.contas[0], transacao)

        elif opcao == "5":
            cpf = input("CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada.")
                continue

            conta = cliente.contas[0]
            print("\n======= EXTRATO =======")
            for t in conta.historico.transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
            print(f"Saldo atual: R$ {conta.saldo_atual():.2f}")

        elif opcao == "6":
            for conta in contas:
                print("=" * 30)
                print(f"Agência: {conta.agencia}")
                print(f"Número: {conta.numero}")
                print(f"Titular: {conta.cliente.nome}")

        elif opcao == "0":
            print("Obrigado por utilizar nosso sistema bancário!")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
