from onl.platform.base import *
from onl.platform.accton import *
from time import sleep

class OnlPlatform_x86_64_accton_as7946_74xkb_r0(OnlPlatformAccton,
                                              OnlPlatformPortConfig_2x400_8x100_64x25):
    PLATFORM='x86-64-accton-as7946-74xkb-r0'
    MODEL="AS7946-74XKB"
    SYS_OBJECT_ID=".7946.74"

    def baseconfig(self):
        self.insmod('optoe')
        for m in [ 'sys' , 'cpld', 'fan', 'psu', 'leds', 'thermal' ]:
            self.insmod("x86-64-accton-as7946-74xkb-%s.ko" % m)

        ########### initialize I2C bus 0 ###########
        self.new_i2c_devices([
                # initialize multiplexer (PCA9548)
                ('pca9548', 0x77, 0), # i2c 1-8
                
                # initialize multiplexer (PCA9548) of main board
                ('pca9548', 0x76, 1), # i2c 9-16

                # initiate  multiplexer (PCA9548) for QSFP ports
                ('pca9548', 0x73, 9),  # i2c 17-24
                ('pca9548', 0x73, 14), # i2c 25-32

                # initiate multiplexer for QSFP ports
                ('pca9548', 0x74, 17), # i2c 33-40
                ('pca9548', 0x74, 18), # i2c 41-48
                ('pca9548', 0x74, 19), # i2c 49-56
                ('pca9548', 0x74, 20), # i2c 57-64
                ('pca9548', 0x74, 21), # i2c 63-72
                ('pca9548', 0x74, 22), # i2c 73-80
                ('pca9548', 0x74, 23), # i2c 81-88
                ('pca9548', 0x74, 24), # i2c 89-96
                ('pca9548', 0x74, 25), # i2c 97-104
                ('pca9548', 0x74, 26), # i2c 105-106

                #initiate CPLD
                ('as7946_74xkb_cpld1', 0x61, 12),
                ('as7946_74xkb_cpld2', 0x62, 13),
                ('as7946_74xkb_cpld3', 0x63, 16),
                ])

        # initialize QSFP port(0-1), QSFP28 port(2-10), SFP port(11-74)
        port_i2c_bus = [ 33,  34,  35,  36,  37,  38,  39,  40,  41,  42,
                         43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
                         53,  54,  55,  56,  57,  58,  59,  60,  61,  62,
                         63,  64,  65,  66,  67,  68,  69,  70,  71,  72,
                         73,  74,  75,  76,  77,  78,  79,  80,  81,  82,
                         83,  84,  85,  86,  87,  88,  89,  90,  91,  92,
                         93,  94,  95,  96,  97,  98,  99, 100, 101, 102,
                        103, 104, 105, 106]

        # initialize QSFP port 33-42
        for port in range(0, 10):
            self.new_i2c_device('optoe1', 0x50, port_i2c_bus[port])
            subprocess.call('echo port%d > /sys/bus/i2c/devices/%d-0050/port_name' % (port, port_i2c_bus[port]), shell=True)

        # initialize SFP port 43-106
        for port in range(10, 74):
            self.new_i2c_device('optoe2', 0x50, port_i2c_bus[port])
            subprocess.call('echo port%d > /sys/bus/i2c/devices/%d-0050/port_name' % (port, port_i2c_bus[port]), shell=True)

        return True
