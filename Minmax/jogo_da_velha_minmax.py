import tkinter as tk
from functools import partial

# Configurações do tabuleiro
player = 'X'
ai = 'O'

def check_winner(board):
    """Verifica se há um vencedor ou empate."""
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 'Tie'
    
    return None

def minimax(board, depth, is_maximizing):
    """Implementa o algoritmo Minimax para a IA."""
    result = check_winner(board)
    if result == ai:
        return 10 - depth
    elif result == player:
        return depth - 10
    elif result == 'Tie':
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(best_score, score)
        return best_score

def best_move():
    """Encontra a melhor jogada para a IA."""
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = ai
        update_buttons()
        check_game_over()

def on_click(row, col):
    """Trata o clique do jogador no botão do tabuleiro."""
    if board[row][col] == ' ' and not check_winner(board):
        board[row][col] = player
        update_buttons()
        if not check_game_over():
            best_move()

def update_buttons():
    """Atualiza a interface do jogo."""
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=board[i][j])

def check_game_over():
    """Verifica se o jogo terminou e exibe o resultado."""
    winner = check_winner(board)
    if winner:
        if winner == 'Tie':
            label.config(text="Empate!")
        else:
            label.config(text=f"{winner} venceu!")
        return True
    return False

def reset_game():
    """Reseta o jogo para uma nova partida."""
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    label.config(text="Jogo da Velha")
    update_buttons()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Jogo da Velha - Minimax")
board = [[' ' for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

frame = tk.Frame(root)
frame.pack()

label = tk.Label(root, text="Jogo da Velha", font=("Arial", 14))
label.pack()

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(frame, text=" ", font=("Arial", 20), width=5, height=2,
                                  command=partial(on_click, i, j))
        buttons[i][j].grid(row=i, column=j)

reset_button = tk.Button(root, text="Reiniciar", font=("Arial", 12), command=reset_game)
reset_button.pack()

root.mainloop()
