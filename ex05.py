import sys
import base64
import codecs
import binascii

KEYSIZE_MIN = 2
KEYSIZE_MAX = 40
KEYSIZE = 2
PROBA_LETTER = 70

def encode_hex(s):
	return codecs.encode(s, "hex_codec")
def decoderin(s):
	decode_hex = codecs.getdecoder("hex_codec")
	return decode_hex(s)[0]
letters = list(range(97, 122)) + [32]

def single_xoring(s1, c):
	print(s1)
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
 


# gros probleme sur le brute/eval le xor n'as pas l'air de se faire 


# get bests results for analyse of bruteforced single XOR
def brute_forced(cipher_string):
	list_of_possible_breaking_cipher = []
	for i in range(0, 255):
		i_b = i.to_bytes(1, byteorder='big')
		result = single_xoring(decoderin(cipher_string), i_b)
	if evaluate(result) > PROBA_LETTER:
		list_of_possible_breaking_cipher.insert(result)
	return list_of_possible_breaking_cipher

# loop on all chain
def brutalize_all_lists(list_block):
	for one_str in list_block:
		str_encode = binascii.hexlify(codecs.encode(one_str)).decode('ascii')
		# print(codecs.encode(str_encode))
		# print(str_encode)
		print(brute_forced(str_encode))
		return


# a checker dans ce bout de code


# print(hamming('this is a test', 'wokka wokka!!!'))
# print(str(get_file(), 'utf-8'))

# s = 'Hello world'
# l = list(s)
# l[6] = 'W'
# s = "".join(l) # s = 'Hello World'

cipher_text = get_file()
list_size_key = battery_hamming(cipher_text)
list_of_ranked_size = sorted(list_size_key.items(), key = lambda kv:(kv[1], kv[0]))
# print(list_of_ranked_size)
list_block = get_list_of_key_block(list_of_ranked_size[0][0], cipher_text)
# print(cipher_text)
brutalize_all_lists(list_block)
# print(list_block)