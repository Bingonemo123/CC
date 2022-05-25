import chess
import numpy as np
import os
import time
import chess.engine
import datetime
enginepath = r"C:\Users\HP\Downloads\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe"

def inputmanager(board=None):
    ptext = ""
    if "MyColor" not in inputset:
        ptext = 'Your color:'
        l = input(ptext)
        if l in ['w', 'W', 'White', 'white']:
            inputset["MyColor"] = chess.WHITE
 
        if l in ['b', 'B', 'Black', 'black']:
            inputset["MyColor"] = chess.BLACK


    elif inputset['MyColor'] != board.turn:
        ptext = "Oponent's move:"
        l = input(ptext)
        if l in [ 'exit', 'E', 'e' ]:
            return 'Exit'
        elif l in ['pop', 'return', 'back']:
            return 'pop'
        elif 'ud' in l.split(' '):
            return 'ud', l.split(' ')
        try:
            move = board.push_uci(l)
            return move
        except ValueError as e:
            print(e)
        try:
            move = board.push_san(l)
            return move
        except ValueError as e:
            print(e)
        try:
            move = board.push_xboard(l)
            return move
        except ValueError as e:
            print(e)
            return False

def Movemaker(l, board):
    try:
        move = board.push_uci(l)
        return move
    except ValueError as e:
        print(e)
    try:
        move = board.push_san(l)
        return move
    except ValueError as e:
        print(e)
    try:
        move = board.push_xboard(l)
        return move
    except ValueError as e:
        print(e)
        return False

def rot(b):
    return [63 - sq for sq in list(b)]


engine = chess.engine.SimpleEngine.popen_uci(enginepath)
engine.configure({"UCI_Elo": 1800})

