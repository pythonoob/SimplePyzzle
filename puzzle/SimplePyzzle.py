# -*- coding: utf-8 -*-
import math
import random

class SimplePyzzle:
    END_GAME = 0

    def __init__(self, fichas):
        self.board = self.gen_board(int(math.sqrt(fichas)))

    def level(self):
        return len(self.board)

    def get_pos (self, x, y):
        return self.board[x][y]

    def gen_board(self, level):
        nums = set()
        max = level ** 2
        aux = []
        for i in range(level):
            aux.append([])
            for j in range(level):
                rand = random.randint(1, max)
                while rand in nums:
                    rand = random.randint(1, max)
                aux[i].append(rand)
                nums.add(rand)
        return aux

    def is_solved(self):
        level = len(self.board)
        num = 1
        for i in range(level):
            for j in range(level):
                if self.board[i][j] != num:
                    return False
                num = num + 1
        return True

    def valid_pos(self, x, y):
        return x >= 0 and x < len(self.board) and y >= 0 and y < len(self.board[x])

    def play(self, xi, yi, xf, yf):
        if not self.is_solved():
            if (self.valid_pos(xi, yi) and self.valid_pos(xf, yf)):
                self.change_pos(xi, yi, xf, yf)
                if self.is_solved():
                    return SimplePyzzle.END_GAME
        else: return SimplePyzzle.END_GAME


    def change_pos(self, xi, yi, xf, yf):
        aux = self.board[xi][yi]
        self.board[xi][yi] = self.board[xf][yf]
        self.board[xf][yf] = aux
