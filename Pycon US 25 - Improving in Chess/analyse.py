import asyncio
import chess
import chess.pgn
import chess.engine
from chessboard import display
import io
import tkinter as tk
import pygame
import math

# Initialize pygame and font system
pygame.init()
pygame.font.init()

# Constants for move evaluation
EVAL_RANGES = {
    "brilliant": (800, float("inf")),  # Gaining over +8 advantage
    "excellent": (500, 800),  # Gaining +5 to +8 advantage
    "great": (300, 500),  # Gaining +3 to +5 advantage
    "good": (50, 300),  # Gaining +0.5 to +3 advantage
    "neutral": (-50, 50),  # Between -0.5 and +0.5 (minimal change)
    "inaccuracy": (-150, -50),  # Losing -0.5 to -3 advantage
    "mistake": (-300, -150),  # Losing -3 to -8 advantage
    "blunder": (float("-inf"), -300),  # Losing more than -8 advantage
}


class GameAnalyzer:
    # Colors for the quality indicators
    QUALITY_COLORS = {
        "brilliant": (52, 152, 219),  # Blue
        "great": (46, 204, 113),  # Green
        "good": (39, 174, 96),  # Dark Green
        "neutral": (149, 165, 166),  # Gray
        "inaccuracy": (243, 156, 18),  # Orange
        "mistake": (230, 126, 34),  # Dark Orange
        "blunder": (231, 76, 60),  # Red
    }

    def __init__(self, engine_path):
        self.engine_path = engine_path
        self.engine = None
        self.board = chess.Board()
        self.game_board = None
        self.game = None
        self.moves = []
        self.current_move_idx = -1
        self.previous_eval = 0
        self.move_evals = []
        self.analysis_info = None
        self.root = None
        self.analysis_label = None
        self.move_label = None
        self.best_move = None
        self.best_move_arrow = None

    async def initialize(self):
        """Initialize engine and UI components"""
        self.transport, self.engine = await chess.engine.popen_uci(self.engine_path)

        self.game_board = display.start(caption="Chess Analysis with Python")

        # Create control panel for navigation
        self.root = tk.Tk()
        self.root.title("Chess Game Analysis")
        self.root.geometry("600x200")

        # Text area for PGN input (at the top)
        pgn_frame = tk.Frame(self.root)
        pgn_frame.pack(pady=1, fill=tk.BOTH, expand=True)

        pgn_label = tk.Label(pgn_frame, text="Paste PGN here:")
        pgn_label.pack(anchor=tk.W)

        self.pgn_text = tk.Text(pgn_frame, height=3, width=60)
        self.pgn_text.pack(fill=tk.BOTH, expand=True)

        # Initialize the analysis UI below PGN
        self.analysis_frame = tk.Frame(self.root)
        self.analysis_frame.pack(pady=5, fill="x")

        self.analysis_label = tk.Label(
            self.analysis_frame,
            text="Analysis will appear here",
            font=("Helvetica", 12),
        )
        self.analysis_label.pack()

        # Navigation buttons below analysis
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        load_button = tk.Button(button_frame, text="Load PGN", command=self.load_pgn)
        load_button.grid(row=0, column=0, padx=5)

        prev_button = tk.Button(
            button_frame, text="< Previous", command=self.previous_move
        )
        prev_button.grid(row=0, column=1, padx=5)

        next_button = tk.Button(button_frame, text="Next >", command=self.next_move)
        next_button.grid(row=0, column=2, padx=5)

        suggest_move_button = tk.Button(
            button_frame, text="Suggest Best Move", command=self.show_best_move
        )
        suggest_move_button.grid(row=0, column=3, padx=5)

        # Move info and analysis frame (below the buttons)
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=5, fill="x")

        # Current move notation label
        self.move_label = tk.Label(
            self.info_frame, text="Move: Starting Position", font=("Helvetica", 12)
        )
        self.move_label.pack(anchor=tk.W, pady=(5, 2))

        # Quality analysis label below move notation
        self.quality_label = tk.Label(
            self.info_frame,
            text="Move quality will appear here",
            font=("Helvetica", 10),
        )
        self.quality_label.pack(anchor=tk.W)

        # Start updating the UI
        self.update_ui()

    def load_pgn(self):
        """Load a PGN from the text area"""
        pgn_text = self.pgn_text.get("1.0", tk.END).strip()
        if not pgn_text:
            self.analysis_label.config(text="Error: No PGN data provided", fg="red")
            return

        try:
            pgn_io = io.StringIO(pgn_text)
            self.game = chess.pgn.read_game(pgn_io)
            if self.game:
                self.process_game()
                self.reset_to_start()
            else:
                self.analysis_label.config(text="Error: Invalid PGN format", fg="red")
        except Exception as e:
            self.analysis_label.config(text=f"Error: {str(e)}", fg="red")

    def process_game(self):
        """Process the loaded game and prepare move list"""
        self.moves = []
        self.move_evals = []
        self.board = self.game.board()

        # Extract all moves from the game
        for move in self.game.mainline_moves():
            self.moves.append(move)

        # Reset position
        self.current_move_idx = -1
        self.board = self.game.board()

        # Reset display
        display.update(self.board.fen(), game_board=self.game_board)
        self.move_label.config(text=f"Move: Starting Position")
        self.analysis_label.config(text="")

    def reset_to_start(self):
        """Reset to starting position"""
        self.current_move_idx = -1
        self.board = self.game.board()
        display.update(self.board.fen(), game_board=self.game_board)
        self.move_label.config(text=f"Move: Starting Position")
        self.analysis_label.config(text="")

    def previous_move(self):
        """Go to previous move"""
        if self.current_move_idx > -1:
            self.current_move_idx -= 1
            self.update_position()  # Call the main update method
        elif self.current_move_idx == -1:
            # If already at the start, re-update to ensure clean state
            self.update_position()

    def next_move(self):
        """Go to next move"""
        if self.game and self.current_move_idx < len(self.moves) - 1:
            self.current_move_idx += 1
            self.update_position()  # Call the main update method

    def update_position(self):
        """Update the board position based on current_move_idx"""
        try:
            # Reset board to initial position
            self.board = self.game.board()

            last_move = None
            # Replay moves up to current_move_idx
            for i in range(self.current_move_idx + 1):
                move = self.moves[i]
                self.board.push(move)
                last_move = move

            # Update display
            display.update(self.board.fen(), game_board=self.game_board)

            # Update move info
            if self.current_move_idx == -1:
                self.move_label.config(text="Move: Starting Position")
                self.analysis_label.config(text="")
                self.quality_label.config(text="Move quality will appear here")
            else:
                # Update move notation label
                move_number = (self.current_move_idx // 2) + 1
                side = "White" if self.current_move_idx % 2 == 0 else "Black"
                move = self.moves[self.current_move_idx]

                # Try to get SAN for the move. The board (self.board) should be in the correct state here.
                try:
                    current_move_san = self.board.san(move)
                except (
                        chess.IllegalMoveError
                ):  # Should not happen if moves are from a valid game
                    current_move_san = move.uci()  # Fallback to UCI
                except Exception:  # General fallback
                    current_move_san = move.uci()

                self.move_label.config(
                    text=f"Move {move_number}: {side} plays {current_move_san}"
                )

                # Draw arrow for the last move (which is the current move in this context)
                if last_move:
                    self.draw_move_arrow(last_move)

                # If we have real analysis, use it
                if (
                        self.current_move_idx < len(self.move_evals)
                        and self.move_evals[self.current_move_idx] is not None
                ):
                    eval_type, eval_score = self.move_evals[self.current_move_idx]
                    self.update_analysis_ui(eval_type, eval_score)
                    # draw_quality_indicator is called within update_analysis_ui
                else:
                    # If no analysis yet for this move, reset quality label and clear indicator implicitly by board redraw
                    self.quality_label.config(
                        text="Move quality will appear here", fg="black"
                    )
                    # The display.update earlier in this function should clear old pygame drawings on the board
                    # If specific clearing of only the dot is needed, that's more complex. Assuming full board update is enough.

        except Exception as e:
            print(f"Error updating position: {e}")

        # Clear best move arrow if any
        if hasattr(self, "best_move"):
            self.best_move = None
        self.best_move_arrow = None

        # Analyze the current position
        asyncio.create_task(self.analyze_current_position())

    def draw_move_arrow(self, move):
        """Draw an arrow on the board to indicate the last move"""
        from_square = chess.parse_square(move.uci()[0:2])
        to_square = chess.parse_square(move.uci()[2:4])

        from_coords = self.square_to_coordinates(from_square)
        to_coords = self.square_to_coordinates(to_square)

        # Calculate center points of squares
        from_center = (
            from_coords[0] + 25,
            from_coords[1] + 25,
        )  # 25 is half the square size
        to_center = (to_coords[0] + 25, to_coords[1] + 25)

        # Arrow color
        color = (0, 0, 255, 150)  # Semi-transparent blue

        # Draw arrow line
        pygame.draw.line(self.game_board.display_surf, color, from_center, to_center, 3)

        # Draw arrowhead
        arrow_length = 15
        dx = to_center[0] - from_center[0]
        dy = to_center[1] - from_center[1]
        angle = math.atan2(dy, dx)

        # Calculate arrowhead points
        point1 = (
            to_center[0] - arrow_length * math.cos(angle - math.pi / 6),
            to_center[1] - arrow_length * math.sin(angle - math.pi / 6),
        )
        point2 = (
            to_center[0] - arrow_length * math.cos(angle + math.pi / 6),
            to_center[1] - arrow_length * math.sin(angle + math.pi / 6),
        )

        # Draw arrowhead
        pygame.draw.polygon(
            self.game_board.display_surf, color, [to_center, point1, point2]
        )

        # Update display
        pygame.display.update()

        return None  # For compatibility with the suggest_best_move method

    def draw_quality_indicator(self, square, quality):
        """Draw a colored dot on the piece to indicate move quality"""
        if quality not in self.QUALITY_COLORS:
            quality = "neutral"

        color = self.QUALITY_COLORS[quality]
        coords = self.square_to_coordinates(square)

        # Draw a circle at the top-right corner of the square
        center = (coords[0] + 40, coords[1] + 10)  # Top-right corner
        radius = 8

        # Draw circle with border
        pygame.draw.circle(
            self.game_board.display_surf, (0, 0, 0), center, radius + 1
        )  # Black border
        pygame.draw.circle(
            self.game_board.display_surf, color, center, radius
        )  # Colored center

        # Update display
        pygame.display.update()

    def square_to_coordinates(self, square):
        """Convert a chess square (0-63) to board coordinates"""
        file_idx = chess.square_file(square)  # 0-7 for a-h
        rank_idx = 7 - chess.square_rank(square)  # 0-7 for 8-1 (note the inversion)

        # Get the coordinates from the board_rect
        coords = self.game_board.board_rect[rank_idx][file_idx]
        return coords

    def update_analysis_ui(self, eval_type, eval_score):
        """Update the analysis display in the UI"""
        # Set color based on eval type
        color_map = {
            "brilliant": "#3498db",  # Blue
            "great": "#2ecc71",  # Green
            "good": "#27ae60",  # Dark Green
            "neutral": "black",  # Black
            "inaccuracy": "#f39c12",  # Orange
            "mistake": "#e67e22",  # Dark Orange
            "blunder": "#e74c3c",  # Red
        }

        color = color_map.get(eval_type, "black")

        # Format the evaluation score
        if abs(eval_score) > 1000:  # Probably a mate score
            if eval_score > 0:
                eval_text = f"M{(10000 - eval_score) // 10}"
            else:
                eval_text = f"-M{(10000 + eval_score) // 10}"
        else:
            eval_text = f"{eval_score / 100:.2f}"

        # Update analysis label
        self.analysis_label.config(
            text=f"{eval_type.capitalize()} ({eval_text})", fg=color
        )

        # Update quality label as well
        self.quality_label.config(
            text=f"Move Quality: {eval_type.capitalize()} (Evaluation: {eval_text})",
            fg=color,
        )

        # Draw quality indicator on the piece
        if self.current_move_idx >= 0 and self.current_move_idx < len(self.moves):
            move = self.moves[self.current_move_idx]
            to_square = chess.parse_square(move.uci()[2:4])
            self.draw_quality_indicator(to_square, eval_type)

    def show_best_move(self):
        """Wrapper to properly schedule the async suggest_best_move coroutine"""
        asyncio.create_task(self.suggest_best_move())

    def update_ui(self):
        """Update the UI periodically"""
        if self.root:
            self.root.update()

    async def suggest_best_move(self):
        """Get the best move from the engine and display it on the board"""
        try:
            # Clear any previous best move arrow
            if self.best_move_arrow is not None:
                # We should redraw the board to clear the arrow
                display.update(self.board.fen(), game_board=self.game_board)

                # Redraw the current move arrow if needed
                if self.current_move_idx >= 0:
                    last_move = self.moves[self.current_move_idx]
                    self.draw_move_arrow(last_move)

                    # If we have an evaluation for this move, show the quality indicator
                    if (
                            self.current_move_idx < len(self.move_evals)
                            and self.move_evals[self.current_move_idx] is not None
                    ):
                        eval_type, eval_score = self.move_evals[self.current_move_idx]
                        destination_square = chess.parse_square(last_move.uci()[2:4])

                        # Draw quality indicator with the stored evaluation type
                        self.draw_quality_indicator(destination_square, eval_type)

                self.best_move_arrow = None

            # Get the best move from the engine
            result = await self.engine.play(self.board, chess.engine.Limit(time=1.0))
            self.best_move = result.move

            if self.best_move:
                # Draw the best move arrow
                self.best_move_arrow = self.draw_move_arrow(self.best_move)

                # Update the UI to show the best move
                best_move_san = self.board.san(self.best_move)
                current_analysis_text = self.analysis_label.cget("text")
                # Avoid duplicating "Best move:" prefix
                if "Best move:" not in current_analysis_text:
                    self.analysis_label.config(
                        text=f"Best move: {best_move_san} ({current_analysis_text})",
                        fg="green",
                    )
                else:
                    # If "Best move:" is already there, just update the move part
                    # This is a simple replacement, could be made more robust
                    self.analysis_label.config(
                        text=f"Best move: {best_move_san}",
                        fg="green",
                    )
            else:
                self.analysis_label.config(
                    text="Engine suggests no best move or it's a draw/stalemate.",
                    fg="orange",
                )

        except Exception as e:
            self.analysis_label.config(
                text=f"Error finding best move: {str(e)}", fg="red"
            )
            print(f"Best move error: {str(e)}")

    def update_ui(self):
        """Update the UI periodically"""
        if self.root:
            self.root.update()

        # Schedule the next update
        asyncio.get_event_loop().call_later(0.1, self.update_ui)

    async def analyze_current_position(self):
        """Analyze the current position using the chess engine"""
        if not self.engine:
            self.analysis_label.config(text="Engine not initialized", fg="red")
            return
        if self.current_move_idx < 0:  # No move selected yet
            self.analysis_label.config(text="Select a move to analyze.", fg="black")
            self.quality_label.config(text="Move quality: Select a move.", fg="black")
            return

        try:
            # Using a shallower depth and shorter time for quicker feedback during navigation
            info = await self.engine.analyse(
                self.board, chess.engine.Limit(depth=15, time=0.3)
            )
        except Exception as e:
            self.analysis_label.config(text=f"Engine analysis error: {e}", fg="red")
            self.quality_label.config(text="-", fg="red")
            return

        if "score" not in info:
            self.analysis_label.config(
                text="Could not get score from engine.", fg="red"
            )
            self.quality_label.config(text="-", fg="red")
            return

        current_score_obj = info[
            "score"
        ].white()  # Current board's score from White's POV

        if current_score_obj.is_mate():
            current_eval_score = (
                (10000 - current_score_obj.mate() * 10)
                if current_score_obj.mate() > 0
                else (-10000 - current_score_obj.mate() * 10)
            )
        else:
            current_eval_score = current_score_obj.score()
            if current_eval_score is None:
                current_eval_score = 0  # Default to 0 if no score

        # Determine the player who made the *current* move displayed on the board
        player_who_made_current_move = (
            chess.WHITE if self.current_move_idx % 2 == 0 else chess.BLACK
        )

        # Convert current_eval_score to the perspective of the player who made the current move
        current_eval_pov_player = (
            current_eval_score
            if player_who_made_current_move == chess.WHITE
            else -current_eval_score
        )

        # self.previous_eval should be the evaluation of the *previous* board state,
        # from the perspective of the player who made *that previous* move.
        # For the very first move, previous_eval is 0 (from starting position).
        eval_diff = current_eval_pov_player - self.previous_eval

        eval_type = "neutral"
        for move_type_key, (min_r, max_r) in EVAL_RANGES.items():
            if min_r <= eval_diff <= max_r:
                eval_type = move_type_key
                break

        # Update self.previous_eval *for the next move's analysis*.
        # It becomes the current_eval_pov_player.
        self.previous_eval = current_eval_pov_player

        # Store the eval_type and the raw current_eval_score (White's POV or mate score) for UI display
        if self.current_move_idx >= 0:
            while len(self.move_evals) <= self.current_move_idx:
                self.move_evals.append(None)
            self.move_evals[self.current_move_idx] = (eval_type, current_eval_score)

        self.update_analysis_ui(eval_type, current_eval_score)

    async def cleanup(self):
        """Clean up resources when closing"""
        if self.engine:
            await self.engine.quit()
        if self.game_board:
            display.terminate()
        if self.root:
            self.root.destroy()


async def main():
    # Path to the chess engine (Stockfish or other compatible UCI engine)
    engine_path = r"C:\Users\adars\projects\chess\engines\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"

    # Initialize pygame and font system
    pygame.init()
    pygame.font.init()

    # Create and initialize the analyzer
    analyzer = GameAnalyzer(engine_path)
    await analyzer.initialize()

    try:
        # Keep the program running
        while True:
            await asyncio.sleep(0.1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        # Clean up
        await analyzer.cleanup()


if __name__ == "__main__":
    # Set up event loop policy for python-chess
    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())

    # Run the main function
    asyncio.run(main())
