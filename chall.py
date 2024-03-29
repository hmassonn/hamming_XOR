import sys
import base64
import codecs
import binascii

KEYSIZE_MIN = 1
KEYSIZE_MAX = 50
# KEYSIZE = 2
PROBA_LETTER = 70

def encode_hex(s):
	return codecs.encode(s, "hex_codec")
def decoderin(s):
	decode_hex = codecs.getdecoder("hex_codec")
	return decode_hex(s)[0]
letters = list(range(97, 122)) + [32]

def single_xoring(s1, c):
	s2 = c * len(s1)
	return bytes([ a ^ b for (a, b) in zip(s1, s2)])

def xoring(s1, s2):
	return bytes([ a ^ b for (a, b) in zip(s1, s2)])

def convert_multi_single(text, key):
	decoction = encode_hex(bytes(text, 'utf-8'))
	for k in key:
		k = ord(k)
		k_b = k.to_bytes(1, byteorder='big')
		decoction = single_xoring(decoction, k_b)
		# text = str(text, 'utf-8')
		print(decoction)
		print(k_b)
	text = encode_hex(decoction)
	return str(text, 'utf-8')

def get_file():
	file = open("05.txt")
	return str(base64.b64decode(file.read()), 'utf-8')

def convert(text, key):
	size_key = 0
	long_key = ''
	for each in text:
		# print(long_key)
		# print(key)
		long_key += key[size_key]
		size_key += 1
		if size_key == len(key):
			size_key = 0
	long_key += key[size_key]
	decoction = bytes(text, 'utf-8')
	decokey = bytes(long_key, 'utf-8')
	text = xoring(decoction, decokey)
	return encode_hex(text)

# we check number of bits between 2 chains for hamming analyse
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

# we cut the chain in blocks for hamming two blocks together
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

# for each size of key between KEYSIZE_MIN and KEYSIZE_MAX we check hamming distance
# return list of hamming by 
def battery_hamming(cipher_text):
	list_size_key = {}
	for one_key in range(KEYSIZE_MIN, KEYSIZE_MAX):
		list_size_key[one_key] = simple_hamming(cipher_text, one_key)
	return list_size_key

# we cut all block of size_key by new chain of same unique key
def get_list_of_key_block(size_key, cipher_text):
	all_lists = [''] * size_key
	for i in range(size_key):
		y = i
		while y < len(cipher_text):
			all_lists[i] += cipher_text[y]
			y += size_key
	return all_lists

def evaluate(strin):
	total = 0
	maxtot = 0
	for c in strin:
		maxtot += 1
		for x in letters:
			if c == x:
				total += 1
	return (total / maxtot) * 100

# get bests results for analyse of bruteforced single XOR
def brute_forced(cipher_string):
	breaking_cipher_list = []
	for i in range(0, 255):
		i_b = i.to_bytes(1, byteorder='big')
		result = single_xoring(decoderin(cipher_string), i_b)
		# print(evaluate(result), PROBA_LETTER, evaluate(result) > PROBA_LETTER)
		if evaluate(result) > PROBA_LETTER:
			# breaking_cipher_list.insert(len(breaking_cipher_list), result)
			breaking_cipher_list.insert(len(breaking_cipher_list), i_b)
	return breaking_cipher_list

# loop on all chain
def brutalize_all_lists(list_block):
	for one_str in list_block:
		str_encode = binascii.hexlify(codecs.encode(one_str)).decode('ascii')
		# print(codecs.encode(str_encode))
		print(brute_forced(str_encode))

def better_ranking_letter(cipher_string, key=''):
	breaking_cipher_list = [None, '']
	# for i in range(0, 255):
	for i in letters:
		# print(key + chr(i))
		# print(breaking_cipher_list[1])
		result = convert(cipher_string, key + chr(i))
		if breaking_cipher_list[0] == None:
			breaking_cipher_list[0] = result
			breaking_cipher_list[1] = i
		elif evaluate(result) > evaluate(breaking_cipher_list[0]):
			breaking_cipher_list[0] = result
			breaking_cipher_list[1] = i
		print(evaluate(result), chr(i))
	return breaking_cipher_list[1]

