import sys
import base64

decode =  sys.argv[1].decode("hex")
print decode
decode = '1c0111001f010100061a024b53535009181c'
against = "686974207468652062756c6c277320657965"
res = ""

for i, x in enumerate(decode, start=0):
	res += format(int(x, 16) ^ int(against[i], 16), 'x')
print res