while True:
    board = chess.Board()
    timecontrol = 10 * 60
    mytime, optime = timecontrol - 60, timecontrol 
    optimest = time.time()
    inputset = {}

    cpoi = 0


    inputmanager()

    if inputset['MyColor'] == chess.BLACK:
        print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
    else:
        print(board.unicode())

    input()

    while len(list(board.legal_moves)) != 0: 
        if inputset['MyColor'] == board.turn:
            rlm = list(board.legal_moves)
            np.random.shuffle(rlm)
            movelib = []
            if board.fullmove_number <= 5:
                timlim = 0.1
            elif board.fullmove_number > 5 and board.fullmove_number < 12:
                timlim = 0.2
            elif board.fullmove_number > 5 and board.fullmove_number < 25:
                timlim = 0.3
            else:
                timlim = 0.2

            print('timlim', timlim)
            for lm in rlm:
                mytimest = time.time()
                board.push(lm)
                

                if inputset['MyColor'] == chess.BLACK:
                    limit = chess.engine.Limit(time=timlim)
                else:
                    limit = chess.engine.Limit(time=timlim)
                info = engine.analyse(board, limit)

                if info['score'].relative > chess.engine.Cp(cpoi -50) and info['score'].relative < chess.engine.Cp(cpoi + 50):
                    if np.random.choice([True, False]):
                        os.system('cls')
                        print(chess.piece_name(board.piece_at(lm.to_square).piece_type), lm, info['score'])
                        if inputset['MyColor'] == chess.BLACK:
                            print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
                        else:
                            print(board.unicode())


                        movearr = chess.SquareSet.between(lm.from_square, lm.to_square)
                        movearr.add(lm.from_square)
                        movearr.add(lm.to_square)

                        if inputset['MyColor'] == chess.BLACK:

                            print(chess.SquareSet(rot(movearr)))
                        else:
                            print(movearr)

                        if cpoi > info['score'].relative.score() : cpoi = info['score'].relative.score()
                        print(f'cpoi {cpoi}')
                        break
                
                if info['score'].relative < chess.engine.Cp(-800):
                    if np.random.choice([True, False]):
                        os.system('cls')
                        print(chess.piece_name(board.piece_at(lm.to_square).piece_type), lm, info['score'])
                        if inputset['MyColor'] == chess.BLACK:
                            print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
                        else:
                            print(board.unicode())

                        movearr = chess.SquareSet.between(lm.from_square, lm.to_square)
                        movearr.add(lm.from_square)
                        movearr.add(lm.to_square)

                        if inputset['MyColor'] == chess.BLACK:

                            print(chess.SquareSet(rot(movearr)))
                        else:
                            print(movearr)


                        cpoi = info['score'].relative.score()
                        break


                print(datetime.timedelta(seconds=mytime), lm , info["score"])
                board.pop()
                movelib.append(info["score"])
                mytime -= time.time() - mytimest
                if mytime < 0:
                    mytime = 0
               

            else:
                
                if cpoi >= 300:
                    winmoves = []
                    for scr in enumerate(movelib):
                        if scr[1].relative > cpoi:
                            winmoves.append(rlm[minmax[0]])

                    mv = np.random.choice(winmoves)

                    board.push(mv)

                    os.system('cls')
                    print(chess.piece_name(board.piece_at(mv.to_square).piece_type), mv, info['score'])
                    if inputset['MyColor'] == chess.BLACK:
                        print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
                    else:
                        print(board.unicode())

                    movearr = chess.SquareSet.between(mv.from_square, mv.to_square)
                    movearr.add(mv.from_square)
                    movearr.add(mv.to_square)

                    if inputset['MyColor'] == chess.BLACK:

                        print(chess.SquareSet(rot(movearr)))
                    else:
                        print(movearr)


                    cpoi = info['score'].relative.score()


                else:
                    maxmin = None
                    minmax = None
                    for scr in enumerate(movelib):

                        if maxmin is None and scr[1].relative > chess.engine.Cp(0):
                            maxmin = scr
                        
                        if minmax is None and scr[1].relative <= chess.engine.Cp(0):
                            minmax = scr
                        
                        if maxmin is not None:
                            if scr[1].relative > chess.engine.Cp(0) and scr[1].relative < maxmin[1].relative:
                                maxmin = scr

                        if minmax is not None:
                            if scr[1].relative < chess.engine.Cp(0) and scr[1].relative > minmax[1].relative:
                                minmax = scr
                    

                    if minmax is not None:
                        board.push(rlm[minmax[0]])
                        os.system('cls')
                        print(chess.piece_name(board.piece_at(rlm[minmax[0]].to_square).piece_type), rlm[minmax[0]], minmax[1], 'minmax')
                        if inputset['MyColor'] == chess.BLACK:
                            print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
                        else:
                            print(board.unicode())

                        movearr = chess.SquareSet.between(rlm[minmax[0]].from_square, rlm[minmax[0]].to_square)
                        movearr.add(rlm[minmax[0]].from_square)
                        movearr.add( rlm[minmax[0]].to_square)

                        if inputset['MyColor'] == chess.BLACK:

                            print(chess.SquareSet(rot(movearr)))
                        else:
                            print(movearr)

                        cpoi = minmax[1].relative.score()
                    else:
                        board.push(rlm[maxmin[0]])
                        os.system('cls')
                        print(chess.piece_name(board.piece_at(rlm[maxmin[0]].to_square).piece_type), rlm[maxmin[0]], maxmin[1], 'maxmin')
                        if inputset['MyColor'] == chess.BLACK:
                            print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
                        else:
                            print(board.unicode())

                        movearr = chess.SquareSet.between(rlm[maxmin[0]].from_square, rlm[maxmin[0]].to_square)
                        movearr.add(rlm[maxmin[0]].from_square)
                        movearr.add( rlm[maxmin[0]].to_square)

                        if inputset['MyColor'] == chess.BLACK:

                            print(chess.SquareSet(rot(movearr)))
                        else:
                            print(movearr)

                        cpoi = maxmin[1].relative.score()
            
            mytime -= 30
            optimest = time.time()

        else:
            mov = inputmanager(board=board)
            print(mov)
            if mov == 'Exit':
                break
            elif mov == 'pop':
                board.pop()
            elif isinstance(mov, tuple):
                board.pop()
                mov = Movemaker(mov[1][1], board)
                os.system('cls')
                print(mov)
                if inputset['MyColor'] == chess.BLACK:
                    print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
                else:
                    print(board.unicode())
            elif mov:
                os.system('cls')
                print(mov)
                if inputset['MyColor'] == chess.BLACK:
                    print(board.transform(chess.flip_vertical).transform(chess.flip_horizontal).unicode())
                else:
                    print(board.unicode())
            optime -= time.time() - optimest


                


engine.quit()

