from db import Session, Base, engine
from models import DadoCLP
from threading import Thread, Lock
from datetime import datetime

class GuardarDados:
    """
    Implementar a Gravação de Dados
    """
    def __init__(self):
        """
        Construtor
        """
        self._session = Session()
        Base.metadata.create_all(engine)
        self._lock = Lock()
        #self.thread_guardar_dados = Thread(target=self.processar_dados)

    def guardar_dados(self, dados: dict):
        """
        Recebe e armazena dados no banco de dados
        """
        try:
            novo_dado = DadoCLP(**dados)
            self._lock.acquire()
            self._session.add(novo_dado)
            self._session.commit()
            self._lock.release()
            print("Dados armazenados com sucesso!")
        except Exception as e:
            self._session.rollback()
            print(f"Erro ao guardar dados: {e}")
        finally:
            self._session.close()

    def buscar_dados(self,init,final):
        """
        Busca dados no banco de dados
        """
        try:
           print("Busca de dados iniciada")
           while True:
               init = datetime.strptime(init, '%d/%m/%Y %H:%M:%S')
               final = datetime.strptime(final, '%d/%m/%Y %H:%M:%S')
               self._lock.acquire()
               result = self._session.query(DadoCLP).filter(DadoCLP.timestamp.between(init,final)).all()
               self._lock.release()

               result_listaformatada = [obj.get_DadosDB() for obj in result] #Não precisa pra interface
               #print(tabulate(result_listaformatada,headers=DadoCLP.__table__.columns.keys())) #Não precisa pra interface

        except Exception as e:
            print ("Erro na busca de dados: ",e.args)