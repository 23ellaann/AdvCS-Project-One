import sys

import pygame
from pygame.locals import *

import random
import time
import numpy as np
from enum import IntEnum

pygame.init()

FPS = pygame.time.Clock()
FPS.tick(60)

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DISPLAY = pygame.display.set_mode((400, 550))
DISPLAY.fill(WHITE)
pygame.display.set_caption("Game")

bboard = np.zeros((8, 8))
fboard = np.zeros((8, 8))
anaboard = np.zeros((8, 8))
pboard = np.zeros((8, 8))
cboard = np.zeros((8, 8))
uboard = np.zeros((8, 8))

aboard = [[], [], [], [], [], [], [], []]
font = pygame.font.SysFont(None, 40)
nonmines = 0
mines = 0
flagcount = 8
firstClick = 1
gameWon = 0
gameOver = 0
waitForNG = False
start_t = time.perf_counter()
won = 0
lost = 0
total_t = 0

def setup():
    global nonmines, mines, flagcount, firstClick, gameWon, gameOver, waitForNG, start_t, bboard, fboard, pboard, anaboard, cboard, uboard, aboard
    msgdisplay = font.render("Minesweeper", True, (0, 0, 0))
    DISPLAY.blit(msgdisplay, (120, 35))

    nonmines = 0
    mines = 0
    flagcount = 8
    firstClick = 1
    gameWon = 0
    gameOver = 0
    waitForNG = False
    start_t = time.perf_counter()

    bboard = np.zeros((8, 8))
    fboard = np.zeros((8, 8))
    anaboard = np.zeros((8, 8))
    pboard = np.zeros((8, 8))
    cboard = np.zeros((8, 8))
    uboard = np.zeros((8, 8))
    aboard = [[], [], [], [], [], [], [], []]

    row = -1
    column = -1

    mineslst = [0, 1, 2, 3, 4, 5, 6, 7]

    for i in mineslst:
        mineslst[i] = random.randint(0, 64)

    index = -1
    for a in mineslst:
        index += 1
        n = mineslst.count(a)
        if n > 1:
            mineslst[index] = random.randint(0, 63)

    row = -1
    column = -1
    for a in mineslst:
        row = a // 8 - 1
        column = a % 8 - 1
        bboard[row][column] = 9


    row = -1
    column = -1
    for i in range(8):
        row = i
        column = -1
        for j in range(8):
            column = j
            x = row * 50 + 2
            y = column * 50 + 80
            rect = pygame.draw.rect(DISPLAY, GREEN, pygame.Rect(x, y, 45, 45))
            aboard[row].append(rect)
            if bboard[row][column] != 9:
                if row != 0:
                    if bboard[row - 1][column] == 9:
                        bboard[row][column] += 1
                    if bboard[row - 1][column - 1] == 9:
                        bboard[row][column] += 1

                    if column != 7:
                        if bboard[row - 1][column + 1] == 9:
                            bboard[row][column] += 1

                if column != 0:
                    if row != 7:
                        if bboard[row + 1][column - 1] == 9:
                            bboard[row][column] += 1
                    if bboard[row][column - 1] == 9:
                        bboard[row][column] += 1

                if row != 7:
                    if bboard[row + 1][column] == 9:
                        bboard[row][column] += 1
                    if column != 7:
                        if bboard[row + 1][column + 1] == 9:
                            bboard[row][column] += 1

                if column != 7:
                    if bboard[row][column + 1] == 9:
                        bboard[row][column] += 1
        print(len(aboard[row]))
           # if bboard[row][column] == 0:
           #     pygame.draw.rect(DISPLAY, GREEN, pygame.Rect(x, y, 45, 45))
           # if bboard[row][column] == 1:
           #     pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(x, y, 45, 45))
    return aboard

def is_over(rect, pos):
    # function takes a tuple of (x, y) coords and a pygame.Rect object
    # returns True if the given rect overlaps the given coords
    # else it returns False
    return rect.collidepoint(pos[0], pos[1])

