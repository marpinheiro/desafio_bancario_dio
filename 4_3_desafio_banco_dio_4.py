from datetime import datetime
from abc import ABC, abstractmethod

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

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

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def calcular_idade(self):
        nascimento = datetime.strptime(self.data_nascimento, "%d/%m/%Y")
        hoje = datetime.now()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade

    def pode_abrir_conta(self):
        return self.calcular_idade() >= 18

class Conta:
    def __init__(self, numero_agencia, numero_conta, usuario):
        self.numero_agencia = numero_agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.historico = Historico()  # Adicionando histórico de transações

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

    def exibir_extrato(self):
        print("\n============== EXTRATO ==============")
        print(f"Conta: Ag: {self.numero_agencia} - Conta: {self.numero_conta}")
        print("\n================ Transações ================")
        for transacao in self.historico.transacoes:
            print(f"  {transacao['tipo']}: R$ {transacao['valor']:.2f} em {transacao['data']}")
        print("\n================ Saldo ================")
        print(f"Saldo: R$ {self.saldo:.2f}")
        print("===========================================")

class ContaCorrente(Conta):
    def __init__(self, numero_agencia, numero_conta, usuario, limite=500, limite_saques=3):
        super().__init__(numero_agencia, numero_conta, usuario)
        self.limite = limite
        self.limite_saques = limite_saques
        self.qtd_saques = 0

    def sacar(self, valor):
        if self.qtd_saques < self.limite_saques and valor > 0:
            if valor <= self.saldo + self.limite:
                self.saldo -= valor
                self.qtd_saques += 1
                return True
        return False

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def cadastrar_usuario(self, nome, data_nascimento, cpf, endereco):
        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        if not usuario.pode_abrir_conta():
            print("Erro: O usuário deve ter 18 anos ou mais para abrir uma conta.")
            return None
        self.usuarios.append(usuario)
        print(f"Usuário cadastrado: {usuario.nome}")
        return usuario

    def cadastrar_conta_corrente(self, usuario):
        numero_agencia = "0001"
        numero_conta = len(self.contas) + 1
        conta_corrente = ContaCorrente(numero_agencia, numero_conta, usuario)
        self.contas.append(conta_corrente)
        usuario.contas.append(conta_corrente)
        print(f"Conta Corrente cadastrada: Ag: {conta_corrente.numero_agencia}, Conta: {conta_corrente.numero_conta}")

    def listar_usuarios(self):
        if self.usuarios:
            print("\n============== LISTA DE USUÁRIOS ==============")
            for usuario in self.usuarios:
                conta_info = ', '.join([f"Ag: {conta.numero_agencia} - Conta: {conta.numero_conta} - Saldo: R$ {conta.saldo:.2f}" for conta in usuario.contas])
                print(f"Nome: {usuario.nome}, CPF: {usuario.cpf}, Endereço: {usuario.endereco}, Contas: [{conta_info if conta_info else 'Nenhuma'}]")
        else:
            print("Nenhum usuário cadastrado.")

def menu():
    return """
    [c] Cadastrar Usuário
    [b] Cadastrar Conta Corrente
    [d] Depositar
    [s] Sacar
    [l] Listar Usuários
    [e] Extrato
    [q] Sair
    => """

def main():
    banco = Banco()
    while True:
        opcao = input(menu())

        if opcao == "c":
            nome = input("Informe o nome do usuário: ")
            data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
            cpf = input("Informe o CPF (apenas números): ").strip()
            endereco = input("Informe o endereço (logradouro, número-bairro-cidade/sigla do estado): ")
            banco.cadastrar_usuario(nome, data_nascimento, cpf, endereco)
        elif opcao == "b":
            usuario_cpf = input("Informe o CPF do usuário para vincular a conta: ").strip()
            usuario = next((u for u in banco.usuarios if u.cpf == usuario_cpf), None)
            if usuario:
                banco.cadastrar_conta_corrente(usuario)
            else:
                print("Usuário não encontrado.")
        elif opcao == "d":
            numero_conta = int(input("Informe o número da conta para depósito: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                deposito = Deposito(valor)
                deposito.registrar(conta)
                print(f"Depósito realizado com sucesso! Novo saldo: R$ {conta.saldo:.2f}")
            else:
                print("Conta não encontrada.")
        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta para saque: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                saque = Saque(valor)
                saque.registrar(conta)
                print(f"Saque realizado com sucesso! Novo saldo: R$ {conta.saldo:.2f}")
            else:
                print("Conta não encontrada.")
        elif opcao == "l":
            banco.listar_usuarios()
        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta para visualizar o extrato: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero_conta), None)
            if conta:
                conta.exibir_extrato()
            else:
                print("Conta não encontrada.")
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
