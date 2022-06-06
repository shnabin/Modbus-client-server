from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataBank
import time

c = ModbusClient(host="10.10.20.100", port=502, unit_id=1, auto_open=True) #client connection
regs = c.read_holding_registers(200, 5) #Read the holding registers
while True:
    if regs:
        print('reg ad #0 to 15: %s' % regs)
    else:
        print("read error")
    
    server = ModbusServer("192.168.2.200", 12345, no_block=True) #Server connection   
    server.start() 
    DataBank.set_words(0, regs) #Assigning the Server with values so client can read
    state = DataBank.get_words(1) #name tags 
    print("Value of Register 1 has changed to ", state)
    time.sleep(2)
    