def clear_all():
    global uboard
    for row, i in enumerate(aboard):
        # print(len(i))
        for column, j in enumerate(i):
            x = row * 50 + 2
            y = column * 50 + 80
            # print(row, column)
            uboard[row, column] = 1
            rect = pygame.draw.rect(DISPLAY, BLUE, pygame.Rect(x, y, 45, 45))
            n = bboard[row, column]
            surr = font.render(str(int(n)), True, (0, 0, 0))
            DISPLAY.blit(surr, (x + 15, y + 10))
            if n == 9:
                rect = pygame.draw.rect(DISPLAY, BLACK, pygame.Rect((x), (y), 45, 45))

def is_clicked(row, column, ai):
    global uboard
    global nonmines
    global cboard
    global gameOver
    global gameWon
    global firstClick
    global lost
    global won
    if firstClick == 1:
        firstClick = 0
    if gameWon == 1 or gameOver == 1:
        return
    num = bboard[row][column]
    x = row * 50 + 2 + 15
    y = column * 50 + 80 + 10
    # print(num)
    r = [0, 1, 2, 3, 4, 5, 6, 7]
    mines = 0
    for a in r:
        for b in r:
            if bboard[a, b] == 9 and fboard[a, b] == 1:
                mines += 1
    if mines + nonmines == 64:
        gameWon == 1
        won += 1
        clear_all()
        wonmsg = font.render("You Won!!", True, (0, 0, 0))
        DISPLAY.blit(wonmsg, (490, 35))
    elif uboard[row, column] == 0:
        if num != 9:
            rect = pygame.draw.rect(DISPLAY, BLUE, pygame.Rect(x - 15, y - 10, 45, 45))
            surr = font.render(str(int(num)), True, (0, 0, 0))
            DISPLAY.blit(surr, (x, y))
            nonmines += 1
            cboard[row, column] = 1
            uboard[row, column] = 1
            ai.updateKnowledge(row, column)
            if (num == 0):
                uncoverNeighbours(row, column, ai)
        if num == 9:
            rect = pygame.draw.rect(DISPLAY, BLACK, pygame.Rect((x - 15), (y - 10), 45, 45))
            rect = pygame.draw.rect(DISPLAY, WHITE, pygame.Rect(120, 35, 200, 45))
            clear_all()
            lost += 1
            gameOver = 1
            gameovermsg = font.render("Game Over", True, (0, 0, 0))
            DISPLAY.blit(gameovermsg, (490, 35))
            uboard[row, column] = 1


def is_flagged(row, column):
    global mines
    global flagcount
    if gameWon == 1 or gameOver == 1:
        return
    if nonmines + mines == 64 and nonmines == 8:
        gameWon == 1
        return
    if fboard[row][column] == 0:
        x = row * 50 + 2 + 10
        y = column * 50 + 80 + 10
        num = bboard[row][column]
        rect = pygame.draw.rect(DISPLAY, BLACK, pygame.Rect((x), (y), 25, 25))
        fboard[row][column] = 1
        if num == 9:
            mines = mines + 1
        fboard[row][column] = 1
        flagcount = flagcount - 1
    else:
        x = row * 50 + 2
        y = column * 50 + 80
        num = bboard[row][column]
        rect = pygame.draw.rect(DISPLAY, GREEN, pygame.Rect((x), (y), 45, 45))
        fboard[row][column] = 0
        flagcount += 1
        if num == 9:
            mines = mines - 1

def get_nei_indices(x, y):
    neighbours = []
    if x > 0:
        neighbours.append((x - 1, y))
        if y > 0:
            neighbours.append((x - 1, y - 1))
        if y < 8 - 1:
            neighbours.append((x - 1, y + 1))
    if y < 8 - 1:
        neighbours.append((x, y + 1))
    if y > 0:
        neighbours.append((x, y - 1))
    if x < 8 - 1:
        neighbours.append((x + 1, y))
        if y > 0:
            neighbours.append((x + 1, y - 1))
        if y < 8 - 1:
            neighbours.append((x + 1, y + 1))
    return neighbours

