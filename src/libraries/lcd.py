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



# Initialise display

        self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise

        self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise

        self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction

        self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 

        self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size

        self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display

        sleep(self.E_DELAY)

        

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

        self.port.write.byte(self.I2C_ADDR, (bits | self.ENABLE))

        sleep(self.E_PULSE)

        self.port.write_byte(self.I2C_ADDR,(bits & self.ENABLE))

        sleep(self.E_DELAY)



    def message(self, text):

    # Send string to display

        for char in text:

            if char == '\n':

                self.lcd_byte(0xC0, self.LCD_C)  # next line

            else:

                self.lcd_byte(ord(char), self.LCD_CHR)





    def clear(self):

        # clear LCD display

        self.port.write_bytes(0x01, self.LCD_CMD)


