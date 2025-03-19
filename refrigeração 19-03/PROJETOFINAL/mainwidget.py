from kivy.uix.boxlayout import BoxLayout
from pyModbusTCP.client import ModbusClient
from kivy.properties import ObjectProperty
from popups import ModbusPopup, ScanPopup, MedidoresMotorPopup, MedidoresCompPopup, GraficoVelArPopup, GraficoVelMPopup, GraficoMotorPopup, MotoresPopup, ComandoCompPopup, DadosPopup, GraficoArSaiPopup, GraficoTit01Popup, GraficoTit02Popup, GraficoPit01Popup, GraficoPit02Popup, GraficoPit03Popup, HistGraphPopup
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
from Dados import GuardarDados
from kivy.properties import DictProperty, ListProperty



class MainWidget(BoxLayout):
        """
        Widget prinipal do app
        """
        
        #modbus_addrs = ObjectProperty({})  # Declara modbus_addrs como uma propriedade do Kivy
        _updateThread = None
        _updateWidgets = True
        _tags = {}
        _motorLigado = False
        _dados = {
                "timestamp": datetime.now(),
                "temperatura_enrolamento_r": 0,
                "temperatura_enrolamento_s": 35.5,
                "temperatura_enrolamento_t": 36.0,
                "temperatura_carcaca": 30.2,
                "temperatura_arSaida": 25.4,
                "velocidade_arSaida": 12.5,
                "vazao_arSaida": 200.0,
                "frequencia_compressor": 50.0,
                "frequencia_motor": 60.0,
                "mostra_partida": 1.0,
                "temp_canVermelho": 40.0,
                "temp_canAzul": 38.5,
                "pressao_canVerm": 2.5,
                "pressao_canAzul": 2.8,
                "pressao_arEnt": 3.0,
                "pressao_baixaScroll": 1.2,
                "pressao_altaScroll": 5.0,
                "pressao_baixaHerm": 1.0,
                "pressao_altaHerm": 4.8,
                "corrente_r": 10.5,
                "corrente_s": 10.2,
                "corrente_t": 10.8,
                "corrente_r_comp": 10.5,
                "corrente_s_comp": 10.2,
                "corrente_t_comp": 10.8,
                "pot_a_total_comp": 1500.0,
                "pot_a_total": 1500.0,
                "fat_pot_comp": 0.98,
                "fat_pot": 0,
                "flap": 0,  # Adicionado
                "vel_inversor": 0,  # Adicionado
                "sel_partida": 0,  # Adicionado
                "sel_vent": 0,  # Adicionado
                "sel_comp": 0,  # Adicionado
                "liga_comp": 0,  # Adicionado
                "aquecedor": 0,  # Adicionado
                "turnOn_turnOff": 0,  # Adicionado
                "torque_motor_axial": 0,  # Adicionado
                "vel_motor": 0  # Adicionado
                
        }

        _divisoresdb = {
                "timestamp":1,
                "temperatura_enrolamento_r": 10,
                "temperatura_enrolamento_s": 10,
                "temperatura_enrolamento_t": 10,
                "temperatura_carcaca": 10,
                "temperatura_arSaida": 1,
                "velocidade_arSaida": 1,
                "vazao_arSaida": 1,
                "frequencia_compressor": 100,
                "frequencia_motor": 100,
                "mostra_partida": 1,
                "temp_canVermelho": 10,
                "temp_canAzul": 10,
                "pressao_canVerm": 10,
                "pressao_canAzul": 10,
                "pressao_arEnt": 10,
                "pressao_baixaScroll": 1,
                "pressao_altaScroll": 1,
                "pressao_baixaHerm": 1,
                "pressao_altaHerm": 1,
                "corrente_r": 10,
                "corrente_s": 10,
                "corrente_t": 10,
                "corrente_r_comp": 10,
                "corrente_s_comp": 10,
                "corrente_t_comp": 10,
                "pot_a_total_comp": 1,
                "pot_a_total": 1,
                "fat_pot_comp": 1000,
                "fat_pot": 1000,
                "flap": 1,  # Adicionado
                "vel_inversor": 1,  # Adicionado
                "sel_partida": 1,  # Adicionado
                "sel_vent": 1,  # Adicionado
                "sel_comp": 1,  # Adicionado
                "liga_comp": 1,  # Adicionado
                "aquecedor": 1,  # Adicionado
                "turnOn_turnOff": 1,  # Adicionado
                "torque_motor_axial": 1,  # Adicionado
                "vel_motor": 1  # Adicionado
                
        }

        alerta_cores = DictProperty({
                "temperatura_carcaca": [0.925, 0.945, 0.973, 0],  # Cor inicial (branco)
                "vel_motor": [0.925, 0.945, 0.973, 0],
                "pressao_canVerm": [0.925, 0.945, 0.973, 0],
                "pressao_canAzul": [0.925, 0.945, 0.973, 0],
                "temp_canVermelho": [0.925, 0.945, 0.973, 0],
                "temp_canAzul": [0.925, 0.945, 0.973, 0],
                "pressao_arEnt": [0.925, 0.945, 0.973, 0],
                "temperatura_arSaida": [0.925, 0.945, 0.973, 0],
                "velocidade_arSaida": [0.925, 0.945, 0.973, 0]
        })

        _max_points = 20

        def __init__(self, **kwargs):
                super().__init__()
                self._lock= Lock()
                self._scan_time = kwargs.get('scan_time')
                self._serverIP = kwargs.get('server_ip')
                self._porta = kwargs.get('server_port')
                self._modbusPopup = ModbusPopup(self._serverIP, self._porta)
                self._scanPopup = ScanPopup(self._scan_time)
                self._motoresPopup = MotoresPopup()
                self._dadosPopup = DadosPopup()
                self._comandoCompPopup = ComandoCompPopup()
                self._medidoresMotorPopup = MedidoresMotorPopup()
                self._medidoresCompPopup = MedidoresCompPopup()
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

                        self._meas['values'][key]= {'addr':value['addr'], 'modelo' : value['modelo'], 'divisor' : value['divisor'], 'color': plot_color}
                        self._tags[key]= {'addr':value['addr'], 'modelo' : value['modelo'], 'divisor' : value['divisor'], 'color': plot_color}
                self._graficoMotorPopup = GraficoMotorPopup(self._max_points, self._tags['temperatura_carcaca']['color'])
                self._graficoTit01Popup = GraficoTit01Popup(self._max_points, self._tags['temp_canAzul']['color'])
                self._graficoArSaiPopup = GraficoArSaiPopup(self._max_points, self._tags['temperatura_arSaida']['color'])
                self._graficoTit02Popup = GraficoTit02Popup(self._max_points, self._tags['temp_canVermelho']['color'])
                self._graficoPit01Popup = GraficoPit01Popup(self._max_points, self._tags['pressao_canAzul']['color'])
                self._graficoPit03Popup = GraficoPit03Popup(self._max_points, self._tags['pressao_arEnt']['color'])
                self._graficoPit02Popup = GraficoPit02Popup(self._max_points, self._tags['pressao_canVerm']['color'])
                self._graficoVelArPopup = GraficoVelArPopup(self._max_points, self._tags['velocidade_arSaida']['color'])
                self._graficoVelMPopup = GraficoVelMPopup(self._max_points, self._tags['vel_motor']['color'])
                self._hgraph = HistGraphPopup(tags=self._tags)
                self._buscador = GuardarDados()

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
                        #self._serverIP = '10.15.30.183'
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
                                self._meas['values'][key] = self.leituraFloat(value['addr'])/(value['divisor'])
                        elif self._tags[key]['modelo'] == 'bit':
                                self._meas['values'][key] = self.leituraBits(value['addr'])*(value['divisor'])
                        elif self._tags[key]['modelo'] == 'holding':
                                self._meas['values'][key] = self.leituraholding(value['addr'])/(value['divisor'])


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
                        '_medidoresPopup': [],

                        '_medidoresMotorPopup':[ ('frequencia_motor', 'Hz'), ('torque_motor_axial', 'N.m'),('corrente_r', ' A'), ('corrente_s', ' A'), ('corrente_t', ' A'),
                        ('pot_a_total', ' kW'), ('fat_pot', ''),('temperatura_enrolamento_r', 'ºC'), ('temperatura_enrolamento_s', 'ºC'), ('temperatura_enrolamento_t', 'ºC')],

                        '_medidoresCompPopup':[('corrente_r_comp', ' A'), ('corrente_s_comp', ' A'), ('corrente_t_comp', ' A'),('pot_a_total_comp', ' kW'),
                        ('fat_pot_comp', ''),('frequencia_compressor', 'Hz')]
                
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
                self._graficoVelArPopup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['velocidade_arSaida']), 0)
                self._graficoVelMPopup.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['vel_motor']), 0)               

                #Atualizar Termômetro Dinâmico
                self.ids.lb_tempcarc.size = (self._meas['values']['temperatura_carcaca']/45*60,13)
                self.ids.lb_tempcanA.size = (self._meas['values']['temp_canAzul']/45*60,13)
                self.ids.lb_tempcanV.size = (self._meas['values']['temp_canVermelho']/45*60,13)
                self.ids.lb_motor.size = (self._meas['values']['vel_motor']/3800*60,13)
                self.ids.lb_pitum.size = (self._meas['values']['pressao_canAzul']/15*60,13)
                self.ids.lb_pitdois.size = (self._meas['values']['pressao_canVerm']/40*60,13)
                self.ids.lb_pittres.size = (self._meas['values']['pressao_arEnt']/15*60,13)
                self.ids.lb_tempsai.size = (self._meas['values']['temperatura_arSaida']/40*60,13)
                self.ids.lb_velsai.size = (self._meas['values']['velocidade_arSaida']/15*60,13)

                limites = {
                        "temperatura_carcaca": (35.0, 40.0),
                        "vel_motor": (3200, 3400),
                        "pressao_canVerm": (25, 34),
                        "pressao_canAzul": (9, 12),
                        "temp_canVermelho": (32, 38),
                        "temp_canAzul": (32, 38),
                        "pressao_arEnt": (300, 400),
                        "temperatura_arSaida": (25, 36),
                        "velocidade_arSaida": (8, 12)
                        }
                
                for key, (limite_laranja, limite_vermelho) in limites.items():
                        valor = self._meas['values'].get(key, 0)
                        if valor > limite_vermelho:
                                self.alerta_cores[key] = [1, 0, 0, 1]  # 🔴 Vermelho
                        elif valor > limite_laranja:
                                self.alerta_cores[key] = [1, 0.5, 0, 1]  # 🟠 Laranja
                        else:
                                self.alerta_cores[key] = [0.925, 0.945, 0.973, 0]

                #Atualizar Banco de dados
                self.armazenaDados()

        #Atualizar Banco de Dados
        def armazenaDados(self):
                """
                Método para armazenar os dados no banco de dados
                """
                self._lock.acquire()
                try:
                        # Atualiza os valores em self._dados com base em self._meas['values']
                        self._dados['timestamp'] = datetime.now()
                        for key in self._meas['values']:
                                if key in self._dados and key in self._divisoresdb:
                                        valor = self._meas['values'][key]
                                        divisor = self._divisoresdb[key]

                                        # Verifica se o valor é uma lista (caso de bits)
                                        if isinstance(valor, list):
                                                # Converte a lista de bits em um número inteiro
                                                # Exemplo: [0, 1, 0, 1] -> 5 (binário 0101)
                                                valor_inteiro = int("".join(map(str, valor)), 2)
                                                self._dados[key] = valor_inteiro
                                        else:
                                        # Para outros tipos (float, holding), aplica o divisor
                                                if divisor != 0:  # Evita divisão por zero
                                                        self._dados[key] = valor
                                                else:
                                                        print(f"Erro: Divisor zero para a chave {key}")
                                else:
                                        print(f"Erro: Chave {key} não encontrada em self._dados ou self._divisoresdb")

                        # Guarda os dados no banco de dados
                        guardador = GuardarDados()
                        guardador.guardar_dados(self._dados)
                except Exception as e:
                        print(f"Erro ao armazenar dados: {e}")
                finally:
                        self._lock.release()

        def selecionaPartida(self, parametro):
                """
                Função que seleciona a partida
                """
                valor_lido = parametro
                self._modbus_client.write_single_register(1324, valor_lido)

        def LigaMotor(self):
                """
                Função que liga/desliga o motor (ventilador)
                """
                tipo_partida = self._modbus_client.read_holding_registers(1216,1)[0] #indica a partida selecionada
                if not self._motorLigado:
                        self._motorLigado = True
                        if tipo_partida == 1:
                                self._modbus_client.write_single_register(1316, 1) #soft-start

                        elif tipo_partida == 2:
                                self._modbus_client.write_single_register(1312, 1) #inversor
                        else:
                                self._modbus_client.write_single_register(1319, 1) #direta
                else:
                        self._motorLigado = False
                        if tipo_partida == 1:
                                self._modbus_client.write_single_register(1316, 0) #soft-start
                        elif tipo_partida == 2:
                                self._modbus_client.write_single_register(1312, 0) #inversor
                        else:
                                self._modbus_client.write_single_register(1319, 0) #direta

        def resetVentilador(self):
                """
                Função que reseta o ventilador
                """
                tipo_partida = self._modbus_client.read_holding_registers(1216,1)[0]
                if tipo_partida == 1:
                        reset = self._modbus_client.write_single_register(1316,2) #soft-start
                        return reset

                elif tipo_partida == 2:
                        reset = self._modbus_client.write_single_register(1312,2) #inversor
                        return reset

                else: 
                        reset = self._modbus_client.write_single_register(1319,2) #direta
                        return reset

        def selecionaCompressor(self, parametro):
                """
                Função que seleciona o compressor
                """
                self.escreveBit(1328, 14, parametro)
                
        def LigaCompressor(self):
                """
                Função que liga/desliga o compressor
                """
                estado_atual = self._modbus_client.read_holding_registers(1231,1)[0] #endereço que indica o status do compressor
                if estado_atual == 0: #0 = compressor ligado
                        self.escreveBit(1329, 15, 1) #desliga o compressor, potencial fonte de erro no 15
                elif estado_atual == 1: #1 = compressor desligado
                        self.escreveBit(1328, 11, 1) #liga o compressor, potencial fonte de erro no 11
                else: 
                        pass
                
        def selecionaVentilador(self, parametro):
                """
                Função que seleciona o tipo de ventilador -> radial ou axial
                """
                self.escreveBit(1328, 13, parametro)

        def selecionaMotor(self, parametro):
                """
                Função que seleciona o tipo de motor -> alto rendimento ou convencional
                """
                self.escreveBit(1328, 10, parametro)

        def velocidadeScroll(self):
                """
                Função que define a velocidade do Scroll 
                """
                tipo_scroll = self._modbus_client.read_holding_registers(1328,1)[0]
                if tipo_scroll == 1: 
                        parametro = int(self._comandoCompPopup.ids.speed_slider.value)
                        self.escreveFloat(1236, parametro)
                else:
                        pass

        def automaticoScroll(self):
                """
                Função que escolhe o modo de operaçao do Scroll 
                """
                self.escreveBit(1328, 12, 0)

        def manualScroll(self):
                """
                Função que escolhe o modo de operaçao do Scroll 
                """
                self.escreveBit(1328, 12, 1)

        def VelInversor(self,vel):
                """
                Define a frequência do inversor
                """
                Partida = self._modbus_client.read_holding_registers(1216,1)[0]
                if Partida == 2:
                        self._modbus_client.write_single_register(1313,vel)

        """
        def ligaVentilador(self): 
                
                Função que liga o ventilador
                
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
                """
       
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


        def parseDTString(self, datetime_str):
                #Método que converte a string inserida pelo usuário para o formato aceito pelo BD
                try:
                        d = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
                        #return d.strftime("%Y-%m-%d %H:%M:%S")
                        return d.strftime("%d/%m/%Y %H:%M:%S")
                except Exception as e:
                        print("Erro: ", e.args)
        
      
        def BuscaComKivy(self):
                """
                Interface com Kivy para buscar dados
                """
                try:
                        init_t = self.parseDTString(self._hgraph.ids.txt_init_time.text)
                        final_t = self.parseDTString(self._hgraph.ids.txt_final_time.text)
                        cols = []
                        
                        cols.append('timestamp')

                        for sensor in self._hgraph.ids.sensores.children:
                                if sensor.ids.checkbox.active:
                                        cols.append(sensor.id)
                        if init_t is None or final_t is None or len(cols)==0:
                                return
                        
                        

                        dadoshistoricos = self._buscador.buscar_dados(cols,init_t,final_t)

                        if dadoshistoricos is None:
                        #or len(dadoshistoricos['timestamp'])==0
                                return
                        
                        self._hgraph.ids.graph.clearPlots()

                        for key, value in dadoshistoricos:
                                if key == 'timestamp':
                                        continue
                                p = LinePlot(line_width=1.5,color=self._tags[key]['color'])
                                p.points = [(x, value[x]) for x in range(0, len(value))]
                                self._hgraph.ids.graph.add_plot(p)
                        self._hgraph.ids.graph.xmax = len(dadoshistoricos[cols[0]])
                        self._hgraph.ids.graph.update_x_labels([datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f") for x in dadoshistoricos['timestamp']])
                except Exception as e:
                        print("Erro: ", e.args)