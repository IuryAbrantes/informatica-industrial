from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import random
from pymodbus.payload import BinaryPayloadBuilder
import struct

class ServidorMODBUS():
    """
    Classe Servidor MODBUS
    """
    def __init__(self, host_ip, port):
        self._server = ModbusServer(host=host_ip, port=port, no_block=True)
    
    def float_to_payload(self, value):
        builder = BinaryPayloadBuilder(byteorder="big", wordorder="big")
        builder.add_32bit_float(value)
        return builder.to_registers()

    def run(self):
        self._server.start()
        print("Servidor em execução")
        while True:
            tit01 = self.float_to_payload(random.uniform(18.0, 30.0))
            tit02 = self.float_to_payload(random.uniform(18.0, 30.0))
            pit01 = self.float_to_payload(random.uniform(-5.0, 5.0))
            pit02 = self.float_to_payload(random.uniform(-5.0, 5.0))
            pit03 = self.float_to_payload(random.uniform(-5.0, 5.0))
            temperatura = self.float_to_payload(random.uniform(18.0, 30.0))
            velocidade = self.float_to_payload(random.uniform(0.0, 50.0))
            vazao = self.float_to_payload(random.uniform(0.0, 100.0))
            encoder_axial = self.float_to_payload(random.uniform(0.0, 100.0))
            torque_axial = self.float_to_payload(random.uniform(0.0, 100.0))
            temp_r = self.float_to_payload(random.uniform(0.0, 100.0))
            temp_s = self.float_to_payload(random.uniform(0.0, 100.0))
            temp_t = self.float_to_payload(random.uniform(0.0, 100.0))
            temp_carc = self.float_to_payload(random.uniform(0.0, 100.0))
            freq_mot = self.float_to_payload(random.uniform(0.0, 100.0))

            self._server.data_bank.set_holding_registers(1220, tit01) 
            self._server.data_bank.set_holding_registers(1218, tit02)  
            self._server.data_bank.set_holding_registers(1224, pit01)  
            self._server.data_bank.set_holding_registers(1222, pit02)  
            self._server.data_bank.set_holding_registers(1226, pit03)  
            self._server.data_bank.set_holding_registers(710, temperatura)  
            self._server.data_bank.set_holding_registers(712, velocidade)  
            self._server.data_bank.set_holding_registers(714, vazao)  
            self._server.data_bank.set_holding_registers(884, encoder_axial)  
            self._server.data_bank.set_holding_registers(1424, torque_axial)  
            self._server.data_bank.set_holding_registers(830, freq_mot)  
            self._server.data_bank.set_holding_registers(700, temp_r)  
            self._server.data_bank.set_holding_registers(702, temp_s)  
            self._server.data_bank.set_holding_registers(704, temp_t)  
            self._server.data_bank.set_holding_registers(706, temp_carc)
            self._server.data_bank.set_holding_registers(732, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(733, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(734, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(726, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(727, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(728, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(729, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(731, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(735, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(736, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(737, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(738, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(739, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(740, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(741, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(742, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(743, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(144, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(745, [random.randrange(40,100)])  
            self._server.data_bank.set_holding_registers(146, [random.randrange(40,100)])

            self._server.data_bank.set_holding_registers(1000,[random.randrange(400,500)]) # temperatura
            self._server.data_bank.set_holding_registers(1001,[random.randrange(100000,120000)]) #pressão
            self._server.data_bank.set_holding_registers(1002,[random.randrange(20,40)]) # umidade
            self._server.data_bank.set_holding_registers(1003,[random.randrange(40,100)]) # consumo
            self._server.data_bank.set_holding_registers(1004,[random.randrange(40,100)]) # consumo
            self._server.data_bank.set_holding_registers(1005,[random.randrange(40,100)]) # consumo
            self._server.data_bank.set_holding_registers(1006,[random.randrange(40,100)]) # consumo
            self._server.data_bank.set_holding_registers(1007,[random.randrange(40,100)]) # consumo
            self._server.data_bank.set_holding_registers(1008,[random.randrange(40,100)]) # consumo

            sleep(1)

# Exemplo de uso
if __name__ == "__main__":
    servidor = ServidorMODBUS('127.0.0.1', 502)
    servidor.run()
