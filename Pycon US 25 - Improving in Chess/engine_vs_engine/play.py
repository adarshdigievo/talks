import asyncio
import chess
import time
import chess.engine
from chessboard import display


async def main() -> None:
    _, stockfish_engine = await chess.engine.popen_uci(
        r"C:\Users\adars\projects\chess\engines\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
    )

    _, komodo_engine = await chess.engine.popen_uci(
        r"C:\Users\adars\projects\chess\engines\komodo-14\Windows\komodo-14.1-64bit.exe"
    )

    _, lc0_engine = await chess.engine.popen_uci(
        r"C:\Users\adars\projects\chess\engines\lc0-v0.29.0-windows-gpu-nvidia-cudnn\lc0.exe"
    )

    board = chess.Board()
    game_board = display.start()

    is_white = True

    while not board.is_game_over():
        if is_white:
            result = await stockfish_engine.play(board, chess.engine.Limit(time=1))
        else:
            result = await lc0_engine.play(board, chess.engine.Limit(time=1))

        is_white = not is_white
        board.push(result.move)
        display.update(board.fen(), game_board=game_board)

        if board.can_claim_threefold_repetition():
            time.sleep(3)
            print("draw by repetition")
            break
        if board.can_claim_fifty_moves():
            time.sleep(3)
            print("draw by fifty move rule")
            break
        if board.is_insufficient_material():
            time.sleep(3)
            print("draw by insufficient material")
            break

    await komodo_engine.quit()
    await lc0_engine.quit()
    await stockfish_engine.quit()
    time.sleep(10)
    display.terminate()


asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())
