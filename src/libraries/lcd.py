import streams
import i2c

BL_SHIFT = 3

ENABLE = 0b00000100 # Enable mask

LCD_PANIC = 48
SETENTRY = 4
INCREMENTA = 2
CONFIG = 32
LINEE = 8
DISP = 8
DISPON = 4

LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command
LCD_LINE_1 = 0x80 # LCD RAM addr for line one
LCD_LINE_2 = 0xC0 # LCD RAM addr for line twoself
        
class lcd:
    def __init__(self, i2cport = I2C1, i2c_addr = 0x27, backlight = True):# device constants
        self.I2C_ADDR = i2c_addr
        self.LCD_WIDTH = 16 # Max. characters per line
        self.backup = 0
        
        self.comm = i2c.I2C(i2cport, i2c_addr, 100000)
        self.comm.start()

        self.backlight = backlight
        
        # Timing constants
        self.E_PULSE = 5
        self.E_DELAY = 5
        
        # Initialise display
        self.i2c_helperWrite(LCD_PANIC)
        self.toggle_enable()
        sleep(5)
        
        self.i2c_helperWrite(LCD_PANIC)
        self.toggle_enable()
        sleep(2)
        
        self.i2c_helperWrite(LCD_PANIC)
        self.toggle_enable()
        sleep(2)
   
        self.i2c_helperWrite(CONFIG)
        self.toggle_enable()
        
        self.lcd_byte(CONFIG | LINEE, LCD_CMD) 
        self.lcd_byte(DISP | DISPON, LCD_CMD) 
        self.lcd_byte(SETENTRY | INCREMENTA, LCD_CMD) 
        self.clear()
        
        sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = 1 for data, 0 for command
        
        bits_high = mode | (bits & 0xF0) | (self.backlight << BL_SHIFT)
        # High bits
        self.i2c_helperWrite(bits_high)
        self.toggle_enable()
        
        bits_low = mode | ((bits<<4) & 0xF0) | (self.backlight << BL_SHIFT)
        # Low bits
        self.i2c_helperWrite(bits_low)
        self.toggle_enable()
        
        sleep(1)
    
    def i2c_helperWrite(self, data):
        self.backup = data
        self.comm.write(data)

    def toggle_enable(self):
        sleep(self.E_DELAY)
        self.i2c_helperWrite (self.backup | ENABLE)
        sleep(self.E_DELAY)
        self.i2c_helperWrite (self.backup & ~ENABLE)
        sleep(self.E_DELAY)
        
    def message(self, string, line = 1):
        # display message string on LCD line 1 or 2
        if line == 1:
            lcd_line = LCD_LINE_1
        elif line == 2:
            lcd_line = LCD_LINE_2
        else:
            raise Exception
        
        if len(string)>self.LCD_WIDTH:
            string = string[0:self.LCD_WIDTH]

        self.lcd_byte(lcd_line, LCD_CMD)

        for i in range(len(string)):
            self.lcd_byte(ord(string[i]), LCD_CHR)
        
    def clear(self):
        # clear LCD display
        self.lcd_byte(0x01, LCD_CMD)