from kivy.uix.popup import Popup



class ModbusPopup(Popup):
    """
    Popup para configuração do protocolo MODBUS
    """
    def __init__(self, server_ip, server_port, **kwargs):
        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_porta.text = str(server_port)

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

