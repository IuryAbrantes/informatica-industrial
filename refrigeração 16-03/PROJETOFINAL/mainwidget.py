from kivy.uix.boxlayout import BoxLayout
from pyModbusTCP.client import ModbusClient
from kivy.properties import ObjectProperty
from popups import ModbusPopup, ScanPopup, MedidoresPopup, GraficoMotorPopup, MotoresPopup, DadosPopup, OutrosPopup, GraficoArSaiPopup, GraficoTit01Popup, GraficoTit02Popup, GraficoPit01Popup, GraficoPit02Popup, GraficoPit03Popup
from kivy.core.window import Window
from threading import Thread, Lock
from time import sleep
from datetime import datetime 
import random
from timeseriesgraph import TimeSeriesGraph
#from db import Session, Base, engine #mudar esse import pro db feito com sqlalchemy
#from models import DadoCLP
from kivy_garden.graph import LinePlot 
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian




class MainWidget(BoxLayout):
        """
        Widget prinipal do app
        """
        
        #modbus_addrs = ObjectProperty({})  # Declara modbus_addrs como uma propriedade do Kivy
        _updateThread = None
        _updateWidgets = True
        _tags = {}
        _max_points = 20

        def __init__(self, **kwargs):
                super().__init__()
                self._lock= Lock()
                self._scan_time = kwargs.get('scan_time')
                self._serverIP = kwargs.get('server_ip')
                self._porta = kwargs.get('server_port')
                self._modbusPopup = ModbusPopup(self._serverIP, self._porta)
                self._scanPopup = ScanPopup(self._scan_time)
                self._medidoresPopup = MedidoresPopup()
                self._motoresPopup = MotoresPopup()
                self._dadosPopup = DadosPopup()   
                self._outrosPopup = OutrosPopup() 
                self._modbus_client = ModbusClient(host=self._serverIP, port=self._porta)
                self.connect_to_server()
                self._meas = {}
                self._meas ['timestamp'] = None
                self._meas ['values'] = {}
                self._tags = kwargs.get('modbus_addrs')
                for key, value in kwargs.get('modbus_addrs').items():
                        if key == 'temperatura_enrolamento_r':
                                plot_color = (1,0,0,1)
                        else:
                                plot_color = (random.random(),random.random(),random.random(),1)

                        self._meas['values'][key]= {'addr':value['addr'], 'modelo' : value['modelo'], 'color': plot_color}
                        self._tags[key]= {'addr':value['addr'], 'modelo' : value['modelo'], 'color': plot_color}
                self._graficoMotorPopup = GraficoMotorPopup(self._max_points, self._tags['temperatura_carcaca']['color'])
                self._graficoTit01Popup = GraficoTit01Popup(self._max_points, self._tags['temp_canAzul']['color'])
                self._graficoArSaiPopup = GraficoArSaiPopup(self._max_points, self._tags['temperatura_arSaida']['color'])
                self._graficoTit02Popup = GraficoTit02Popup(self._max_points, self._tags['temp_canVermelho']['color'])
                self._graficoPit01Popup = GraficoPit01Popup(self._max_points, self._tags['pressao_canAzul']['color'])
                self._graficoPit03Popup = GraficoPit03Popup(self._max_points, self._tags['pressao_arEnt']['color'])
                self._graficoPit02Popup = GraficoPit02Popup(self._max_points, self._tags['pressao_canVerm']['color'])

        def connect_to_server(self):
                """Conecta ao servidor MODBUS"""
                if self._modbus_client.open():
                        print("Conectado ao servidor MODBUS")
                else:
                        print("Falha ao conectar ao servidor MODBUS")


        def startDataRead(self):
                """"
                Método utilizado para a configuração do IP e porta do servidor MODBUS e
                inicializar uma thread para a leitura dos dados e atualização da interface gráfica
                """
                with self._lock:
                        self._serverIP = '127.0.0.1'
                        self._serverPort = 502
                        self._modbus_client.host = self._serverIP
                        self._modbus_client.port = self._serverPort
                try:
                        Window.set_system_cursor("wait") 
                        self._modbus_client.open() 
                        Window.set_system_cursor("arrow") 
                        if self._modbus_client.is_open:
                                self._updateThread = Thread(target=self.updater) 
                                self._updateThread.start() 
                                self.ids.img_con.source = 'imgs/conectado.png' #colocar a imagem
                                self._modbusPopup.dismiss()
                        else:
                                self._modbusPopup.setInfo("Erro de conexão")
                except Exception as e:
                        print("Erro: ", e.args)


        def updater(self):
                """
                Método que invoca as rotinas de leitura dos dados, atualização da interface e
                inserção dos dados no banco de dados 
                """
                try:
                        while self._updateWidgets:
                                self.readData()
                                self.updateGUI()
                                #self.armazenaDados()
                                #self._db.insertData(self._meas)
                                sleep(self._scan_time/1000)
                except Exception as e:
                        self._modbus_client.close()
                        print("Erro: ", e.args)

        def readData(self):
                """
                Método para leitura de dados via MODBUS
                """
                self._meas['timestamp'] = datetime.now()
                for key, value in self._tags.items():
                        print(self._tags[key]['modelo'])
                        if self._tags[key]['modelo'] == 'float':
                                self._meas['values'][key] = self.leituraFloat(value['addr'])
                        elif self._tags[key]['modelo'] == 'bit':
                                self._meas['values'][key] = self.leituraBits(value['addr'])
                        elif self._tags[key]['modelo'] == 'holding':
                                self._meas['values'][key] = self.leituraholding(value['addr'])


        def leituraFloat(self, addr):
                print(addr)
                leitura = self._modbus_client.read_holding_registers(int(addr),2)
                #decodifica o dado ascii armazenado 
                decodificador = BinaryPayloadDecoder.fromRegisters(registers=leitura, byteorder=Endian.BIG, wordorder=Endian.BIG)
                
                return float(decodificador.decode_32bit_float())
                
        
        def leituraholding (self, addr):
                leitura = self._modbus_client.read_holding_registers(addr, 1)[0]
                return leitura

        def leituraBits(self, addr):
                leitura = self._modbus_client.read_holding_registers(addr,2)
                decodificador = BinaryPayloadDecoder.fromRegisters(registers=leitura, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
                #preenche os 8 primeiros bits
                bits = decodificador.decode_bits()
                #mantem os bits ja decodificados e adiciona mais 8
                bits += decodificador.decode_bits()
        #cria uma lista e preenche com os bits decodificados
                lerBits = [int(bit) for bit in bits]
                return lerBits

        def escreveFloat(self, addr, valor):
                builder = BinaryPayloadBuilder() #inicializa uma instancia de construçao
                builder.add_32bit_float(float(valor)) #adiciona o valor do tipo float recebido ao buffer
                payload = builder.to_registers() #retorna uma lista de bytes para a variavel payload
                return self._modbus_client.write_multiple_registers(addr,payload)


        def escreveBit(self, addr, posicaoBit, valorBit):
                """
                Função que escreve um valor específico em um bit específico de um registro de holding.
                """
                # Leitura dos registros de holding
                leitura = self._modbus_client.read_holding_registers(addr, 2)
                # Decodificação dos registros lidos em bits
                decodificador = BinaryPayloadDecoder.fromRegisters(registers=leitura, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
                #preenche os 8 primeiros bits
                bits = decodificador.decode_bits()
                #mantem os bits ja decodificados e adiciona mais 8
                bits += decodificador.decode_bits()
                # Criação de uma lista com os bits decodificados
                lerBits = [int(bit) for bit in bits]
                # Modificação do bit especificado
                escreveBits = lerBits
                escreveBits[posicaoBit] = valorBit
                # Construção do payload com os bits modificados
                builder = BinaryPayloadBuilder(registers = leitura, byteorder = Endian.BIG, wordorder = Endian.LITTLE)
                builder.add_bits(escreveBits)
                payload = builder.to_registers()
                # Escrita dos registros modificados no CLP
                return self._modbus_client.write_multiple_registers(addr, payload)
        
        def updateGUI(self):
                """
                Método para atualização da interface gráfica dos dados lidos
                """
                for key, value in self._tags.items():
                        if key in self.ids:
                                valor = self._meas['values'][key]
                                unidade = value.get('unit', '')  # Obtém a unidade do dicionário

                                if valor is not None:
                                        arredondado = round(valor, 2)  # Arredonda para duas casas decimais
                                        self.ids[key].text = f"{arredondado} {unidade}".strip()
                                else:
                                        self.ids[key].text = f"-.- {unidade}".strip()

        #if value ["local"]== "motor":
                #self.monitoraMotor.ids[key].text = "{:.2f}".format(self._meas["values"][key]) + value["unit"]
        #else:
                #self.ids[key].text = "{:.2f}".format(self._meas["values"][key])+value["unit"]          
                popups = {
                        '_medidoresPopup': [
                        ('corrente_r', ' A'), ('corrente_s', ' A'), ('corrente_t', ' A'), ('frequencia_motor', 'Hz'),
                        ('pot_a_total', ' kW'), ('fat_pot', ''), ('fat_pot_comp', ''),
                        ('temperatura_enrolamento_r', 'ºC'), ('temperatura_enrolamento_s', 'ºC'), ('temperatura_enrolamento_t', 'ºC')
                        , ('frequencia_compressor', 'Hz') , ('frequencia_motor', 'Hz')
                        ]
                        
                
                }
                for popup_name, labels in popups.items():
                        popup = getattr(self, popup_name, None)
                        if popup:
                                for key, unidade in labels:
                                        if key in self._meas['values']:
                                                valor = self._meas['values'][key]
                                        try:
                                                popup.ids[key].text = f"{round(valor, 2)} {unidade}".strip()
                                        except Exception as e:
                                                print(f"Erro ao atualizar {popup_name}: {e}")

                #Atualizar gráfico
                self._graficoMotorPopup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['temperatura_carcaca']),0)
                self._graficoTit01Popup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['temp_canAzul']), 0)
                self._graficoArSaiPopup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['temperatura_arSaida']), 0)
                self._graficoTit02Popup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['temp_canVermelho']), 0)
                self._graficoPit01Popup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['pressao_canAzul']), 0)
                self._graficoPit03Popup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['pressao_arEnt']), 0)
                self._graficoPit02Popup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['pressao_canVerm']), 0)
                

                                
        #exemplo de acionamento que pode ser aplicado
        def desligaCompressor(self): 
                """
                Função que desliga o compressor
                """
                self.escreveBit(1328, 12, 0) #addr , ordem do bit,  desligado
                self.escreveBit(1329, 8, 1) #addr, ordem do bit, ligado
        #exemplo de acionamento que pode ser aplicado
        def desligaCompressor(self): 
                """
                Função que desliga o compressor
                """
                self.escreveBit(1328, 12, 0) #addr , ordem do bit,  desligado
                self.escreveBit(1329, 8, 1) #addr, ordem do bit, ligado

        def ligaCompressor(self):
                """
                Função que liga o compressor
                """
                self.escreveBit(1328, 12, 1)

        def selecionaPartida(self, parametro):
                """
                Função que seleciona o tipo de partida
                """
                
                v_lido = parametro
                self.write_single_register(1324, int(v_lido))

        def selecionaMotor(self, parametro):
                """
                Função que seleciona o tipo de partida
                """
                self.escreveBit(1328, 13, parametro)

        def ligaVentilador(self): 
                """
                Função que liga o ventilador
                """
                tipo_partida = self.read_holding_registers(1324,1)[0]
                if tipo_partida == 1:
                        turnOn = self.write_single_register(1312,1)
                        return turnOn

                elif tipo_partida == 2:
                        turnOn = self.write_single_register(1316,1)
                        return turnOn

                else: 
                        turnOn = self.write_single_register(1319,1)
                        return turnOn

        def selRendimento(self, parametro):
                """
                Função que seleciona o tipo de rendimento -> alto rendimento ou convencional
                """
                self.escreveBit(1328, 13, parametro)

       
        """
        def selecionaPID(self):

                Função que seleciona o tipo de PID(automatico = 0 , manual = 1)
                
                self.escreveBit(1332,1)
                self.escreveBit(1332,0)
        """
        def velocidadeInversor(self, parametro):
                """
                Função que define a velocidade do inversor 
                """
                #parametro = self._comandoVentPopup.ids.vel_inversor
                self.escreveFloat(1313, (parametro*5))

        def stopRefresh(self):
                self._updateWidgets = False


        """
        def parseDTString(self, datetime_str):
                #Método que converte a string inserida pelo usuário para o formato aceito pelo BD
                try:
                d = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
                return d.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                print("Erro: ", e.args)"""