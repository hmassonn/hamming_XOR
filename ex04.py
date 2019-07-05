import sys
import base64
import codecs

rating_of_analyze = 70

def encode_hex(s):
	return codecs.encode(s, "hex_codec")
def decoderin(s):
    decode_hex = codecs.getdecoder("hex_codec")
    return decode_hex(s)[0]
letters = list(range(97, 122)) + [32]

# def single_xoring(s1, c):
# 	s2 = c * len(s1)
# 	return bytes([ a ^ b for (a, b) in zip(s1, s2)])

def xoring(s1, s2):
	return bytes([ a ^ b for (a, b) in zip(s1, s2)])

# def convert_multi_single(text, key):
#     decoction = encode_hex(bytes(text, 'utf-8'))
#     for k in key:
#         k = ord(k)
#         k_b = k.to_bytes(1, byteorder='big')
#         decoction = single_xoring(decoction, k_b)
#         # text = str(text, 'utf-8')
#         print(decoction)
#         print(k_b)
#     text = encode_hex(decoction)
#     return str(text, 'utf-8')

def convert(text, key):
    k = 0
    long_key = ''
    for each in text:
        long_key += key[k]
        k += 1
        if k == 3:
            k = 0
    long_key += key[k]
    decoction = bytes(text, 'utf-8')
    decokey = bytes(long_key, 'utf-8')
    text = xoring(decoction, decokey)
    return encode_hex(text)

text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"
result = convert(text, key)
print(str(result, 'utf-8'))