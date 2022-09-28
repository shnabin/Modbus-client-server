from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataBank
import time
from pyModbusTCP.utils import encode_ieee, decode_ieee, \
                              long_list_to_word, word_list_to_long

# configure the service logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


###modbus connections 
c = ModbusClient(host='192.168.46.114', port=502, auto_open=True)
j = ModbusClient(host='192.168.46.105', port=502, auto_open=True)
dummy = [1,207,0]
server = ModbusServer("127.0.0.1", 5022, no_block=True) #Server connection   
server.start() 

while True:
    ###weather station
    reg4 = c.read_input_registers(51, 2)
    irr = [decode_ieee(f) for f in word_list_to_long(reg4)]
    reg5 = c.read_input_registers(67, 2)
    tmod = [decode_ieee(f) for f in word_list_to_long(reg5)]
    ####meter
    reg1 = j.read_input_registers(19632, 2)
    Vavg = [decode_ieee(f) for f in word_list_to_long(reg1)]
    reg2 = j.read_input_registers(19026, 2)
    Power = [decode_ieee(f) for f in word_list_to_long(reg2)]
    reg3 = j.read_input_registers(19042, 2)
    RP = [decode_ieee(f) for f in word_list_to_long(reg3)]
    ####Dummy values
    data = dummy+irr+tmod+Vavg+Power+RP
    log.debug("Field values: "+str(data))
    ####server instance
    server.data_bank.set_holding_registers(0, data) #Assigning the Server with values so client can read
    state = server.data_bank.get_holding_registers(0,8)
    log.debug("Server values: "+str(state))
    c.close()
    j.close()
    time.sleep(10)
