from math import prod

lookup = {h: bin(int(h, 16))[2:].zfill(4) for h in "0123456789ABCDEF"}

with open("input.txt", "r") as f:
    bits = "".join(map(lambda h: lookup[h], f.readlines()[0]))

def parse(bits):
    def get_bits(bits, length):
        return (bits[length:], bits[0:length])
    def get_bits_decimal(bits, length):
        bits, data = get_bits(bits, length)
        return (bits, int(data, 2))
    def parse_header(bits):
        bits, version = get_bits_decimal(bits, 3)
        bits, type_id = get_bits_decimal(bits, 3)
        return (bits, {"version": version, "type_id": type_id, "packets": []})
    def get_value(bits):
        num = ""
        bits, data = get_bits(bits, 5)
        data, lead = get_bits(data, 1)
        num += data
        while lead == "1":
            bits, data = get_bits(bits, 5)
            data, lead = get_bits(data, 1)
            num += data
        return (bits, int(num, 2))
    def get_subpackets_bitstring(bits):
        bits, length_bits = get_bits(bits, 15)
        length_bits = int(length_bits, 2)
        bits, subpacket_bits = get_bits(bits, length_bits)
        packets = []
        while subpacket_bits:
            subpacket_bits, subpacket = parse(subpacket_bits)
            packets.append(subpacket)
        return (bits, packets)
    def get_subpackets_num(bits):
        bits, num_packets = get_bits(bits, 11)
        num_packets = int(num_packets, 2)
        packets = []
        while num_packets:
            bits, subpacket = parse(bits)
            packets.append(subpacket)
            num_packets -= 1
        return (bits, packets)

    bits, p = parse_header(bits)
    if p["type_id"] == 4:
        bits, value = get_value(bits)
        p["value"] = value
    else:
        bits, length_type = get_bits(bits, 1)
        if length_type == "0":
            bits, p["packets"] = get_subpackets_bitstring(bits)
        else:
            bits, p["packets"] = get_subpackets_num(bits)
    return (bits, p)

def sum_version(packet):
    if packet["type_id"] == 4: return packet["version"]
    return packet["version"] + sum(map(sum_version, packet["packets"]))

def process_packets(packet):
    t_id = packet["type_id"]
    if t_id == 4: return packet["value"]
    values = map(process_packets, packet["packets"])
    if t_id == 0: return sum(values)
    if t_id == 1: return prod(values)
    if t_id == 2: return min(values)
    if t_id == 3: return max(values)
    a, b = values
    if t_id == 5: return int(a > b)
    if t_id == 6: return int(a < b)
    if t_id == 7: return int(a == b)

_, packets = parse(bits)
print(f"Solution 1: {sum_version(packets)}")
print(f"Solution 2: {process_packets(packets)}")