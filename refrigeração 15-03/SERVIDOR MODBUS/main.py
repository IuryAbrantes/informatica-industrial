from servidormodbus import ServidorMODBUS #Importa servidor

s = ServidorMODBUS('127.0.0.1',502) #Cria servidor conectado a 502 (Sistema de refigeração)
s.run() #Inicia o servidor