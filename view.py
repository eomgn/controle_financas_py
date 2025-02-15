from models import Conta, engine,  Bancos, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date, timedelta

# criando uma função para criar uma conta, a função recebe um objeto conta como argumento e retorna o objeto conta
# a função cria uma sessão com o banco de dados,  adiciona o objeto conta ao banco de dados commita o que foi adicionado e atualiza o objeto conta
# depois reseta o estado do objeto
def criar_conta(conta: Conta):
    with Session(engine) as session:
        # criando uma variavel statement que recebe a função select importada do sqlmodel
        # com o argumento Conta e o campo banco igual ao campo banco do objeto conta a variavel results recebe a execução da variavel statement
        statement = select(Conta).where(Conta.banco == conta.banco)
        results = session.exec(statement).all()

        # se results for verdadeiro, printa "Conta já existe" e retorna
        if results:
            print("Conta já existe")
            return 

        # se results não for verdadeiro, adiciona o objeto conta ao banco de dados, commita o que foi adicionado e retorna o objeto conta  
        session.add(conta) # adicionando ao banco de dados o objeto conta
        session.commit() # commitando o que foi adicionado

        return conta

# criando uma função para listar as contas, a função não recebe argumentos e retorna os resultados  
def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
        return results

# criando uma função para desativar a conta, a função recebe um id como argumento
# a função cria uma sessão com o banco de dados, a variavel statement recebe a função select importada do sqlmodel com o argumento Conta e o campo id igual ao campo id passado como argumento
# se o valor da conta for maior que 0, printa "Conta com saldo não pode ser desativada" e retorna se o valor da conta não for maior que 0, o campo status da conta é alterado para Status.INATIVO e o que foi alterado é commitado
def desativar_conta(id: int):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first()

        if conta.valor > 0:
            raise ValueError("Conta com saldo não pode ser desativada")
        
        conta.status = Status.INATIVO
        session.commit()

# criando uma função para transferir saldo, a função recebe 3 argumentos, id_conta_origem, id_conta_destino e valor
# a função cria uma sessão com o banco de dados, a variavel statement recebe a função select importada do sqlmodel com o argumento Conta e o campo id igual ao campo id passado como argumento a variavel conta_origem recebe a execução da variavel statement se o valor da conta_origem for menor que o valor passado como argumento, printa "Saldo insuficiente" e retorna a variavel statement recebe a função select importada do sqlmodel com o argumento Conta e o campo id igual ao campo id passado como argumento
# a variavel conta_destino recebe a execução da variavel statement o valor da conta_origem é subtraido pelo valor passado como argumento e o valor da conta_destino é somado pelo valor passado como argumento
def transferir_saldo(id_conta_origem, id_conta_destino, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id_conta_origem)
        conta_origem = session.exec(statement).first()

        if conta_origem.valor < valor:
            raise ValueError("Saldo insuficiente")
        
        statement = select(Conta).where(Conta.id == id_conta_destino)
        conta_destino = session.exec(statement).first()

        conta_origem.valor -= valor
        conta_destino.valor += valor

        session.commit()

# criando uma função para movimentar dinheiro, a função recebe um objeto historico como argumento
# a função cria uma sessão com o banco de dados, a variavel statement recebe a função select importada do sqlmodel com o argumento Conta e o campo id igual ao campo conta_id do objeto historico a variavel conta recebe a execução da variavel statement se o tipo do objeto historico for Tipos.ENTRADA, o valor da conta é somado pelo valor do objeto historico
# se o tipo do objeto historico não for Tipos.ENTRADA e o valor da conta for menor que o valor do objeto historico, printa "Saldo insuficiente" se o tipo do objeto historico não for Tipos.ENTRADA e o valor da conta for maior ou igual ao valor do objeto historico, o valor da conta é subtraido pelo valor do objeto historico
# o objeto historico é adicionado ao banco de dados e o que foi adicionado é commitado
def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == historico.conta_id)
        conta = session.exec(statement).first()

        #TODO: Validar se a conta esta ativa.
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente")
            conta.valor -= historico.valor

        session.add(historico)
        session.commit()
        return historico    

# criando uma função para total de contas, a função não recebe argumentos
# a função cria uma sessão com o banco de dados, a variavel statement recebe a função select importada do sqlmodel com o argumento Conta a variavel contas recebe a execução da variavel statement a variavel total recebe 0
# para cada conta em contas, o total é somado pelo valor da conta e o total é printado
def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        total = 0

        for conta in contas:
            total += conta.valor

        return print(float(total))

# criando uma função para buscar historico entre datas, a função recebe duas datas como argumento
# a função cria uma sessão com o banco de dados, a variavel statement recebe a função select importada do sqlmodel com o argumento Historico e o campo data maior ou igual a data_inicial e o campo data menor ou igual a data_final a variavel results recebe a execução da variavel statement e retorna os resultados
def buscar_historico_entre_datas(data_inicial, data_final):
    with Session(engine) as session:
        statement = select(Historico).where(Historico.data >= data_inicial, Historico.data <= data_final)
        results = session.exec(statement).all()
        return results

### -----------------------------------

# criando um objeto conta 
conta = Conta(valor=0, banco=Bancos.ITAU)

#### chamando a função criar_conta e passando o objeto conta como argumento
#criar_conta(conta)

#### chamando a função desativar_conta passando o id como parametros
# desativar_conta(3)

#### chamando a função listar_contas e passando o id como parametros
#transferir_saldo(1, 2, 100)

### criando um objeto historico e chamando a funcao movimentar_dinheiro passando o objeto historico como parametro
# historico = Historico(conta_id=1, tipo=Tipos.ENTRADA, valor=50, data=date.today())
# movimentar_dinheiro(historico)

### chamando a função total_contas
#total_contas()

### chamando a função buscar_historico_entre_datas para buscar o historico entre as datas passadas como argumento
# x = buscar_historico_entre_datas(date.today() - timedelta(days=1), (date.today()) + timedelta(days=1))
# print(x)

# -------------------------------

# Graficos

# criando uma função para criar um gráfico por conta
# a função cria uma sessão com o banco de dados, a variavel statement recebe a função select importada do sqlmodel com o argumento Conta e o campo status igual a Status.ATIVO
# a variavel contas recebe a execução da variavel statement a variavel bancos recebe uma lista vazia para cada i em contas, o valor do banco é adicionado a lista bancos a variavel total recebe uma lista vazia para cada i em contas, o valor é adicionado a lista total
# importa a biblioteca matplotlib.pyplot como plt cria um gráfico de barras com os bancos e os valores
def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status==Status.ATIVO)
        contas = session.exec(statement).all()

        bancos = []
        for i in contas:
            bancos.append(i.banco.value)

        total = []
        for i in contas:
            total.append(i.valor)

        
        import matplotlib.pyplot as plt 
        plt.bar(bancos, total)
        plt.show()

# criar_grafico_por_conta()