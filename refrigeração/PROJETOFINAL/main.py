from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder


class MainApp(App):
    """
    Classe com o aplicativo
    """
    def build(self):
        """
        Método que gera o aplicativo no widget principal
        """
        self._widget = MainWidget(server_ip='localhost',server_port=502,
        modbus_addrs = {
            'temp_carc': 706,
            'cor_R': 726,
            'cor_S': 727,
            'cor_T': 728,
            'pot_ativ_t':738,
            'pot_reativ_t':742,
            'fator_pot': 871,
            'rot_mot':884,
            'freq_compr':751
        }        
        )
        return self._widget
    
if __name__ == '__main__':
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()

