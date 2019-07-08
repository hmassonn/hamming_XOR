import sys
import base64
import codecs

decode_hex = codecs.getdecoder("hex_codec")
def encode_hex(s):
	return codecs.encode(s, "hex_codec").decode("utf-8") 
decode = decode_hex('370317191c10074c1c075307070d0f1c53151a190b531000014c1c0b161716051a165344552917051c1c101659051c1107095930254506190b531d0a011e1c53120107090a001645180d101f530110411a1b12170c0e1d165e001b410a100a09190d39100a07101e0e1207061d421f015f45140f1a1c1e15140b17b0da45111959101c01104c0806164503030c0053040309035306111c001000b0cc551c160601451a0e0d161d0c074c1a165308101f0a1214005b4c371c0616551a1606004507091a1c1d11140f0d16010a1b1f5917120b064c1516004505000c00530707091f005301b6c515121a16550d0f16104500021c5303171a1c16001a111c0317531700551e1c1d17000f410f1c06165b')[0]
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
	if evaluate(result) > 70:
		print(i_b, " : ")
		print(result)

