import sys
import base64
import codecs

decode_hex = codecs.getdecoder("hex_codec")
def encode_hex(s):
	return codecs.encode(s, "hex_codec").decode("utf-8") 
decode = decode_hex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')[0]
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

for i in range(0, 255):
	i_b = i.to_bytes(1, byteorder='big')
	result = single_xoring(decode, i_b)
	if evaluate(result) > 68:
		print(result)