def uncoverNeighbours(x, y, ms_ai):

    if x > 0:
        if (bboard[x - 1][y] == 0):
            is_clicked(x - 1, y, ms_ai)
        if y > 0:
            if (bboard[x - 1][y - 1] == 0):
                is_clicked(x - 1, y - 1, ms_ai)
        if y < 8 - 1:
            if (bboard[x - 1][y + 1] == 0):
                is_clicked(x - 1, y + 1, ms_ai)
    if y < 8 - 1:
        if (bboard[x][y + 1] == 0):
            is_clicked(x, y + 1, ms_ai)
    if y > 0:
        if (bboard[x][y - 1] == 0):
            is_clicked(x, y - 1, ms_ai)
    if x < 8 - 1:
        if (bboard[x + 1][y] == 0):
            is_clicked(x + 1, y, ms_ai)
        if y > 0:
            if (bboard[x + 1][y - 1] == 0):
                is_clicked(x + 1, y - 1, ms_ai)
        if y < 8 - 1:
            if (bboard[x + 1][y + 1] == 0):
                is_clicked(x + 1, y + 1, ms_ai)

class KnowledgeDatum:
    def __init__(self):
        self.cell = []
        self.mineCount = 0
        self.x = -1
        self.y = -1

    def __repr__(self):
        return f"cell: {self.cell}. minecount: {self.mineCount}, pos: {self.x, self.y}"


class Minesweeper_AI:
    knowledge = []
    guesses = 0
    moves = 0

    def randomMove(self):
        global cboard
        global pboard
        rmCol = random.randrange(0, 7)
        rmRow = random.randrange(0,7)
        while (cboard[rmRow, rmCol] or pboard[rmCol][rmRow]):
            rmCol = random.randrange(0, 7)
            rmRow = random.randrange(0, 7)
        return rmCol, rmRow

    def contains(self, small, big):
        return set(small).issubset(set(big))

    def intersection(self, list1, list2):
        return list(set(list1) & set (list2))

    def generateProbabilities(self):
        global flagcount, nonmines, anaboard, pboard, cboard
        flagsSet = (8 - flagcount)
        if (64 - flagsSet - nonmines) > 0:
            defaultProbability = flagcount / (64 - flagsSet - nonmines)
        else:
            return
        for x in range(8):
            for y in range(8):
                anaboard[x][y] = 0
                if cboard[x][y] == 1:
                    pboard[x][y] = 0
                elif pboard[x][y] == 0:
                    pboard[x][y] = defaultProbability
        for kd in self.knowledge:
            # print(kd)
            if (kd.cells):
                newprob = kd.mineCount / len(kd.cells)
                for cell in kd.cells:
                    if (cboard[cell] == 0) and (not fboard[cell] == 1):
                        if(anaboard[cell] == 0):
                            pboard[cell] = newprob
                            anaboard[cell] = 1
                        if(anaboard[cell] == 1 and pboard[cell] < newprob):
                            pboard[cell] = newprob

    def getMinProbCell(self):
        global cboard, pboard
        minProb = 1
        cell = None
        for x in range(8):
            for y in range(8):
                if (cboard[x][y] == 0):
                    if (pboard[x][y] <= minProb):
                        cell = (x, y)
                        minProb = pboard[x][y]
        # print(minProb)
        return cell

    def generateKnowledge(self):
        pass

    def move(self):
        global fboard
        global pboard
        global firstClick
        r = [0, 1, 2, 3, 4, 5, 6, 7]
        for x in r:
            for y in r:
                if (fboard[x][y] == 1) and (pboard[x][y] < 1) or (fboard[x][y] == 0 and pboard[x][y] == 1):
                    is_flagged(x, y)
                    # print("flagged")

        if firstClick == 1:
            self.moves += 1
            return self.randomMove()

        if gameWon == 1:
            return

        #print(self.knowledge)
        for kd in self.knowledge:
            if (kd.mineCount == 0) and (len(kd.cells) > 0):
                self.moves += 1
                return kd.cells[0]

        self.generateProbabilities()
        cell = self.getMinProbCell()

        self.moves += 1
        self.guesses += 1
        return cell

    def updateKnowledge(self, x, y):
        global cboard, bboard, pboard
        if cboard[x][y] == 1:
            kd = KnowledgeDatum()
            kd.mineCount = bboard[x][y]
            kd.x = x
            kd.y = y

            updatedKnowledge = []
            if (bboard[x][y] != 9):
                for kd2 in self.knowledge:
                    if (x, y) in kd2.cells:
                        kd2.cells.remove((x, y))
                        updatedKnowledge.append(kd2)

            if kd.mineCount == 0:
                return

            kd.cells = get_nei_indices(x, y)
            for cell in get_nei_indices(x, y):
                if cboard[cell] == 1:
                    kd.cells.remove(cell)

            self.knowledge.append(kd)

            newKnowledge = []
            for kd3 in updatedKnowledge:

                if len(kd3.cells) > 1:
                    for kd2 in self.knowledge:
                        if (kd2 != kd3):
                            if (len(kd2.cells) > 0) and (self.contains(kd3.cells, kd2.cells)):
                                newkd = KnowledgeDatum()
                                newkd.cells = [x for x in kd2.cells if x not in kd3.cells]
                                newkd.mineCount = kd2.mineCount - kd3.mineCount
                                newKnowledge.append(newkd)
            self.knowledge = self.knowledge + newKnowledge

            for kd2 in self.knowledge:
                if len(kd2.cells) == kd2.mineCount:
                    for cell in kd2.cells:
                        c = cell[0]
                        d = cell[1]
                        pboard[c][d] = 1

            r = range(8)
            for x in r:
                for y in r:
                    if pboard[x][y] == 1:
                        for kd2 in self.knowledge:
                            if (x, y) in kd2.cells:
                                kd2.cells.remove((x, y))
                                kd2.mineCount -= 1

