from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder


class MainApp(App):
    """
    Classe com aplicativo
    """

    def build(self):
        """
        Método que gera o app com widget principal
        """  
        self._widget = MainWidget(scan_time = 1000, 
                                  server_ip = '127.0.0.1', 
                                  server_port = 502,
                                  modbus_addrs = {
                                    'temperatura_enrolamento_r': {'addr': 700, 'modelo': 'float'},
                                    'temperatura_enrolamento_s': {'addr': 702, 'modelo': 'float'},
                                    'temperatura_enrolamento_t': {'addr': 704, 'modelo': 'float'},
                                    'temperatura_carcaca': {'addr': 706, 'modelo': 'float'},
                                    'temperatura_arSaida': {'addr': 710, 'modelo': 'float'},
                                    'velocidade_arSaida': {'addr': 712, 'modelo': 'float'},
                                    'vazao_arSaida': {'addr': 714, 'modelo': 'float'},
                                    'frequencia_compressor': {'addr': 751, 'modelo': 'float'},
                                    'frequencia_motor': {'addr': 830, 'modelo': 'float'},
                                    'mostra_partida': {'addr': 1216, 'modelo': 'bit'},
                                    'temp_canVermelho': {'addr': 1218, 'modelo': 'float'},
                                    'temp_canAzul': {'addr': 1220, 'modelo': 'float'},
                                    'pressao_canVerm': {'addr': 1222, 'modelo': 'float'},
                                    'pressao_canAzul': {'addr': 1224, 'modelo': 'float'},
                                    'pressao_arEnt': {'addr': 1226, 'modelo': 'float'},
                                    'pressao_baixaScroll': {'addr': 1230, 'modelo': 'bit'},
                                    'pressao_altaScroll': {'addr': 1230, 'modelo': 'bit'},
                                    'pressao_baixaHerm': {'addr': 1230, 'modelo': 'bit'},
                                    'pressao_altaHerm': {'addr': 1230, 'modelo': 'bit'},
                                    'corrente_r':{'addr': 726, 'modelo': 'holding'},
                                    'corrente_s':{'addr': 727, 'modelo': 'holding'},
                                    'corrente_t':{'addr': 728, 'modelo': 'holding'},
                                    'pot_a_total':{'addr': 738, 'modelo': 'holding'},
                                    'freq_motor':{'addr' : 830, 'modelo' : 'holding'},
                                    'fat_pot':{'addr' : 750, 'modelo' : 'holding'},
                                    'fat_pot_comp':{'addr' : 871, 'modelo' : 'holding'},
                                    'flap': {'addr': 1310, 'modelo': 'float'},
                                    'vel_inversor': {'addr': 1313, 'modelo': 'bit'},
                                    'sel_partida': {'addr': 1324, 'modelo': 'bit'},
                                    'sel_vent': {'addr': 1328, 'modelo': 'bit'},
                                    'sel_comp': {'addr': 1328, 'modelo': 'bit'},
                                    'liga_comp': {'addr': 1328, 'modelo': 'bit'},
                                    'aquecedor': {'addr': 1329, 'modelo': 'bit'},
                                    'turnOn_turnOff': {'addr': 1330, 'modelo': 'bit'}})

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