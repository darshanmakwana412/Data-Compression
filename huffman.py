from heapq import *
from collections import Counter

forward = {}
reverse = {}

class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None
    
	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


class metadata:
    def __init__(self, codex, encoded_text, buffer):
        self.codex = codex
        self.encoded_text = encoded_text
        self.buffer = buffer

def get_heap(text):
    ordered_list = Counter(text)
    h = []
    for i in ordered_list:
        node = HeapNode(i, ordered_list[i])
        heappush(h,node)
    return h

def generate_tree(h):
    while(len(h)>1):
        node1 = heappop(h)
        node2 = heappop(h)
        new_node = HeapNode(None, node1.freq + node2.freq)
        new_node.left = node1
        new_node.right = node2
        heappush(h,new_node)
    return heappop(h)
        
def generate_code(node,current):
    global forward,reverse
    if(node == None):
        return 

    if(node.char != None):
        forward[node.char] = current
        reverse[current] = node.char
        return

    generate_code(node.left, current + '0')
    generate_code(node.right, current + '1')


def encode(text,codex):
    encoded_text = ""
    for c in text:
        encoded_text += codex[c]
    buffer = 8 - len(encoded_text)%8
    encoded_text += '0'*buffer
    return bitstring_to_bytes(encoded_text),buffer

def bitstring_to_bytes(s):
    b = bytearray()
    for i in range(0, len(s), 8):
        byte = s[i:i+8]
        b.append(int(byte, 2))
    return bytes(b)

def bytes_to_bitstring(encoded_text,buffer):
    decoded_data = ""
    for i in encoded_text:
        decoded_data += "{0:08b}".format(ord(chr(i)))
    return decoded_data[:len(decoded_data)-buffer]

def decode(reverse, encoded_text, buffer):
    decoded_data = bytes_to_bitstring(encoded_text, buffer)
    text = ""
    current = ""
    for bit in decoded_data:
        current += bit
        try:
            character = reverse[current]
            text += character
            current = ""
        except:
            pass
    return text