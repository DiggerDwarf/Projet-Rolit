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

def save(fileName: str, grid: list[list[int]], start_bias: int, nb_players: int, nb_AIs: int, nb_rounds: int, curr_round: int) -> None:
    data = pack_grid(grid)
    byte  = (start_bias << 6) & 0b11000000
    byte |= ((nb_players-1) << 4) & 0b110000
    byte |= (nb_AIs << 2) & 0b1100
    byte |= (nb_rounds-1) & 0b11
    data.append(byte)
    byte  = (curr_round << 6) & 0b11000000
    data.append(byte)
    with open(fileName, "wb") as saveFile:
        saveFile.write(data)

def recall(fileName: str) -> tuple[list[list[int]], int, int, int, int, int, int]:
    with open(fileName, "rb") as saveFile:
        grid = unpack_grid(saveFile.read(32))
        byte1 = saveFile.read(1)[0]
        byte2 = saveFile.read(1)[0]
    start_bias =  (byte1 >> 6) & 0b11
    turn = 60 - sum([grid[i].count(0) for i in range(8)])
    nb_players =  ((byte1 >> 4) & 0b11) + 1
    nb_AIs =      (byte1 >> 2) & 0b11
    nb_rounds =   ((byte1) & 0b11) + 1
    curr_round =  (byte2 >> 6) & 0b11
    return grid, start_bias, turn, nb_players, nb_AIs, nb_rounds, curr_round
