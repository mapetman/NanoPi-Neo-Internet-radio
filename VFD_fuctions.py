#!/usr/bin/python
import smbus
import time
ADDRESS = 0x50        #address of VFD - IMPORTANT NOTE: according to datasheet it is wite only
bus = smbus.SMBus(0)    #NanoPi NEO has I2c_0 and I2c_2, I2c_0 is connected to pins

#Chars coded to VFD 2 byte format. Although Futaba single sign has three bytes, the last one is 0x00. 
#Third byte bellow is used to find single char from string that has to be displayed - see findcharposition() 
chars = [
		[0x3f, 0xa2, "0"],
		[0x06, 0x02, "1"],
		[0x5b, 0x84, "2"],
		[0b01111001, 0b10000000, "3"],
		[0b01110100, 0b10000100, "4"],
		[0b01101101, 0b10000100, "5"],
		[0b01101111, 0b10000100, "6"],
    [0b00111000, 0b00000000, "7"],
		[0b01111111, 0b10000100, "8"],
		[0b00000110, 0b00000000, "9"],
		[0x77, 0x84, "A"],
		[0x8F, 0xA4, "B"], 
		[0x39, 0x00, "C"],
		[0x8F, 0x20, "D"],
		[0x79, 0x80, "E"],
		[0x71, 0x80, "F"],
		[0x3d, 0x84, "G"],
		[0x76, 0x84, "H"],
		[0x00, 0xd1, "I"],
		[0x0e, 0x00, "J"],
		[0x70, 0x8a, "K"],
		[0x38, 0x00, "L"],
		[0xb6, 0xc2, "M"],
		[0xb6, 0x88, "N"],
		[0x3f, 0x00, "O"],
		[0x73, 0x84, "P"],
		[0x73, 0x8c, "R"],
		[0x6d, 0x84, "S"],
		[0x01, 0xd1, "T"],
		[0x3e, 0x00, "U"],
		[0x36, 0xa8, "W"],
		[0x80, 0xaa, "X"],
		[0x80, 0x92, "Y"],
		[0x09, 0xa2, "Z"],
		[0x58, 0x88, "a"],
		[0x78, 0x88, "b"],
		[0x78, 0x84, "c"],
		[0x0e, 0xa4, "d"],
		[0x70, 0x88, "h"],
		[0x00, 0x90, "i"],
		[0x00, 0xdd, "k"],
		[0x00, 0x94, "l"],
		[0x54, 0x94, "m"],
		[0x5c, 0x84, "o"],
		[0x00, 0x94, "r"],
		[0x40, 0x84, "-"],
		[0x08, 0x00, "_"],
		[0x40, 0xc4, "+"],
		[0x00, 0xa2, "/"],
		[0x80, 0x88, "\\"],
		[0x6d, 0x91, "$"],
		[0x80, 0xa0, ">"],
		[0x00, 0x8a, "<"],
		[0x00, 0x91, "|"],
		[0x00, 0x40, ":"],
		[0x00, 0x01, "'"],
		[0x00, 0x00, " "],
		]


# digit number - static addresses of first byte of every single sign, VFD matrix is 1x12 
digit = [0xc0, 0xc0 + 0x03, 0xc0 + 0x06, 0xc0 + 0x09, 0xc0 + 0x0c, 0xc0 + 0x0f, 0xc0 + 0x12, 0xc0 + 0x15, 0xc0 + 0x18, 0xc0 + 0x1b, 0xc0 + 0x1e, 0xc0 + 0x21]

#VFD reset - clears all data in VFD register (LED's not included)
def clearVFD():	
	bus.write_byte(ADDRESS, 0x08)
	bus.write_byte(ADDRESS, 0x44)
	i = 0
	while i < 12:
		bus.write_byte_data(ADDRESS, digit[i], 0x00)
		bus.write_byte_data(ADDRESS, digit[i] + 1, 0x00)
		i += 1

#Function finds position in coded char table
def findcharposition(char):
	i = 0
	while i < 57:
			if chars[i][2] == str(char):
				return i
				break
			i += 1
	return "err"	



#MAIN PART
#Commands to set VFD to write without incrementation of address
bus.write_byte(ADDRESS, 0x08)
bus.write_byte(ADDRESS, 0x44)

#Displayed text
text = "M12A"

VFDreset()

#Write chars to VFD
for index in range(len(text)):
	text1 = text[:index + 1]
	#print "index: " 
	#print index
	#print text1
	#print text1[-1:]
	lit = findcharposition(text1[-1:])
	bus.write_byte_data(ADDRESS, digit[index], chars[lit][0])
	bus.write_byte_data(ADDRESS, digit[index] + 1, chars[lit][1])
	bus.write_byte(ADDRESS, 0x9f)
	time.sleep(0.25)
