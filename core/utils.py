NESW = 'nesw' # Clockwise head order

def sort_heads(heads) -> list:
    return sorted(heads, key=lambda x: NESW.index(x))


def rotate_heads(heads, turns) -> list:
    bits = get_head_bits(heads)
    # For each turn, move the last item in the list to the front
    for _ in range(turns):
        bits.insert(0, bits.pop())
    return [NESW[x] for x, bit in enumerate(bits) if bit]


def get_head_bits(heads):
    # Create a list of bool flags representing whether a head is present on each side
    return [x in sort_heads(heads) for x in NESW]
