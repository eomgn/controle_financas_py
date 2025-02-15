# importando as bibliotecas necessárias
from sqlmodel import SQLModel, Field, create_engine, Relationship
from enum import Enum
from datetime import date

# criando uma classe Enum para os bancos
class Bancos(Enum):
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    BANCO_DO_BRASIL = 'Banco do Brasil'
    ITAU = 'Itau'
    BRADESCO = 'Bradesco'
    INTER = 'Inter'

# criando uma classe Enum para os status
class Status(Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'

# criando uma classe Enum para os tipos
class Tipos(Enum):
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'

# criando uma classe conta que herda de SQLModel
# e possui os campos id, valor, banco e status
class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    valor: float
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)

class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date

# criando uma engine para o banco de dados
# e criando as tabelas
sqlite_file_name = "database.db"  
sqlite_url = f"sqlite:///{sqlite_file_name}"  

# criando uma variavel engine que recebe a função create_engine importada do sqlmodel
# com o argumento sqlite_url e echo=True para mostrar os logs
engine = create_engine(sqlite_url, echo=True)  

# criando uma função para criar o banco de dados e as tabelas
# a função create_all é importada do metadata
def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)

# se o arquivo for executado diretamente, a função create_db_and_tables é chamada
if __name__ == "__main__":
    create_db_and_tables()