setup()
ai = Minesweeper_AI()
ai_loop = False

while True:
    ev = pygame.event.get()

    for event in ev:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Enter for AI move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                mv = ai.move()
                if mv is not None:
                    time.sleep(0.5)
                    ms.click(mv[0], mv[1], ms_ai)
                    # print("=>" + str(mv))
            if event.key == pygame.K_l:
                start_t = time.perf_counter()
                ai_loop = not ai_loop

        row = -1
        for i in aboard: # todo: fix
            row = row + 1
            column = -1
            for j in i:
                column += 1
                for event in ev:
                    if event.type == pygame.KEYDOWN:
                        if event.key == 32:
                            if aboard[row][column].collidepoint(pygame.mouse.get_pos()):
                                is_clicked(row, column, ai)
                        if event.key == 1073742049:
                            if aboard[row][column].collidepoint(pygame.mouse.get_pos()):
                                if flagcount > 0:
                                    is_flagged(row, column)
    if lost or won:
        wonmsg2 = font.render(str(won / (won + lost)), True, (0, 0, 0))
        DISPLAY.blit(wonmsg2, (45, 520))

    if ai_loop:
        mv = ai.move()
        if mv is not None:
            is_clicked(mv[0],mv[1], ai)
            # print("=>"+str(mv))
    #screen.fill(grey)
    if gameOver or gameWon:
        time.sleep(1)
        if (not waitForNG):
            if (gameOver == 1):
                lost += 1
                setup()
                print("calculating...") # loss
            if (gameWon == 1):
                won += 1
                setup()
                print("won")
            waitForNG = True
        if (ai_loop):
            end_t = time.perf_counter()
            time_taken = end_t - start_t
            total_t += time_taken
            ai.knowledge = []
            waitForNG = False
            start_t = time.perf_counter()

    pygame.display.update()

