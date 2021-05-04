import streams
import adc
import Math
streams.serial()

SERIESRESISTOR = 10000
NOMINAL_RESISTANCE = 10000
NOMINAL_TEMPERATURE = 25
BCOEFFICIENT = 3950
 
ntcPin = A1
pinMode(ntcPin,INPUT_ANALOG)
 
 
 
def read():
    """converts the raw value from the sensor to a value in Celsius  """
    #Gets the raw value from the sensor
    adcValue = adc.read(ntcPin)
    print("analog = %d"%adcValue)
    
    #Gets the resistance
    resistance = (1023 / adcValue)
    resistance = SERIESRESISTOR / resistance
    print("Resistance = %.2f Ohm"%resistance)
    
    
    #gets the temperature value and converts it to celsius
    steinhart = resistance/NOMINAL_RESISTANCE #(R/R0)
    steinhart = Math.log(steinhart,Math.e) #ln(R/R0)
    steinhart = steinhart/BCOEFFICIENT #1/B*ln(R/R0)
    steinhart = steinhart + 1.0/(NOMINAL_TEMPERATURE + 273.15) # (1/B*ln(R/R0)) + 1/T0 
    steinhart = 1/steinhart #inverts the formula
    steinhart = steinhart - 273.15 #converts to Celsius
    
    print("%.1f Celsius"%steinhart)
    return steinhart
    