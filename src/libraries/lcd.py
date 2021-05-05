import streams

import i2c



class lcd:

    def __init__(self, i2c_addr , backlight = True):



        # device constants

        self.I2C_ADDR  = i2c_addr

        self.LCD_WIDTH = 16   # Max. characters per line



        self.LCD_CHR = 1 # Mode - Sending data

        self.LCD_CMD = 0 # Mode - Sending command



        self.LCD_LINE_1 = 0x80 # LCD RAM addr for line one

        self.LCD_LINE_2 = 0xC0 # LCD RAM addr for line two



        if backlight:

            # on

            self.LCD_BACKLIGHT  = 0x08

        else:

            # off

            self.LCD_BACKLIGHT = 0x00



        self.ENABLE = 0b00000100 # Enable bit



        # Timing constants

        self.E_PULSE = 5

        self.E_DELAY = 5



        self.port=i2c.I2C(I2C1, 0x27, 400000) 

        self.port.start()

        self.port.lock()

        self.port.write_bytes(0x33,0) # Inizializzazione

        self.port.write_bytes(0x32,0) # Inizializzazione

        self.port.write_bytes(0x06,0) # Cursore

        self.port.write_bytes(0x0C,0) # Accendi Display

        self.port.write_bytes(0x28,0) # Lunghezza di righe 

        self.port.write_bytes(0x01,0) # reset display 



    def lcd_byte(self, bits, mode):

        # Send byte to data pins

        # bits = data

        # mode = 1 for data, 0 for command



        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT

        bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT



        # High bits

        self.port.write_bytes(self.I2C_ADDR, bits_high)

        self.toggle_enable(bits_high)



        # Low bits

        self.port.write_bytes(self.I2C_ADDR, bits_low)

        self.toggle_enable(bits_low)



    def toggle_enable(self, bits):

        sleep(self.E_DELAY)

        self.port.write_bytes(self.I2C_ADDR, (bits | self.ENABLE))

        sleep(self.E_PULSE)

        self.port.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))

        sleep(self.E_DELAY)



    def message(self, string, line = 1):

        # display message string on LCD line 1 or 2

        lcd_line = self.LCD_LINE_1



        string = string.ljust(self.LCD_WIDTH," ")



        self.port.write_bytes(lcd_line, self.LCD_CMD)



        for i in range(self.LCD_WIDTH):

            self.port.write_bytes(ord(string[i]), self.LCD_CHR)



    def clear(self):

        # clear LCD display

        self.port.write_bytes(0x01, self.LCD_CMD)


