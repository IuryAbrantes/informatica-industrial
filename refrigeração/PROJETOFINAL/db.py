from db import engine
from db import Base
from sqlalchemy import Column, Integer, DataTime


class DadoCLP(Base):
	"""
	Modelo dos dados do CLP
	"""
	_tablename_ = 'dadoclp'
	id = Column(Integer, primary_key=True,autoincrement=True)
	timestamp = Column(DataTime)
	temperatura_enrolamento_s = Column(float)
	temperatura_enrolamento_t = Column(float)
	temperatura_carcaca = Column(float)
	temperatura_arSaida = Column(float)
	velocidade_arSaida = Column(float)
	vazao_arSaida = Column(float)
	frequencia_compressor = Column(float)
	frequencia_motor = Column(float)
	mostra_partida = Column(float)
	temp_canVermelho = Column(float)
	temp_canAzul = Column(float)
	pressao_canVerm = Column(float)
	pressao_canAzul = Column(float)
	pressao_arEnt = Column(float)
	pressao_baixaScroll = Column(float)
	pressao_altaScroll = Column(float)
	pressao_baixaHerm = Column(float)
	pressao_altaHerm = Column(float)
	corrente_r = Column(float)
	corrente_s = Column(float)
	corrente_t = Column(float)
	pot_a_total = Column(float)
	freq_motor = Column(float)
	fat_pot_comp = Column(float)
	fat_pot = Column(float)