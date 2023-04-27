from machine import Pin, UART, PWM

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
pin = PWM(Pin(25, mode= Pin.OUT))
pin.freq(10000)
while True:
    if uart.any():
        message_bytes = uart.read()
        message = message_bytes.decode('utf-8')
        li = list(message.split(","))
        li = list(map(int, li))
        print(li)
        pin.duty_u16(int(li[4]*1000))

