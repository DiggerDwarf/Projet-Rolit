"""Functions for saving and recalling game state"""

def pack_grid(grid: list[list[int]]) -> bytearray:
    out = bytearray()
    for i in range(8):
        for j in range(4):
            out.append( (grid[i][2*j] << 4) | (grid[i][2*j + 1]) )
    return out

def unpack_grid(packed: bytearray) -> list[list[int]]:
    out = [[None for _ in range(8)] for _ in range(8)]
    for i in range(len(packed)):
        out[i//4][2*(i%4)] = packed[i] >> 4 & 0b1111
        out[i//4][2*(i%4) + 1] = packed[i]  & 0b1111
    return out