def one_by_one(hexipher_text):
	key = ''
	for each in range(0, 47):
		key += chr(better_ranking_letter(hexipher_text, key))
		last_key = key[len(key)-1]
		hexipher_text = binascii.hexlify(convert(hexipher_text, last_key)).decode('utf-8')
		print("key:", key)
		# print("text : ", hexipher_text)


# cipher_text = get_file()
cipher_text = 'NwMXGRwQB0wcB1MHBw0PHFMVGhkLUxAAAUwcCxYXFgUaFlNEVSkXBRwcEBZZBRwRBwlZMCVFBhkLUx0KAR4cUxIBBwkKABZFGA0QH1MBEEEaGxIXDA4dFl4AG0EKEAoJGQ05EAoHEB4OEgcGHUIfAV9FFA8aHB4VFAsXsNpFERlZEBwBEEwIBhZFAwMMAFMEAwkDUwYRHAAQALDMVRwWBgFFGg4NFh0MB0waFlMIEB8KEhQAW0w3HAYWVRoWBgBFBwkaHB0RFA8NFgEKGx9ZFxILBkwVFgBFBQAMAFMHBwkfAFMBtsUVEhoWVQ0PFhBFAAIcUwMXGhwWABoRHAMXUxcAVR4cHRcAD0EPHAYWWw=='
hexipher_text = '370317191c10074c1c075307070d0f1c53151a190b531000014c1c0b161716051a165344552917051c1c101659051c1107095930254506190b531d0a011e1c53120107090a001645180d101f530110411a1b12170c0e1d165e001b410a100a09190d39100a07101e0e1207061d421f015f45140f1a1c1e15140b17b0da45111959101c01104c0806164503030c0053040309035306111c001000b0cc551c160601451a0e0d161d0c074c1a165308101f0a1214005b4c371c0616551a1606004507091a1c1d11140f0d16010a1b1f5917120b064c1516004505000c00530707091f005301b6c515121a16550d0f16104500021c5303171a1c16001a111c0317531700551e1c1d17000f410f1c06165b'
# print(len(cipher_text))
list_size_key = battery_hamming(cipher_text)
list_of_ranked_size = sorted(list_size_key.items(), key = lambda kv:(kv[1], kv[0]))
one_by_one(hexipher_text)
# print(list_of_ranked_size)
# for i in range(0, 1):
# 	list_block = get_list_of_key_block(list_of_ranked_size[i][0], cipher_text)
# # print(cipher_text)
# 	print("\n")
# 	brutalize_all_lists(list_block)
# print(list_block)



# lili = {}
# for i in range(0,256):
# 	lili[i] = 0
# toto = base64.b64decode(cipher_text)
# for i in toto:
# 	lili[i] += 1
# lili2 = sorted(lili.items(), key = lambda kv:(kv[1], kv[0]))
# # print(lili2)
# lili[28] = 'e'
# lili[22] = 't'
# lili[0] = 'a'
# lili[83] = 'o'
# lili[16] = 'i'
# lili[7] = 'n'
# lili[26] = ' '
# lili[23] = 's'
# lili[69] = 'h'
# lili[6] = 'r'
# lili[1] = 'd'
# lili[10] = 'l'
# lili[3] = 'u'

# lili = list(toto)

# i = -1
# for char in lili:
# 	i +=1
# 	if char == '\x28':
# 		lili[i] = '\x45'
# 	elif char == '\x22':
# 		lili[i] = '\x54'
# 	elif char == '\x00':
# 		lili[i] = '\x41'
# 	elif char == '\x83':
# 		lili[i] = '\x4f'	
# 	elif char == '\x16':
# 		lili[i] = '\x49'
# 	elif char == '\x07':
# 		lili[i] = '\x4e'
# 	elif char == '\x26':
# 		lili[i] = '\x20'
# 	elif char == '\x23':
# 		lili[i] = '\x53'
# 	elif char == '\x69':
# 		lili[i] = '\x48'
# 	elif char == '\x06':
# 		lili[i] = '\x52'
# 	elif char == '\x01':
# 		lili[i] = '\x44'
# 	elif char == '\x10':
# 		lili[i] = '\x4c'
# 	else:
# 		lili[i] = lili[i]

# print(str(bytes(lili)))