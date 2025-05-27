# Project: A data encryption and decryption application using the Huffman algorithm with a graphical user interface.
# To fulfil the requirement of FIT Course by Pham@PTIT
# Tran Quoc Cuong - B23DCAT034 - 13
# Duong Thien Ngan - B23DCAT209 - 13
# Le Van Duy - B23DCAT074 - 13

from collections import Counter
import heapq

class Node:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    freq = Counter(data)
    heap = [Node(freq=freq[byte], byte=bytes([byte])) for byte in freq]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(n1.freq + n2.freq, left=n1, right=n2)
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def build_code_table(node, prefix="", code_table=None):
    if code_table is None:
        code_table = {}
    if node:
        if node.byte is not None:
            code_table[node.byte] = prefix
        build_code_table(node.left, prefix + "0", code_table)
        build_code_table(node.right, prefix + "1", code_table)
    return code_table

def encode_data(data, code_table):
    return ''.join(code_table[bytes([b])] for b in data)

def pad_encoded_data(encoded_data):
    extra_padding = 8 - len(encoded_data) % 8
    encoded_data += "0" * extra_padding
    padded_info = f"{extra_padding:08b}"
    encoded_data = padded_info + encoded_data
    return bytes(int(encoded_data[i:i+8], 2) for i in range(0, len(encoded_data), 8))

def decode_data(encoded_data, tree):
    current = tree
    decoded_bytes = bytearray()

    for bit in encoded_data:
        current = current.left if bit == '0' else current.right
        if current.left is None and current.right is None:
            decoded_bytes.extend(current.byte)
            current = tree
    return decoded_bytes