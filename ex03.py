import sys
import base64
import codecs

rating_of_analyze = 70

def encode_hex(s):
	return codecs.encode(s, "hex_codec").decode("utf-8") 
def decoderin(s):
    decode_hex = codecs.getdecoder("hex_codec")
    return decode_hex(s)[0]
letters = list(range(97, 122)) + [32]

def single_xoring(s1, c):
	s2 = c * len(s1)
	return bytes([ a ^ b for (a, b) in zip(s1, s2)])

def evaluate(strin):
	total = 0
	maxtot = 0
	for c in strin:
		maxtot += 1
		for x in letters:
			if c == x:
				total += 1
	return (total / maxtot) * 100

def analyze_single_xor(s):
    for i in range(0, 255):
        i_b = i.to_bytes(1, byteorder='big')
        result = single_xoring(decoderin(s), i_b)
        if evaluate(result) > rating_of_analyze:
            print(result)

file = open("03.txt","r")
for line in file:
    if (line[len(line)-1] == '\n'):
        analyze_single_xor(line[:-1])
    else:
        analyze_single_xor(line)
