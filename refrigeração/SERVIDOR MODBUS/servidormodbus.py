from pyModbusTCP.server import DataBank, ModbusServer #Importa biblioteca
import random
from time import sleep

class ServidorMODBUS():
    """
    Classe do servidor
    """
    def __init__(self, host_ip, port):
        """
        Construtor do servidor
        """
        self._db = DataBank()  #atributo data bank
        self._server = ModbusServer(host=host_ip,port=port,no_block=True, data_bank = self._db) #atributo server
        self._fator_escala = 100  # Fator de escala

        # Dicionário que associa endereços aos nomes dos valores
        self._endereco_nomes = {
            722: "Status do PID",
            706: "Temperatura da carcaça",
            726: "Corrente R",
            727: "Corrente S",
            728: "Corrente T",
            738: "Potência ativa total",
            742: "Potência reativa total",
            871: "Fator de potência",
            884: "Rotação do motor (RPM)",
            751: "Frequência do compressor",
        }

    def float_to_int(self, valor_float):
        """
        Converte um float para inteiro, aplicando o fator de escala.
        """
        return int(valor_float * self._fator_escala)

    def int_to_float(self, valor_int):
        """
        Converte um inteiro de volta para float, aplicando o fator de escala.
        """
        return valor_int / self._fator_escala

    def run(self):
        """
        Método run para execução do servidor Modbus
        """
        try:
            self._server.start()
            print("Servidor MODBUS em execução")
            while True:
                
                valor_float = {
                    address: random.uniform(0.95 * 400, 1.05 * 400)
                    for address in self._endereco_nomes.keys()
                }

                """
                self._db.set_holding_registers(1216,[random.uniform(float(0.95*400),float(1.05*400))]) #partida selecionada              
                self._db.set_holding_registers(1420,[random.uniform(float(0.95*400),float(1.05*400))]) #torque
                self._db.set_holding_registers(1304,[random.uniform(float(0.95*400),float(1.05*400))]) #valor controle proporcional
                self._db.set_holding_registers(1306,[random.uniform(float(0.95*400),float(1.05*400))]) #controle floategral
                self._db.set_holding_registers(1308,[random.uniform(float(0.95*400),float(1.05*400))]) #controle derivativo
                
                



                self._db.set_holding_registers(1316,[random.uniform(float(0.95*400),float(1.05*400))]) #partida soft-starter
                self._db.set_holding_registers(1319,[random.uniform(float(0.95*400),float(1.05*400))]) #partida direta
                self._db.set_holding_registers(1324,[random.uniform(float(0.95*400),float(1.05*400))]) #selecione o tipo de partida
                self._db.set_holding_registers(1312,[random.uniform(float(0.95*400),float(1.05*400))]) #partida inversor
                self._db.set_holding_registers(1313,[random.uniform(float(0.95*400),float(1.05*400))]) #velocidade inversor
                self._db.set_holding_registers(1330,[random.uniform(float(0.95*400),float(1.05*400))]) #motor lig/deslig
                self._db.set_holding_registers(708,[random.uniform(float(0.95*400),float(1.05*400))])  #Tipo do motor
                self._db.set_holding_registers(1314,[random.uniform(float(0.95*400),float(1.05*400))]) #rampa aceleração inversor
                self._db.set_holding_registers(1315,[random.uniform(float(0.95*400),float(1.05*400))]) #rampa desaceleração inversor                
                self._db.set_holding_registers(1317,[random.uniform(float(0.95*400),float(1.05*400))]) #rampa aceleração soft-starter
                self._db.set_holding_registers(1318,[random.uniform(float(0.95*400),float(1.05*400))]) #rampa desaceleração soft-starter
                self._db.set_holding_registers(1332,[random.uniform(float(0.95*400),float(1.05*400))]) #tipo PID (manual/auto)
                """

                for address, value in valor_float.items():
                    valor_int = self.float_to_int(value)
                    self._db.set_holding_registers(address, [valor_int])

                print("============================")
                print(" Tabela MODBUS")
                for address, name in self._endereco_nomes.items():
                    valor_int = self._db.get_holding_registers(address, 1)[0]
                    decoded_value = self.int_to_float(valor_int)
                    print(f'{name}: {decoded_value:.2f}')
                sleep(1)
        except Exception as e:
            print("Erro: ", e.args)