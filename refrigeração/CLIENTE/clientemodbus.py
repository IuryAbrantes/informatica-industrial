from pyModbusTCP.client import ModbusClient
from time import sleep
class ClienteMODBUS():
    """
    Classe Cliente MODBUS
    """
    def __init__(self, server_ip,porta,scan_time=1):
        """
        Construtor
        """
        self._cliente = ModbusClient(host=server_ip,port = porta)
        self._scan_time = scan_time
        self._fator_escala = 100  # Fator de escala (para ler o float corretamente)

    def int_to_float(self, valor_int):
        """
        Converte um inteiro de volta para float, aplicando o fator de escala.
        """
        return valor_int / self._fator_escala

    def atendimento(self):
        """
        Método para atendimento do usuário
        """
        self._cliente.open()
        try:
            atendimento = True
            while atendimento:
                sel = input("Deseja realizar uma leitura, escuta ou configuração? (1- Leitura | 2- Escrita | 3- Configuração | 4- Sair): ")

                if sel == '1':
                    tipo = input ("Qual tipo de dado deseja ler? (1- Holding Register | 2- Coil | 3- Input Register | 4- Discrete Input) :")
                    addr = input (f"Digite o endereço da tabela MODBUS: ")
                    nvezes = input ("Digite o número de vezes que deseja ler: ")
                    for i in range(0,int(nvezes)):
                        valor = self.lerDado(int(tipo), int(addr))
                        if tipo == '1':  #Se for um Holding Register, converte o valor para float
                            valor_float = self.int_to_float(valor)      
                            print(f"{valor_float:.2f}")
                        else:
                            print(f"Leitura {i + 1}: {valor}")
                        sleep(self._scan_time)
                elif sel =='2':
                    tipo = input ("Qual tipo de dado deseja escrever? (1- Holding Register | 2- Coil) :")
                    addr = input (f"Digite o endereço da tabela MODBUS: ")
                    valor = input(f"Digite o valor que deseja escrever: ")
                    self.escreveDado(int(tipo),int(addr),int(valor))
                    
                elif sel =='3':
                    scant = input("Digite o tempo de varredura desejado [s]: ")
                    self._scan_time = float(scant)

                elif sel =='4':
                    self._cliente.close()
                    atendimento = False

                else:
                    print("Seleção inválida")
        except Exception as e:
            print('Erro no atendimento: ',e.args)
    def lerDado(self, tipo, addr):
        """
        Método para leitura de um dado da tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.read_holding_registers(addr,1)[0]
        
        if tipo == 2:
            return self._cliente.read_coils(addr,1)[0]
        
        if tipo == 3:
            return self._cliente.read_input_registers(addr,1)[0]
        
        if tipo == 4:
            return self._cliente.read_discrete_inputs(addr,1)[0]
        
    def escreveDado(self, tipo, addr, valor):
        """
        Método para a escrita de dados na tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.write_single_register(addr,valor)