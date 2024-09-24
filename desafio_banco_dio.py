import datetime

# Variáveis globais
saldo = 0.0
saques = []
limite_saque_diario = 500
LIMITE_SAQUE = 3  # Limite de saques por dia

def depositar():
    global saldo
    valor = float(input("Digite o valor que deseja depositar: "))
    if valor > 0:
        saldo += valor
        saques.append({'data': datetime.date.today(), 'valor': valor, 'tipo': 'Depósito'})
        print(f"Depósito de R${valor:.2f} realizado com sucesso!")
    else:
        print("Valor de depósito inválido.")

def sacar():
    global saldo
    hoje = datetime.date.today()
    
    # Filtra os saques feitos hoje
    saques_hoje = [s for s in saques if s['data'] == hoje and s['tipo'] == 'Saque']
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
        saques.append({'data': hoje, 'valor': valor, 'tipo': 'Saque'})
        print(f"Saque de R${valor:.2f} realizado com sucesso!")

def exibir_extrato():
    print("\n--- Extrato ---")
    if not saques:
        print("Não foram realizadas movimentações.")
    else:
        for saque in saques:
            print(f"Data: {saque['data']}, Tipo: {saque['tipo']}, Valor: R${saque['valor']:.2f}")
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
