from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.graph import LinePlot
from kivy.uix.boxlayout import BoxLayout

class ModbusPopup(Popup):
    """
    Popup para configuração do protocolo MODBUS
    """
    _info_lb = None
    def __init__(self, server_ip, server_port, **kwargs):
        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_porta.text = str(server_port)


    def setInfo(self, message):
        self._info_lb = Label(text = message)
        self.ids.layout.add_widget(self._info_lb)    

    def clearInfo(self):
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)

class ScanPopup(Popup):
    """
    Popup para configuração do tempo de varredura
    """
    def __init__(self, scantime, **kwargs):
        """
        Construtor da classe ScanPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_st.text = str(scantime)



class MedidoresPopup(Popup):
    """
    Popup para monitoramento de medidores da planta
    """
    


class GraficosPopup(Popup):
    """
    Popup para monitoramento gráfico da planta
    """
    def __init__(self,xmax, plot_color, **kwargs):
        super().__init__(**kwargs)
        self._plot = LinePlot(line_width=1.5, color=plot_color)
        self.ids.graph.add_plot(self._plot)
        self.ids.graph.xmax = xmax


class MotoresPopup(Popup):
    """
    Popup para configuração de motores da planta
    """



class DadosPopup(Popup):
    """
    Popup para monitoramento de dados históricos da planta
    """


class OutrosPopup(Popup):
    """
    Popup para outras configurações da planta
    """


class LabelCheckBoxGraficos(BoxLayout):
    """
    
    """