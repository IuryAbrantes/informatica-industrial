from db import Base
from sqlalchemy import Column, Integer, DateTime, Float, Text
from datetime import datetime

class DadoCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadoclp'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)

    temperatura_enrolamento_r = Column(Float)
    temperatura_enrolamento_s = Column(Float)
    temperatura_enrolamento_t = Column(Float)
    temperatura_carcaca = Column(Float)
    temperatura_arSaida = Column(Float)
    velocidade_arSaida = Column(Float)
    vazao_arSaida = Column(Float)
    frequencia_compressor = Column(Float)
    frequencia_motor = Column(Float)
    mostra_partida = Column(Float)
    temp_canVermelho = Column(Float)
    temp_canAzul = Column(Float)
    pressao_canVerm = Column(Float)
    pressao_canAzul = Column(Float)
    pressao_arEnt = Column(Float)
    pressao_baixaScroll = Column(Float)
    pressao_altaScroll = Column(Float)
    pressao_baixaHerm = Column(Float)
    pressao_altaHerm = Column(Float)
    corrente_r = Column(Float)
    corrente_s = Column(Float)
    corrente_t = Column(Float)
    pot_a_total = Column(Float)
    fat_pot_comp = Column(Float)
    fat_pot = Column(Float)
    flap = Column(Text)
    vel_inversor = Column(Text)
    sel_partida = Column(Text)
    sel_vent = Column(Text)
    sel_comp = Column(Text)
    liga_comp = Column(Text)
    aquecedor = Column(Text)
    turnOn_turnOff = Column(Text)
    torque_motor_axial = Column(Text)
    vel_motor_axial = Column(Text)

    def get_DadosDB(self):
        return [self.id,
        self.timestamp.strftime('%d/%m/%Y %H:%M:%S.%f'),
        self.temperatura_enrolamento_r,
        self.temperatura_enrolamento_s,
        self.temperatura_enrolamento_t,
        self.temperatura_carcaca,
        self.temperatura_arSaida,
        self.velocidade_arSaida,
        self.vazao_arSaida,
        self.frequencia_compressor,
        self.frequencia_motor,
        self.mostra_partida,
        self.temp_canVermelho,
        self.temp_canAzul,
        self.pressao_canVerm,
        self.pressao_canAzul,
        self.pressao_arEnt,
        self.pressao_baixaScroll,
        self.pressao_altaScroll,
        self.pressao_baixaHerm,
        self.pressao_altaHerm,
        self.corrente_r,
        self.corrente_s,
        self.corrente_t,
        self.pot_a_total,
        self.fat_pot_comp,
        self.fat_pot,
        self.flap,
        self.vel_inversor,
        self.sel_partida,
        self.sel_vent,
        self.sel_comp,
        self.liga_comp,
        self.aquecedor,
        self.turnOn_turnOff,
        self.torque_motor_axial,
        self.vel_motor_axial
    ]