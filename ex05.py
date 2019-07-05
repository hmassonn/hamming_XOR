import sys
import base64
import codecs

rating_of_analyze = 70
keysize_min = 2
keysize_max = 40
KEYSIZE = 2

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

def get_file():
    file = open("05.txt")
    return base64.b64decode(file.read())

def convert(text, key):
    size_key = 0
    long_key = ''
    for each in text:
        long_key += key[size_key]
        size_key += 1
        if size_key == len(key):
            size_key = 0
    long_key += key[size_key]
    decoction = bytes(text, 'utf-8')
    decokey = bytes(long_key, 'utf-8')
    text = xoring(decoction, decokey)
    return encode_hex(text)

def hamming(one, two):
    som = 0
    for c1, c2 in zip(one, two):
        if c1 != c2:
            som += 1
    one = str(encode_hex(bytes(one, 'utf-8')))
    two = str(encode_hex(bytes(two, 'utf-8')))
    for c1, c2 in zip(one, two):
        if c1 != c2:
            som += 1
    return som

def simple_hamming(cipher_text, try_key):
    nb_block = len(cipher_text) // (try_key * 2) - 1
    two_block = try_key * 2
    # copy = list(cipher_text)
    som = 0
    for i in range(nb_block):
        first_block = cipher_text[slice((i * two_block), (i * two_block) + try_key)]
        second_block = cipher_text[slice((i * two_block) + try_key, (i * two_block) + two_block)]
        som += hamming(first_block, second_block)
    som /= try_key * nb_block
    return(som)

def battery_hamming(cipher_text):
    list_size_key = {}
    for one_key in range(keysize_min, keysize_max):
        list_size_key[one_key] = simple_hamming(cipher_text, one_key)
        # print("key (", aff_one, ") : ", simple_hamming(cipher_text, one_key))
    return list_size_key

# print(hamming('this is a test', 'wokka wokka!!!'))
# print(str(get_file(), 'utf-8'))

# s = 'Hello world'
# l = list(s)
# l[6] = 'W'
# s = "".join(l) # s = 'Hello World'

list_size_key = battery_hamming(str(get_file(), 'utf-8'))
print(sorted(list_size_key.items(), key = lambda kv:(kv[1], kv[0])))   