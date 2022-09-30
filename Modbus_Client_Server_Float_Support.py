from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataBank
import time
from pyModbusTCP import utils
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
    rad = utils.encode_ieee(irr[0])
    reg5 = c.read_input_registers(67, 2)
    tmod = [decode_ieee(f) for f in word_list_to_long(reg5)]
    temp = utils.encode_ieee(tmod[0])
    ####Janitza
    reg1 = j.read_input_registers(19632, 2)
    Vavg = [decode_ieee(f) for f in word_list_to_long(reg1)]
    Vu = utils.encode_ieee(Vavg[0])
    reg2 = j.read_input_registers(19026, 2)
    Power = [decode_ieee(f) for f in word_list_to_long(reg2)]
    Pac = utils.encode_ieee(Power[0])
    reg3 = j.read_input_registers(19042, 2)
    RP = [decode_ieee(f) for f in word_list_to_long(reg3)]
    Qac = utils.encode_ieee(RP[0])
    ####Dummy values
    raw = dummy+Vavg+Power+RP+irr+tmod
    #data = [i * 100 for i in raw]
    log.debug("Field values: "+str(raw))
    ####----------------------server instance-------------------########
    ##Voltage value
    server.data_bank.set_holding_registers(4, [(Vu&0xffff0000)>>16, Vu&0xffff]) #Assigning the Server with values so client can read
    state = server.data_bank.get_holding_registers(4,2)
    Voltage = [decode_ieee(f) for f in word_list_to_long(state)]
    log.debug("Voltage values: "+str(Voltage))
    ##Int values
    server.data_bank.set_holding_registers(0, dummy) #Assigning the Server with values so client can read
    state1 = server.data_bank.get_holding_registers(0,3)
    log.debug("Server values: "+str(state1))
    ##Power value
    server.data_bank.set_holding_registers(6, [(Pac&0xffff0000)>>16, Pac&0xffff]) #Assigning the Server with values so client can read
    state2 = server.data_bank.get_holding_registers(6,2)
    Pow = [decode_ieee(f) for f in word_list_to_long(state2)]
    log.debug("Power values: "+str(Pow))
    ##Reactive value
    server.data_bank.set_holding_registers(8, [(Qac&0xffff0000)>>16, Qac&0xffff]) #Assigning the Server with values so client can read
    state3 = server.data_bank.get_holding_registers(8,2)
    Reactive = [decode_ieee(f) for f in word_list_to_long(state3)]
    log.debug("Reactive values: "+str(Reactive))
    ##Radiation value
    server.data_bank.set_holding_registers(10, [(rad&0xffff0000)>>16, rad&0xffff]) #Assigning the Server with values so client can read
    state4 = server.data_bank.get_holding_registers(10,2)
    Radiation = [decode_ieee(f) for f in word_list_to_long(state4)]
    log.debug("Radiation values: "+str(Radiation))
    ##Module temp value
    server.data_bank.set_holding_registers(12, [(temp&0xffff0000)>>16, temp&0xffff]) #Assigning the Server with values so client can read
    state5 = server.data_bank.get_holding_registers(12,2)
    Tmodu = [decode_ieee(f) for f in word_list_to_long(state5)]
    log.debug("Tmod values: "+str(Tmodu))
    
    c.close()
    j.close()
    time.sleep(5)
