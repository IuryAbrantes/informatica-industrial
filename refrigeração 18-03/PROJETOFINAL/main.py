from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder
from kivy.core.window import Window

Window.size=(1024,768)
Window.fullscreen = False

class MainApp(App):
    """
    Classe com aplicativo
    """

    def build(self):
        """
        Método que gera o app com widget principal
        """  
        self._widget = MainWidget(scan_time = 1000, 
                                  #server_ip = '10.15.30.183',
                                  server_ip = '127.0.0.1', 
                                  server_port = 502,
                                  modbus_addrs = {
                                    'temperatura_enrolamento_r': {'addr': 700, 'modelo': 'float', 'divisor': 10},
                                    'temperatura_enrolamento_s': {'addr': 702, 'modelo': 'float', 'divisor': 10},
                                    'temperatura_enrolamento_t': {'addr': 704, 'modelo': 'float', 'divisor': 10},
                                    'temperatura_carcaca': {'addr': 706, 'modelo': 'float', 'divisor': 10},
                                    'temperatura_arSaida': {'addr': 710, 'modelo': 'float', 'divisor': 1},
                                    'velocidade_arSaida': {'addr': 712, 'modelo': 'float', 'divisor': 1},
                                    'vazao_arSaida': {'addr': 714, 'modelo': 'float', 'divisor': 1},
                                    'frequencia_compressor': {'addr': 751, 'modelo': 'float', 'divisor': 100},
                                    'frequencia_motor': {'addr': 830, 'modelo': 'float', 'divisor': 100},
                                    'mostra_partida': {'addr': 1216, 'modelo': 'bit', 'divisor': 1},
                                    'temp_canVermelho': {'addr': 1218, 'modelo': 'float', 'divisor': 10},
                                    'temp_canAzul': {'addr': 1220, 'modelo': 'float', 'divisor': 10},
                                    'pressao_canVerm': {'addr': 1222, 'modelo': 'float', 'divisor': 10},
                                    'pressao_canAzul': {'addr': 1224, 'modelo': 'float', 'divisor': 10},
                                    'pressao_arEnt': {'addr': 1226, 'modelo': 'float', 'divisor': 10},
                                    'pressao_baixaScroll': {'addr': 1230, 'modelo': 'bit', 'divisor': 1},
                                    'pressao_altaScroll': {'addr': 1230, 'modelo': 'bit', 'divisor': 1},
                                    'pressao_baixaHerm': {'addr': 1230, 'modelo': 'bit', 'divisor': 1},
                                    'pressao_altaHerm': {'addr': 1230, 'modelo': 'bit', 'divisor': 1},
                                    'corrente_r':{'addr': 726, 'modelo': 'holding', 'divisor': 10},
                                    'corrente_s':{'addr': 727, 'modelo': 'holding', 'divisor': 10},
                                    'corrente_t':{'addr': 728, 'modelo': 'holding', 'divisor': 10},
                                    'pot_a_total':{'addr': 738, 'modelo': 'holding', 'divisor': 1},
                                    'fat_pot':{'addr' : 750, 'modelo' : 'holding', 'divisor': 1000},
                                    'fat_pot_comp':{'addr' : 871, 'modelo' : 'holding', 'divisor': 1000},
                                    'flap': {'addr': 1310, 'modelo': 'float', 'divisor': 1},
                                    'vel_inversor': {'addr': 1313, 'modelo': 'bit', 'divisor': 1},
                                    'sel_partida': {'addr': 1324, 'modelo': 'bit', 'divisor': 1},
                                    'sel_vent': {'addr': 1328, 'modelo': 'bit', 'divisor': 1},
                                    'sel_comp': {'addr': 1328, 'modelo': 'bit', 'divisor': 1},
                                    'liga_comp': {'addr': 1328, 'modelo': 'bit', 'divisor': 1},
                                    'aquecedor': {'addr': 1329, 'modelo': 'bit', 'divisor': 1},
                                    'turnOn_turnOff': {'addr': 1330, 'modelo': 'bit', 'divisor': 1},
                                    'torque_motor_axial': {'addr': 1424, 'modelo': 'float', 'divisor': 1},
                                    'vel_motor_axial': {'addr': 884, 'modelo': 'float', 'divisor': 1}})

        return self._widget
    
    def on_stop(self):
        """
        Método executado quando o app é fechado
        """  
        self._widget.stopRefresh()
    
if __name__ == '__main__':

    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly = True)
    Builder.load_string(open("popups.kv", encoding="utf-8").read(), rulesonly = True)
    MainApp().run()