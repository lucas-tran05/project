import os
import json
import heapq

# === Node class ===
class Node:
    def __init__(self, frequency, symbol, left=None, right=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huffman_direction = ''

    def __lt__(self, nxt):
        return self.frequency < nxt.frequency

# === IO Utilities ===
def read_image_bit_string(path):
    with open(path, 'rb') as image:
        bit_string = ''
        byte = image.read(1)
        while byte:
            bits = bin(ord(byte))[2:].rjust(8, '0')
            bit_string += bits
            byte = image.read(1)
    return bit_string

def write_image(bit_string, path):
    with open(path, 'wb') as image:
        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i+8]
            if len(byte) < 8:
                byte = byte.ljust(8, '0')  # zero padding
            image.write(bytes([int(byte, 2)]))

# === Huffman Core ===
def get_frequency(image_bit_string):
    freq = {}
    for i in range(0, len(image_bit_string), 8):
        byte = image_bit_string[i:i+8]
        freq[byte] = freq.get(byte, 0) + 1
    return freq

def build_huffman_tree(freq_table):
    heap = [Node(freq, byte) for byte, freq in freq_table.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        left.huffman_direction = '0'
        right.huffman_direction = '1'
        merged = Node(left.frequency + right.frequency, left.symbol + right.symbol, left, right)
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, prefix='', code_map=None):
    if code_map is None:
        code_map = {}
    if node.left is None and node.right is None:
        code_map[node.symbol] = prefix
    if node.left:
        generate_codes(node.left, prefix + '0', code_map)
    if node.right:
        generate_codes(node.right, prefix + '1', code_map)
    return code_map

def compress_bits(image_bit_string, code_map):
    return ''.join(code_map[image_bit_string[i:i+8]] for i in range(0, len(image_bit_string), 8))

def decompress_bits(bit_string, code_map):
    reverse_map = {v: k for k, v in code_map.items()}
    result = ''
    current = ''
    for bit in bit_string:
        current += bit
        if current in reverse_map:
            result += reverse_map[current]
            current = ''
    return result

# === Encode Function ===
def encode(image_path):
    original_bits = read_image_bit_string(image_path)
    freq_table = get_frequency(original_bits)
    tree = build_huffman_tree(freq_table)
    codes = generate_codes(tree)
    compressed_bits = compress_bits(original_bits, codes)

    # Paths
    base_path = os.path.splitext(image_path)[0]
    huff_path = base_path + '.huff'
    map_path = base_path + '.map'

    # Save compressed file
    write_image(compressed_bits, huff_path)

    # Save code map as JSON
    with open(map_path, 'w') as f:
        json.dump(codes, f)

    stats = {
        "Kích thước gốc (bit)": len(original_bits),
        "Kích thước nén (bit)": len(compressed_bits),
        "Tỉ lệ nén": f"{len(original_bits) / len(compressed_bits):.2f}"
    }

    return compressed_bits, codes, stats

# === Decode Function ===
def decode(huff_path):
    compressed_bits = read_image_bit_string(huff_path)

    # Load code map
    map_path = os.path.splitext(huff_path)[0] + '.map'
    with open(map_path, 'r') as f:
        codes = json.load(f)

    decoded_bits = decompress_bits(compressed_bits, codes)

    # Save output file
    out_path = os.path.splitext(huff_path)[0] + '_decompressed.jpg'
    write_image(decoded_bits, out_path)

    return out_path
