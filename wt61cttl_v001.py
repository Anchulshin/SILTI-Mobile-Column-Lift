import binascii
import serial
import time
from time import sleep
import sys
ser = serial.Serial('/dev/ttyUSB0', 115200)
ser.timeout = 1
class WT61CTTL:
	def __init__(self, period):
		
		self.period = period
		
	def twos_complement(self,hexstr,bits):
		value = int(hexstr,16)
		if value & (1 << (bits-1)):
			value -= 1 << bits
		return value

	def datadp(self):
		if ser.isOpen():
			while 1:
				s = ser.read(11)
				hex_string = binascii.hexlify(s).decode('utf-8')

				packet01 = hex_string[0:2]
				packet02 = hex_string[2:4]
				x_packL = hex_string[4:6]
				x_packH = hex_string[6:8]
				y_packL = hex_string[8:10]
				y_packH = hex_string[10:12]
				z_packL = hex_string[12:14]
				z_packH = hex_string[14:16]
				T_packL = hex_string[16:18]
				T_packH = hex_string[18:20]
				datasum = hex_string[20:22]
				g=9.8
				checksum = int(packet01,base=16) + int(packet02,base=16) + int(x_packH,base=16) + int(x_packL,base=16)
				checksum += int(y_packH,base=16) + int(y_packL,base=16) + int(z_packH,base=16)+ int(z_packL,base=16)
				checksum += int(T_packH,base=16) + int(T_packL,base=16)
				laststr = str(hex(checksum))
				
				len_laststr = len(laststr)
				hex_checksum = laststr[len_laststr-2:len_laststr]
				
				if(hex_checksum == datasum):
					if (packet01 == "55"):
						if (packet02 == "51"): #acceleration pack
							ax = (int(x_packH,base=16)*256+int(x_packL,base=16))/32768*16*g
							ay = (int(y_packH,base=16)*256+int(y_packL,base=16))/32768*16*g
							az = (int(z_packH,base=16)*256+int(z_packL,base=16))/32768*16*g
							aT =  (int(T_packH,base=16)*256+int(T_packL,base=16))/340+36.53
							#print("ax:%6.3f, ay:%6.3f, az:%6.3f, aT:%6.2f"%(ax,ay,az,aT))
						elif (packet02 == "52"): #angular velocity pack
							wx = (int(x_packH,base=16)*256+int(x_packL,base=16))/32768*2000
							wy = (int(y_packH,base=16)*256+int(y_packL,base=16))/32768*2000
							wz = (int(z_packH,base=16)*256+int(z_packL,base=16))/32768*2000
							wT =  (int(T_packH,base=16)*256+int(T_packL,base=16))/340+36.53	
							#print("wx:%6.3f, wy:%6.3f, wz:%6.3f, wT:%6.2f"%(wx,wy,wz,wT))
						elif (packet02 == "53"): #angle pack
							Roll = (int(x_packH,base=16)*256+int(x_packL,base=16))/32768*180
							Pitch = (int(y_packH,base=16)*256+int(y_packL,base=16))/32768*180
							Yaw = (int(z_packH,base=16)*256+int(z_packL,base=16))/32768*180
							rT = self.twos_complement(T_packH+T_packL, 16) / 340+36.53
							print ("Xax(R):%6.3f, Yax(P):%6.3f, Zax(Y):%6.3f, T:%6.2f"%(Roll, Pitch, Yaw, rT))
							result = "Xax(R):"+str("{:.2f}".format(Roll)) +", Yax(P):"+str("{:.2f}".format(Pitch))+", Zax(Y):"+str("{:.2f}".format(Yaw))+", Temp:"+str("{:.1f}".format(rT))
							ser.flushInput() #버퍼삭제기능
							ser.flushOutput() #버퍼삭제기능
							time.sleep(self.period)
							return result
						
						
						

if __name__=="__main__":
	argument = sys.argv
	if len(argument) != 1:
		if (argument[1] != ""):
			t=WT61CTTL(float(argument[1]))
			t.datadp()	
	else:
		t=WT61CTTL(0.5)
		t.datadp()
