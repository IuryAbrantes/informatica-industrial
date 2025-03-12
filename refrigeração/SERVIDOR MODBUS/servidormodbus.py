from pyModbusTCP.server import DataBank, ModbusServer #importa biblioteca
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
import random
from time import sleep

class ServidorMODBUS():
    """
    Classe Servidor Modbus
    """

    def __init__(self,host_ip,port): #construtor protegido
        """
        Construtor
        """
        self._db = DataBank() #atributo data bank
        self._server = ModbusServer(host=host_ip,port=port,no_block=True,data_bank = self._db) #atributo server
        
    def run(self): #método run
        """
        Execução servidor Modbus
        """
        try:
            self._server.start()
            print("Servidor MODBUS em execução")
            while True:

                #tipo 4X
                self._db.set_holding_registers(722,[random.randrange(int(0.95*400),int(1.05*400))]) #status do PID
                self._db.set_holding_registers(706,[random.randrange(int(0.95*400),int(1.05*400))]) #temperatura carcaça
                self._db.set_holding_registers(726,[random.randrange(int(0.95*400),int(1.05*400))]) #corrente R
                self._db.set_holding_registers(727,[random.randrange(int(0.95*400),int(1.05*400))]) #corrente S
                self._db.set_holding_registers(728,[random.randrange(int(0.95*400),int(1.05*400))]) #corrente T
                self._db.set_holding_registers(738,[random.randrange(int(0.95*400),int(1.05*400))]) #potencia ativa total
                self._db.set_holding_registers(742,[random.randrange(int(0.95*400),int(1.05*400))]) #potencia reativa total
                self._db.set_holding_registers(871,[random.randrange(int(0.95*400),int(1.05*400))]) #fator de potência
                self._db.set_holding_registers(751,[random.randrange(int(0.95*400),int(1.05*400))]) #frequencia compressor
                self._db.set_holding_registers(710,[random.randrange(int(0.95*400),int(1.05*400))]) #temperatura na saida de ar
                self._db.set_holding_registers(712,[random.randrange(int(0.95*400),int(1.05*400))]) #velocidade na ar
                self._db.set_holding_registers(714,[random.randrange(int(0.95*400),int(1.05*400))]) #vazao do ar
                self._db.set_holding_registers(1216,[random.randrange(int(0.95*400),int(1.05*400))]) #partida selecionada
                self._db.set_holding_registers(1230,[random.randrange(int(0.95*400),int(1.05*400))]) #Status das valvulas
                #Lista: bit0 - Status da Valvula XV-01 e XV-02 Scroll (aberta = 0, fechada =1)
                #Lista: bit1 - Status da Valvula XV-03 e XV-04 Hermetico(aberta = 0, fechada =1)
                
                #Tipo FP
                valor_float= random.uniform(0.95*800, 1.05*1400)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(valor_float)
                payload = builder.to_registers()
                self._db.set_holding_registers(884, payload)#rotacao motor em rpm


                valor_float2= random.uniform(0.95*20, 1.05*50)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(valor_float)
                payload = builder.to_registers()
                self._db.set_holding_registers(1218, payload)#Temperatura TIT-02 (cano vermelho) em ºC

                valor_float3= random.uniform(0.95*20, 1.05*50)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(valor_float)
                payload = builder.to_registers()
                self._db.set_holding_registers(1220, payload)#Temperatura TIT-01 (cano azul) em  ºc

                valor_float4= random.uniform(0.95*-5, 1.05*5)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(valor_float)
                payload = builder.to_registers()
                self._db.set_holding_registers(1222, payload)#Pressao PIT-02 (cano vermelho) em ºC

                valor_float2= random.uniform(0.95*-5, 1.05*5)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(valor_float)
                payload = builder.to_registers()
                self._db.set_holding_registers(1224, payload)#Pressao PIT-01 (cano azul) em ºC

                valor_float2= random.uniform(0.95*-5, 1.05*5)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(valor_float)
                payload = builder.to_registers()
                self._db.set_holding_registers(1218, payload)#Pressao PIT-03 (camara de entrada de ar no ventilador) em milimetros de coluna de agua mmH20
                

               
                
                leitura = self._db.get_holding_registers(884,2)
                decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.BIG, wordorder=Endian.BIG)
                
                
                print("=================")
                print("Tabela MODBUS")
                print(f' Holding Register \r \n R1216: {round(decoder.decode_32bit_float(),2)} \r\n R706: {self._db.get_holding_registers(706)}')
                sleep(1)
        except Exception as e:
            print("Erro: ",e.args)


            """
            acho que pra fazer leitura de bits, essa logica faz sentido
            def leDado(self, addr, bit):
            
            ler = self._cliente.read_holding_registers(addr, 1)[0]
            lista_bits = [int(x) for x in "{0:016b}".format(ler)]
            return str(lista_bits[abs(15 - bit)])


            # Exemplo de uso
if __name__ == "__main__":
    servidor = ServidorMODBUS('127.0.0.1', 502)
    servidor.run()"""