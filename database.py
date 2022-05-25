import re
import io
import chess.pgn

c = 0
with open(r'C:\Users\HP\Documents\repos\CC\ficsgamesdb_search_238513.pgn', 'r') as file:
    for line in file:
        if re.search('checkmated', line) is not None:
            pgn = io.StringIO(line)
            game = chess.pgn.read_game(pgn)
            fin = game.end()
            print(fin.board())
            c += 1

print(c)