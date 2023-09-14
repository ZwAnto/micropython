import re
from machine import UART

def validate(b):
    if (sum(b[:-1]) & 0x3f) + 0x20 == b[-1]:
        return b[:-2].split(b"\x09")
    else:
        raise Exception("Checksum validation faile for {}".format(b.decode('utf-8')))

def parse_date(date):
    tz = 'CEST' if date[0] == 'E' else 'CET'
    year = date[1:3]
    month = date[3:5]
    day = date[5:7]
    hour = date[7:9]
    minute = date[9:11]
    second = date[11:13]
    
    return "{}-{}-{} {}:{}:{} {}".format(day, month, year, hour, minute, second, tz)

def read():
    regex_trame = re.compile(b'[\x0a\x0d]')
    uart = UART(1, 9600, bits=7, parity=0, stop=1, rx=20, tx=21, timeout=20)
    status = {'EAST': False, 'SINSTS': False, 'DATE': False}
    counter = 0
    while not all(status.values()) and counter < 500:
        try:
            line = uart.readline()
            assert line is not None
            
            line = regex_trame.sub('',line)
            line = validate(line)
            
            if line[0].decode('utf-8') in status.keys():
                status[line[0].decode('utf-8')] = line[1].decode('utf-8')
                
        except Exception as e:
            #print(e)
            pass
        finally:
            counter +=1
    
    if status['DATE']:
        status['DATE'] = parse_date(status['DATE'])
        
    if status['SINSTS']:
        status['SINSTS'] = int(status['SINSTS'])
        
    if status['EAST']:
        status['EAST'] = int(status['EAST'])
        
    return status

