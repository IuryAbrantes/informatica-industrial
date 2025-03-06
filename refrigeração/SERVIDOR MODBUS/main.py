from servidormodbus import ServidorMODBUS #Importa servidor

s = ServidorMODBUS('localhost',502) #Cria servidor conectado a 502 (Sistema de refigeração)
s.run() #Inicia o servidor