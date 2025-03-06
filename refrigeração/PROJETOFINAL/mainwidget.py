from kivy.uix.boxlayout import BoxLayout
from pyModbusTCP.client import ModbusClient
from kivy.properties import ObjectProperty


class MainWidget(BoxLayout):
    """
    Widget prinipal do app
    """
    modbus_addrs = ObjectProperty({})  # Declara modbus_addrs como uma propriedade do Kivy
    def __init__(self, server_ip, server_port, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.server_ip = server_ip
        self.server_port = server_port
        self.modbus_client = ModbusClient(host=self.server_ip, port=self.server_port)
        self.connect_to_server()


    def connect_to_server(self):
        """Conecta ao servidor MODBUS"""
        if self.modbus_client.open():
            print("Conectado ao servidor MODBUS")
        else:
            print("Falha ao conectar ao servidor MODBUS")


    def readData(self, dt):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """
        if self.modbus_client.is_open:
            for widget_id, address in self.modbus_addrs.items():
                # Lê o valor do registrador
                valor = self.modbus_client.read_holding_registers(address, 1)
                if valor:
                    # Converte o valor inteiro de volta para float
                    valor_float = valor[0] / 100.0
                    # Atualiza o texto do widget correspondente
                    self.ids[widget_id].text = f"{valor_float:.2f}"
        else:
            print("Servidor MODBUS desconectado")