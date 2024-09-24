import datetime

# Variáveis globais
saldo = 0.0
transacoes = []  # Lista para armazenar todas as transações
limite_saque_diario = 500
LIMITE_SAQUE = 3  # Limite de saques por dia
LIMITE_TOTAL_TRANSAÇÕES = 10  # Limite total de transações (saques + depósitos)

def formatar_data_hora(data_hora):
    return data_hora.strftime("%d/%m/%Y %H:%M:%S")

def depositar():
    global saldo
    if len(transacoes) >= LIMITE_TOTAL_TRANSAÇÕES:
        print("Você já atingiu o limite de 10 transações permitidas no dia de hoje.")
        return

    valor = float(input("Digite o valor que deseja depositar: "))
    if valor > 0:
        saldo += valor
        transacoes.append({'data': datetime.datetime.now(), 'valor': valor, 'tipo': 'Depósito'})
        print(f"Depósito de R${valor:.2f} realizado com sucesso!")
    else:
        print("Valor de depósito inválido.")

def sacar():
    global saldo
    hoje = datetime.date.today()
    
    if len(transacoes) >= LIMITE_TOTAL_TRANSAÇÕES:
        print("Você já atingiu o limite de 10 transações permitidas no dia de hoje.")
        return
    
    # Filtra os saques feitos hoje
    saques_hoje = [s for s in transacoes if s['data'].date() == hoje and s['tipo'] == 'Saque']
    valor_sacado_hoje = sum([s['valor'] for s in saques_hoje])
    
    print(f"Você já sacou R${valor_sacado_hoje:.2f} hoje. Limite restante: R${limite_saque_diario - valor_sacado_hoje:.2f}")
    
    if len(saques_hoje) >= LIMITE_SAQUE:
        print("Você já atingiu o limite de 3 saques diários.")
        return

    valor = float(input("Digite o valor que deseja sacar: "))
    
    if valor + valor_sacado_hoje > limite_saque_diario:
        print(f"O valor excede o limite de saque diário. Você só pode sacar mais R${limite_saque_diario - valor_sacado_hoje:.2f}.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    else:
        saldo -= valor
        transacoes.append({'data': datetime.datetime.now(), 'valor': valor, 'tipo': 'Saque'})
        print(f"Saque de R${valor:.2f} realizado com sucesso!")

def exibir_extrato():
    print("\n--- Extrato ---")
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            data_hora_formatada = formatar_data_hora(transacao['data'])
            print(f"Data: {data_hora_formatada}, Tipo: {transacao['tipo']}, Valor: R${transacao['valor']:.2f}")
    print(f"Saldo atual: R${saldo:.2f}\n")

def menu_bancario():
    while True:
        print("\n--- Menu Bancário ---")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Extrato")
        print("4. Encerrar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            depositar()
        elif opcao == '2':
            sacar()
        elif opcao == '3':
            exibir_extrato()
        elif opcao == '4':
            print("Sessão encerrada.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    print("Bem-vindo ao Sistema Bancário do Marciano")
    menu_bancario()

if __name__ == '__main__':
    main()
