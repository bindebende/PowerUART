from silta import stm32f407

class VoltageRegulator:
    __bridge = 0

    # GPIO IN pins
    __PGOOD = 'PD2'
    __CC1 = 'PD0'
    __CC2 = 'PD2'

    # ADC pins
    __COMP = 'PB4'
    __VSNS = 'PA0'
    __LED5VWP = 'PA1'
    __Out5V = 'PA2'
    __SS_TR = 'PB1'
    __CLK = 'PB2'



    def __init__(self, serial):

        self.bridge = stm32f407.bridge(serial)

        # config GPIO inputs
        self.bridge.gpiocfg(self.__PGOOD, 'input')
        self.bridge.gpiocfg(self.__CC1, 'input')
        self.bridge.gpiocfg(self.__CC2, 'input')

        # config Analog inputs
        self.bridge.gpiocfg(self.__COMP, 'analog')
        self.bridge.gpiocfg(self.__VSNS, 'analog')
        self.bridge.gpiocfg(self.__LED5VWP, 'analog')
        self.bridge.gpiocfg(self.__Out5V, 'analog')
        self.bridge.gpiocfg(self.__CLK, 'analog')
        self.bridge.gpiocfg(self.__SS_TR, 'analog')


    def checkSupply(self):
        result = {}

        value_VSNS = self.bridge.adc(self.__VSNS)

        # compensate the voltage drop from the feedback resistors
        value_VSNS *= 6.25

        if(value_VSNS > 4.9 and value_VSNS < 5.1):
            result['VSNS']={'value':value_VSNS,'result':'Passed'}
        else:
            result['VSNS'] = {'value': value_VSNS, 'result': 'Failed'}

        # read 5v input
        value5V = self.bridge.adc(self.__Out5V)
        # compensate the EOL input voltage divider
        value5V *= 2

        if(value5V > 4.9 and value5V < 5.1):
            result['5v']={'value':value_VSNS,'result':'Passed'}
        else:
            result['5v'] = {'value': value_VSNS, 'result': 'Failed'}

        # read 5v LED input
        value5VLED = self.bridge.adc(self.__Out5V)
        # compensate the EOL input voltage divider
        value5VLED *= 2

        if (value5VLED > 4.9 and value5VLED < 5.1):
            result['5v_LED'] = {'value': value_VSNS, 'result': 'Passed'}
        else:
            result['5v_LED'] = {'value': value_VSNS, 'result': 'Failed'}





        return result