import smbus

class INA260:
    
    _INA260_DEVICE_ADDRESS   = 0x44
    _INA260_CONFIG_ADDR      = 0x00
    _INA260_ADC_CONFIG_ADDR  = 0x01
    _INA260_CURRENT_ADDR     = 0x07
    _INA260_DIETEMP_ADDR     = 0x06
    _INA260_MANFID_ADDR      = 0x3E
    _INA260_BUS_VOLTAGE_ADDR = 0x05
    _INA260_BUS_VOLTAGE_LSB  = 3.125 #mV
    _INA260_CURRENT_LSB      = 0.480 #mA
    
        # Constructor
    def __init__(self, dev_address=_INA260_DEVICE_ADDRESS):
        self.i2c = smbus.SMBus(1) #/dev/i2c-1
        self.dev_address = dev_address
    
    def twos_compliment_to_int(self, val, len):
        # Convert twos compliment to integer
        if(val & (1 << len - 1)):
            val = val - (1<<len)
        return val

    def get_temperature(self):
        raw_read = self.i2c.read_i2c_block_data(self.dev_address,self._INA260_DIETEMP_ADDR,2)
        word_rdata = raw_read[0] *256 + raw_read[1]
        print(raw_read, word_rdata)
        temperature_twos_compliment = word_rdata >> 4
        temperature_sign_bit = temperature_twos_compliment >> 15
        temp = float(self.twos_compliment_to_int(temperature_twos_compliment, 12)) / 1000.0 * 125
        return temp
        
    def get_bus_voltage(self):
        raw_read = self.i2c.read_i2c_block_data(self.dev_address,self._INA260_BUS_VOLTAGE_ADDR,2)
        word_rdata = raw_read[0] *256 + raw_read[1]
        vbus = float(word_rdata) / 1000.0 * self._INA260_BUS_VOLTAGE_LSB
        return vbus

    def get_current(self):
        raw_read = self.i2c.read_i2c_block_data(self.dev_address,self._INA260_CURRENT_ADDR,2)
        word_rdata = raw_read[0] *256 + raw_read[1]
        current_twos_compliment = word_rdata
        current_sign_bit = current_twos_compliment >> 15
        if (current_sign_bit == 1):
            current = float(self.twos_compliment_to_int(current_twos_compliment, 16)) / 1000.0 * self._INA260_CURRENT_LSB
        else:
            current = float(current_twos_compliment) / 1000.0 * self._INA260_CURRENT_LSB
        return current



    def get_manfid(self):
        raw_read = self.i2c.read_i2c_block_data(self.dev_address,self._INA260_MANFID_ADDR,2)
        word_rdata = raw_read[0] *256 + raw_read[1]
        print(hex(word_rdata))
    
    def reset_chip(self):

        MODE = 0xf #continous temperatur voltage
        VBUSCT = 0x7 # 4120us
        VSENCT = 0x7

        byte_list = [0xc1, 0x00]
        self.i2c.write_i2c_block_data(self.dev_address,self._INA260_CONFIG_ADDR,byte_list)


        byte_list = [0xff, 0xef]
        self.i2c.write_i2c_block_data(self.dev_address,self._INA260_ADC_CONFIG_ADDR,byte_list)

        self.get_manfid()
