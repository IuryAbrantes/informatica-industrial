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

    
    
    def buscar_dados(self, cols, init_t, final_t):
        """
        
        """
        init = datetime.strptime(init_t, '%d/%m/%Y %H:%M:%S')
        final = datetime.strptime(final_t, '%d/%m/%Y %H:%M:%S')

        self._lock.acquire()
        result = self._session.query(DadoCLP).filter(DadoCLP.timestamp.between(init,final)).all()
        self._lock.release()

        return result
    
    def buscar_dadosa(self, cols, init_t, final_t):
        """
        Busca dados no banco de dados com base nas colunas especificadas e no intervalo de tempo.
        
        :param cols: Lista de colunas a serem filtradas.
        :param init: Data/hora inicial no formato 'dd/mm/yyyy HH:MM:SS'.
        :param final: Data/hora final no formato 'dd/mm/yyyy HH:MM:SS'.
        """
        try:
            print("Busca de dados iniciada")

            # Converte as strings de data/hora para objetos datetime
            init = datetime.strptime(init_t, '%d/%m/%Y %H:%M:%S')
            final = datetime.strptime(final_t, '%d/%m/%Y %H:%M:%S')

            # Filtra as colunas válidas
            colunas_validas = [col for col in cols if hasattr(DadoCLP, col)]
            if not colunas_validas:
                print("Nenhuma coluna válida fornecida.")
                return []

            # Adiciona a coluna 'timestamp' à lista de colunas, se não estiver presente
            if 'timestamp' not in colunas_validas:
                colunas_validas.append('timestamp')

            # Cria a lista de colunas para a consulta
            colunas_consulta = [getattr(DadoCLP, col) for col in colunas_validas]

            # Executa a consulta usando with_entities
            self._lock.acquire()
            result = self._session.query(*colunas_consulta).filter(
                DadoCLP.timestamp.between(init, final)
            ).all()
            self._lock.release()

            # Formata o resultado em uma lista de dicionários
            result_listaformatada = [dict(zip(colunas_validas, row)) for row in result]

            return result_listaformatada

        except Exception as e:
            print("Erro na busca de dados: ", e.args)
            return []