import pytz
from datetime import datetime

# Listas para armazenar usuários e contas
usuarios = []
contas = []

# Função para calcular a idade
def calcular_idade(data_nascimento):
    nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
    hoje = datetime.now()
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    return idade

# Função para cadastrar um usuário (cliente)
def cadastrar_usuario():
    while True:
        nome = input("Informe o nome do usuário: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        cpf = input("Informe o CPF (apenas números): ").strip()
        endereco = input("Informe o endereço (logradouro, número-bairro-cidade/sigla do estado): ")

        # Verifica se o CPF já está cadastrado
        if any(usuario['cpf'] == cpf for usuario in usuarios):
            print("Erro: Já existe um usuário cadastrado com esse CPF.")
            continue
        
        # Calcula a idade
        idade = calcular_idade(data_nascimento)
        if idade < 18:
            print("Erro: O usuário deve ter 18 anos ou mais para abrir uma conta.")
            continue

        usuarios.append({
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
            "contas": []  # Inicializa a lista de contas
        })
        print(f"Usuário cadastrado: {usuarios[-1]}")
        break

# Função para cadastrar uma conta bancária vinculada a um usuário
def cadastrar_conta_bancaria():
    usuario_cpf = input("Informe o CPF do usuário para vincular a conta: ").strip()
    usuario = next((u for u in usuarios if u['cpf'] == usuario_cpf), None)

    if usuario:
        # Define número da agência e número da conta sequencial
        numero_agencia = "0001"
        numero_conta = len(contas) + 1  # Sequencial começando em 1

        conta = {
            "numero_agencia": numero_agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,  # Inicializa o saldo da conta
            "extrato": {'depositos': [], 'saques': []}  # Inicializa o extrato
        }

        contas.append(conta)  # Armazena a conta na lista de contas
        usuario['contas'].append(conta)  # Adiciona a conta ao usuário
        print(f"Conta cadastrada: {conta}")
    else:
        print("Usuário não encontrado.")

# Função para listar usuários cadastrados com suas contas
def listar_usuarios():
    if usuarios:
        print("\n============== LISTA DE USUÁRIOS ==============")
        for usuario in usuarios:
            contas_usuario = usuario.get('contas', [])
            conta_info = ', '.join([f"Ag: {conta['numero_agencia']} - Conta: {conta['numero_conta']} - Saldo: R$ {conta['saldo']:.2f}" for conta in contas_usuario])
            if conta_info:
                print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}, Endereço: {usuario['endereco']}, Contas: [{conta_info}]")
            else:
                print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}, Endereço: {usuario['endereco']}, Contas: [Nenhuma]")
    else:
        print("Nenhum usuário cadastrado.")

def menu():
    return """
    [c] Cadastrar Usuário
    [b] Cadastrar Conta Bancária
    [l] Listar Usuários
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    => """

# Função de depósito
def depositar():
    numero_conta = int(input("Informe o número da conta para depósito: "))
    conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)

    if conta:
        valor = input("Informe o valor do depósito: ")
        try:
            valor = float(valor)
            if valor > 0:
                data_hora = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d-%m-%Y %H:%M:%S")
                conta['saldo'] += valor
                conta['extrato']['depositos'].append(f"Depósito: R$ {valor:.2f} em {data_hora}")
                print(f"Depósito realizado com sucesso! Novo saldo: R$ {conta['saldo']:.2f}")
            else:
                print("Operação falhou! O valor informado é inválido.")
        except ValueError:
            print("Operação falhou! O valor informado deve ser um número.")
    else:
        print("Conta não encontrada.")

# Função de saque
def sacar():
    numero_conta = int(input("Informe o número da conta para saque: "))
    conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)

    if conta:
        valor = input("Informe o valor do saque: ")
        try:
            valor = float(valor)
            if valor > 0:
                if valor > conta['saldo']:
                    print("Operação falhou! Você não tem saldo suficiente.")
                else:
                    data_hora = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d-%m-%Y %H:%M:%S")
                    conta['saldo'] -= valor
                    conta['extrato']['saques'].append(f"Saque: R$ {valor:.2f} em {data_hora}")
                    print(f"Saque realizado com sucesso! Novo saldo: R$ {conta['saldo']:.2f}")
            else:
                print("Operação falhou! O valor informado é inválido.")
        except ValueError:
            print("Operação falhou! O valor informado deve ser um número.")
    else:
        print("Conta não encontrada.")

# Função de exibir extrato
def exibir_extrato():
    numero_conta = int(input("Informe o número da conta para visualizar o extrato: "))
    conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)

    if conta:
        print("\n============== EXTRATO ==============")
        print(f"Conta: Ag: {conta['numero_agencia']} - Conta: {conta['numero_conta']}")
        print("\n================ Depositos ================")
        if conta['extrato']['depositos']:
            for dep in conta['extrato']['depositos']:
                print(f"  {dep}")
        else:
            print("Não foram realizados depósitos.")
        print("\n================ Saques ================")
        if conta['extrato']['saques']:
            for saq in conta['extrato']['saques']:
                print(f"  {saq}")
        else:
            print("Não foram realizados saques.")

        print("\n================ Saldo ================")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("===========================================")
    else:
        print("Conta não encontrada.")

def main():
    while True:
        opcao = input(menu())

        if opcao == "c":
            cadastrar_usuario()
        elif opcao == "b":
            cadastrar_conta_bancaria()  # Chama a função para cadastrar a conta
        elif opcao == "l":
            listar_usuarios()  # Chama a função para listar usuários
        elif opcao == "d":
            depositar()  # Chama a função de depósito
        elif opcao == "s":
            sacar()  # Chama a função de saque
        elif opcao == "e":
            exibir_extrato()  # Chama a função de exibir extrato
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()


# Esse projeto não está relacionado ao meu primeiro, pois segui a orientanção de pegar o que foi solicitado .
# Criei o que solicitao, que era no menu, incluir a opção de criar usuario, criar conta, porém adicionei um novo item de listar todas as contas
# Coloquei também a opção de verificar se o cliente tem a idade minima para abrir conta.
# Separei a opçaõ de listar extrato ,deposito e saque por conta.
# Esperoa ter atendido.
# Marciano Pinheiro da Silva