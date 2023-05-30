import serial
import base64
import struct

jpeg_data = b''
frame_num_current = 0

with serial.Serial('/dev/ttyUSB0', 1000000, timeout=3) as ser:
    while 1:
        sdata_bytes = ser.readline()
        sdata_base64 = sdata_bytes.decode('ascii').strip()
        sdata = base64.b64decode(sdata_base64)
        try:
            frame_num, offset, jpeg_segment = struct.unpack('II242s', sdata)
            if frame_num != frame_num_current:
                with open('frame.jpg', 'wb') as f:
                    f.write(jpeg_data)
                frame_num_current = frame_num
                jpeg_data = b''
            jpeg_data += jpeg_segment
        except Exception as e:
            print(e)
            continue
        

        