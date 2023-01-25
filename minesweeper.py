from tkinter import *
from random import sample, randint

GAME_SIZE = 600
SPACE_SIZE = 20
AMOUNT = int(GAME_SIZE / SPACE_SIZE)
i = 0

import sys
sys.setrecursionlimit(1500)

class MineSweeper:
    bomb_columns = []
    game_columns = [[] for _ in range(AMOUNT)]
    mouse_on = []

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Minesweeper")
        self.window.resizable(False, False)
        self.window.bind("<Button-3>", lambda event: self.right_click_square())
        self.window.bind("<Escape>", lambda event: self.restart())
        self.checked = []
        
        self.canvas = Canvas(self.window, bg = "#000000", width = GAME_SIZE, height = GAME_SIZE, bd = 0, relief = RAISED)
        self.canvas.pack()

        self.generate_bombs()
        self.make_squares()
        self.show_start()
        self.window.mainloop()

    def right_click_square(self):
        self.game_columns[self.mouse_on[0]][self.mouse_on[1]].switch_texture(flagged = False, game = self)
    
    def left_click_square(self, row, column) -> bool:
        self.game_columns[column][row].switch_texture(flagged = True, game = self)
    
    def restart(self):
        self.canvas.delete("all")
        self.checked = []
        self.bomb_columns = []
        self.game_columns = [[] for _ in range(AMOUNT)]
        for column in range(len(self.game_columns)):
            for row in range(len(self.game_columns[column])):
                    self.game_columns[column][row] = square()
        self.generate_bombs()
        self.make_squares()
    
    def lose(self):
        pass

    def make_squares(self):
        for column in range(0, 30):
            for row in range(0, 30):
                self.game_columns[column].append(square(row, column, self))

    def generate_bombs(self):
        
        self.bomb_columns = [[0] * AMOUNT for _ in range(AMOUNT)]

        indices = sample(range(900), randint(115, 135))

        for index in indices:
            row, col = divmod(index, 30)
            self.bomb_columns[row][col] = 'bomb'

        for column in range(len(self.bomb_columns)):
            for square in range(len(self.bomb_columns[column])):
                i = 0
                if self.bomb_columns[column][square] ==  'bomb':
                    continue
                
                if column != 0:
                    if square != 0:
                        if self.bomb_columns[column - 1][square - 1] == 'bomb':
                            i += 1
                    if self.bomb_columns[column - 1][square] == 'bomb':
                        i += 1
                    if square != len(self.bomb_columns[column]) - 1:
                        if self.bomb_columns[column - 1][square + 1] == 'bomb':
                            i += 1
                if square != 0:
                    if self.bomb_columns[column][square - 1] == 'bomb':
                        i += 1
                if square != len(self.bomb_columns[column]) - 1:
                    if self.bomb_columns[column][square + 1] == 'bomb':
                        i += 1

                if column != len(self.bomb_columns) - 1:
                    if square != 0:
                        if self.bomb_columns[column + 1][square - 1] == 'bomb':
                            i += 1
                    if self.bomb_columns[column + 1][square] == 'bomb':
                        i += 1
                    if square != len(self.bomb_columns[column]) - 1:
                        if self.bomb_columns[column + 1][square + 1] == 'bomb':
                            i += 1
                
                self.bomb_columns[column][square] = str(i)

    def show_start(self):
        empty_squares = []
        for row in range(len(self.game_columns)):
            for square in range(len(self.game_columns[row])):
                if self.game_columns[row][square].number == 0 and self.game_columns[row][square].bomb == False:
                    empty_squares.append([row, square])
        
        rand_id = randint(0, len(empty_squares))
        self.game_columns[empty_squares[rand_id][0]][empty_squares[rand_id][1]].switch_texture(flagged = False, game = self)
                

class square:
    def __init__(self, row, column, game: MineSweeper):
        self.num_images = []
        self.number = 0
        self.row = row
        self.column = column
        self.revealed = False
        for name in range(1, 8):
            self.num_images.append(PhotoImage(file = "resources/{}.png".format(name)))
        
        self.empty_image = PhotoImage(file = "resources/empty.png")
        self.bomb_image = PhotoImage(file = "resources/bomb.png")
        self.flag_image = PhotoImage(file = "resources/flag.png")

        if game.bomb_columns[column][row] == 'bomb':
            self.bomb = True
        else:
            self.bomb = False
            self.number = int(game.bomb_columns[column][row])
        
        self.button = Button(game.canvas, width = SPACE_SIZE, height = SPACE_SIZE, borderwidth = 1, command = lambda: game.left_click_square(row, column))
        self.button.place(x = column * SPACE_SIZE, y = row * SPACE_SIZE)
        self.button.bind("<Enter>", lambda event: self.enter(game))

    def enter(self, game: MineSweeper):
        game.mouse_on = [self.column, self.row]
    
    def switch_texture(self, flagged, game: MineSweeper):
        if self.revealed:
            return
        if not flagged:
            if self.number != 0:
                self.button.configure(image = self.num_images[self.number - 1])
            else:
                if self.bomb:
                    self.button.configure(image = self.bomb_image)  
        else:
            self.button.configure(image = self.flag_image)

        if self.number == 0 and not self.bomb and not flagged:

            self.button.configure(image = self.empty_image)

            if ([self.column + 1, self.row] not in game.checked) and self.column != 29:
                game.checked.append([self.column + 1, self.row])
                game.game_columns[self.column + 1][self.row].switch_texture(flagged = False, game = game)

            if [self.column - 1, self.row] not in game.checked and self.column != 0:
                game.checked.append([self.column - 1, self.row])
                game.game_columns[self.column - 1][self.row].switch_texture(flagged = False, game = game)

            if [self.column, self.row + 1] not in game.checked and self.row != 29:
                game.checked.append([self.column, self.row + 1])
                game.game_columns[self.column][self.row + 1].switch_texture(flagged = False, game = game)

            if [self.column, self.row - 1] not in game.checked and self.row != 0:
                game.checked.append([self.column, self.row - 1])
                game.game_columns[self.column][self.row - 1].switch_texture(flagged = False, game = game)

            if ([self.column + 1, self.row + 1] not in game.checked) and self.column != 29 and self.row != 29:
                game.checked.append([self.column + 1, self.row + 1])
                game.game_columns[self.column + 1][self.row + 1].switch_texture(flagged = False, game = game)

            if [self.column - 1, self.row + 1] not in game.checked and self.column != 0 and self.row != 29:
                game.checked.append([self.column - 1, self.row + 1])
                game.game_columns[self.column - 1][self.row + 1].switch_texture(flagged = False, game = game)

            if [self.column + 1, self.row - 1] not in game.checked and self.row != 29 and self.row != 0:
                game.checked.append([self.column + 1, self.row - 1])
                game.game_columns[self.column + 1][self.row - 1].switch_texture(flagged = False, game = game)

            if [self.column - 1, self.row - 1] not in game.checked and self.row != 0 and self.column != 0:
                game.checked.append([self.column - 1, self.row - 1])
                game.game_columns[self.column - 1][self.row - 1].switch_texture(flagged = False, game = game)

        if not flagged:
            self.revealed = True

def main():

    MineSweeper()

if __name__=="__main__":
   main()