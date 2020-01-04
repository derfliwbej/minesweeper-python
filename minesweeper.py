import os
import time
import random


def setUpGameSettings(difficulty_chosen):
    game = {"Dimensions": {"x": 0, "y": 0}, "Mines": 0, "Win":None, "Gameover":False}
    if difficulty_chosen == 1:
        game["Dimensions"]["x"] = 8
        game["Dimensions"]["y"] = 8
        game["Mines"] = 10
        game["Difficulty"] = "Easy"
    elif difficulty_chosen == 2:
        game["Dimensions"]["x"] = 16
        game["Dimensions"]["y"] = 16
        game["Mines"] = 40
        game["Difficulty"] = "Intermediate"
    elif difficulty_chosen == 3:
        game["Dimensions"]["x"] = 30
        game["Dimensions"]["y"] = 16
        game["Mines"] = 99
        game["Difficulty"] = "Expert"
    return game


def createRow(dimensions, y):
    array = []
    for x in range(0, dimensions["x"]):
        cell = {"Revealed": False, "Mine": False, "Flagged": False, "Bombs": 0, "Symbol":".", "Position": {"x": x, "y": y}}
        array.append(cell)
    return array


def plantBombs(matrix, game_settings):
    bombs_planted = 0
    while bombs_planted < game_settings["Mines"]:
        while True:
            randX = random.randint(0, game_settings["Dimensions"]["x"]-1)
            randY = random.randint(0, game_settings["Dimensions"]["y"]-1)
            if not matrix[randY][randX]["Mine"]:
                break
        matrix[randY][randX]["Mine"] = True
        bombs_planted += 1


def countBombs(matrix, game_settings):
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            countAdjacentBombs(x, y, matrix, game_settings)


def countAdjacentBombs(x, y, matrix, game_settings):
    mines = 0
    for row in range(y-1, y+2):
        for column in range(x-1, x+2):
            if row >= 0 and column >= 0 and row < game_settings["Dimensions"]["y"] and column < game_settings["Dimensions"]["x"] and matrix[row] and matrix[row][column] and matrix[row][column]["Mine"]:
                mines += 1
    matrix[y][x]["Bombs"] = mines


def createMatrix(game_settings):
    matrix = []
    dimensions = game_settings["Dimensions"]
    for y in range(0, dimensions["y"]):
        matrix.append(createRow(dimensions, y))

    plantBombs(matrix, game_settings)
    countBombs(matrix, game_settings)
    return matrix


def printMatrix(matrix, game_settings):
    dimensions = game_settings["Dimensions"]
    coordinates_x = ""
    for x in range(0, dimensions["x"]):
        if x == 0:
            coordinates_x += ("     " + str(x))
        elif x >= 10:
            coordinates_x += ("  " + str(x))
        else:
            coordinates_x += ("   " + str(x))
    print(coordinates_x)
    for y in range(0, dimensions["y"]):
        print("   " + (("+---" * dimensions["x"]) + "+"))
        row = ""
        for x in range(0, dimensions["x"]):
            row += ("| " + matrix[y][x]["Symbol"] + " ")
        if y >= 10:
            print(str(y) + " " + row + "|")
        else:
            print(str(y) + "  " + row + "|")
    print("   " + (("+---" * dimensions["x"]) + "+"))


def revealAdjacentTiles(x, y, matrix, game):
    for row in range(y-1, y+2):
        for column in range(x-1, x+2):
            if row >= 0 and column >= 0 and row < game["Dimensions"]["y"] and column < game["Dimensions"]["x"] and not matrix[row][column]["Mine"]:
                revealTile(column, row, matrix, game)


def revealTile(x, y, matrix, game):
    if matrix[y][x]["Bombs"] == 0 and not matrix[y][x]["Revealed"] and not matrix[y][x]["Mine"] and not matrix[y][x]["Flagged"]:
        matrix[y][x]["Revealed"] = True
        matrix[y][x]["Symbol"] = " "
        revealAdjacentTiles(x, y, matrix, game)
    elif matrix[y][x]["Bombs"] != 0 and not matrix[y][x]["Revealed"] and not matrix[y][x]["Mine"] and not matrix[y][x]["Flagged"]:
        matrix[y][x]["Revealed"] = True
        matrix[y][x]["Symbol"] = str(matrix[y][x]["Bombs"])


def flagTile(x, y, matrix):
    matrix[y][x]["Symbol"] = "F"
    matrix[y][x]["Flagged"] = True


def unflagTile(x, y, matrix):
    matrix[y][x]["Symbol"] = "."
    matrix[y][x]["Flagged"] = False


def revealAllMines(matrix, game_settings):
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            if matrix[y][x]["Mine"]:
                matrix[y][x]["Symbol"] = "X"
                matrix[y][x]["Revealed"] = True
    return False

'''
    Save File Format:
1   x : y: # of mines : gameover(T/F) : difficulty : win(T/F/None)
'''
def saveGame(filename, matrix, game_settings, saved_files):
    saved_files.append(filename[:-4])
    updateSavedFileDatabase(saved_files)
    file = open(filename, "w")
    file.write(str(game_settings["Dimensions"]["x"]))
    file.write(":")
    file.write(str(game_settings["Dimensions"]["y"]))
    file.write(":")
    file.write(str(game_settings["Mines"]))
    file.write(":")
    file.write(str(game_settings["Gameover"]))
    file.write(":")
    file.write(game_settings["Difficulty"])
    file.write(":")
    file.write(str(game_settings["Win"]))
    for y in range(0, len(matrix)):
        file.write("\n")
        for x in range(0, len(matrix[y])):
            for key in matrix[y][x]:
                if key == "Position":
                    file.write(str(matrix[y][x][key]["x"]))
                    file.write(":")
                    file.write(str(matrix[y][x][key]["y"]))
                else:
                    file.write(str(matrix[y][x][key]))
                    file.write(":")
            if x != len(matrix[y])-1:
                file.write("|")

    print("\t    Saving...")
    file.close()
    time.sleep(2)

def checkNotMines(matrix):
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            if (matrix[y][x]["Mine"] and not matrix[y][x]["Flagged"]) or (not matrix[y][x]["Mine"] and not matrix[y][x]["Revealed"]):
                return False
    return True


def checkIfAllMinesAreRevealed(matrix, game_settings):
    mines_revealed = 0
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            if (matrix[y][x]["Mine"] and matrix[y][x]["Revealed"]):
                mines_revealed += 1
    if mines_revealed == game_settings["Mines"]:
        return True
    else:
        return False


def winChecker(matrix, game_settings):
    if checkNotMines(matrix):
        game_settings["Gameover"] = True
        return True
    elif checkIfAllMinesAreRevealed(matrix, game_settings):
        game_settings["Gameover"] = True
        return False
    else:
        return None

def booleanParse(string):
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        return None

def updateSavedFileDatabase(saved_files):
    file = open("list_of_saves.txt", "w")

    for entry in saved_files:
        file.write(entry)
        file.write("\n")

def loadSavedFileDatabase():
    file = open("list_of_saves.txt")
    saved_file_database = []

    for entry in file:
        saved_file_database.append(entry[:-1])

    return saved_file_database

'''
    Save File Format
    0       1       2               3           4           5
    x       y    # of mines   Gameover(T/F)  Difficulty Win(T/F/None)
1   8   :   8   :   10      :     False    :   Easy    :   None



2   0         1        2        3       4      5   6
  Revealed : Mine : Flagged : Bombs : Symbol : x : y      (per cell)
'''
def loadGame(filename):
    file = open(filename, "r")
    line_number = 1
    game_settings = {"Dimensions": {"x": 0, "y": 0}, "Mines": 0, "Win":None, "Gameover":False}

    for line in file:
        if line_number == 1:
            game = line.split(":")
            game_settings["Dimensions"]["x"] = int(game[0])
            game_settings["Dimensions"]["y"] = int(game[1])
            game_settings["Mines"] = int(game[2])
            game_settings["Gameover"] = booleanParse(game[3])
            game_settings["Difficulty"] = game[4]
            game_settings["Win"] = booleanParse(game[5])
            line_number += 1
            new_matrix = createMatrix(game_settings)
        else:
            cells = line.split("|")
            for value in cells:
                data = value.split(":")
                x = int(data[5])
                y = int(data[6])
                new_matrix[y][x]["Revealed"] = booleanParse(data[0])
                new_matrix[y][x]["Mine"] = booleanParse(data[1])
                new_matrix[y][x]["Flagged"] = booleanParse(data[2])
                new_matrix[y][x]["Bombs"] = int(data[3])
                new_matrix[y][x]["Symbol"] = data[4]

    file.close()
    return [new_matrix, game_settings]

'''
For testing mode only
def revealAllForTestingMode(matrix, game_settings):
    for y in range(0, len(matrix)):
        for x in range(0, len(matrix[y])):
            if not matrix[y][x]["Mine"] and not matrix[y][x]["Revealed"] and not matrix[y][x]["Flagged"]:
                revealTile(x, y, matrix, game_settings)
            if matrix[y][x]["Mine"] and not matrix[y][x]["Revealed"]:
                matrix[y][x]["Flagged"] = True
                matrix[y][x]["Symbol"] = "F"
'''

def Game():
    saved_files = loadSavedFileDatabase()
    os.system("cls")
    print("\t\t\t +------------------+")
    print("\t\t\t |    Minesweeper   |")
    print("\t+----------------+------------------+----------------+")
    print("\t|                                                    |")
    print("\t|\t\t1. Start New Game                    |")
    print("\t|                                                    |")
    print("\t|\t\t2. Load Game                         |")
    print("\t|                                                    |")
    print("\t+----------------------------------------------------+")
    print("\n")


    while True:
        menu = input("\t\t\tEnter your choice: ")
        if menu == "1" or menu == "2":
            menu = int(menu)
            break
        else:
            print("\t\t\tPlease choose between 1 and 2!")


    if menu == 1:

        os.system("cls")
        print("\t\t\t +------------------+")
        print("\t\t\t |    Minesweeper   |")
        print("\t+----------------+------------------+----------------+")
        print("\t|                                                    |")
        print("\t|\tChoose Difficulty                            |")
        print("\t|                                                    |")
        print("\t|\t    1. Easy (8x8, 10 Mines)                  |")
        print("\t|                                                    |")
        print("\t|\t    2. Intermediate (16x16, 40 Mines)        |")
        print("\t|                                                    |")
        print("\t|\t    3. Expert (30x16, 99 Mines)              |")
        print("\t|                                                    |")
        print("\t+----------------------------------------------------+")
        print("\n")


        while True:
            difficulty_chosen = input("\t\t\tEnter your choice: ")
            if difficulty_chosen == "1" or difficulty_chosen == "2" or difficulty_chosen == "3":
                difficulty_chosen = int(difficulty_chosen)
                break
            else:
                print("\t\t\tPlease choose between 1-3!")

        game_settings = setUpGameSettings(difficulty_chosen)
        matrix = createMatrix(game_settings)
    else:
        os.system("cls")
        print()
        print("\t\t    List of saves:")
        for save in saved_files:
            print("\t\t\t" + save)
        print()
        while True:
            filename = input("\t\t\tPlease enter the name of your saved file: ")
            if filename in saved_files:
                filename = filename + ".txt"
                specs = loadGame(filename)
                matrix = specs[0]
                game_settings = specs[1]
                print("\t\t\tLoading...")
                time.sleep(2)
                break
            else:
                print("\t\t\tSaved file does not exist!")

    # revealAllForTestingMode(matrix, game_settings)
    while not game_settings["Gameover"]:
        os.system("cls")
        printMatrix(matrix, game_settings)
        print("\n")
        print("\t    What do you want to do?")
        print("\t\t1. Reveal Tile")
        print("\t\t2. Flag Tile")
        print("\t\t3. Save Game")
        print("\t\t4. Quit Game")


        while True:
            action = input("\t    Enter your choice: ")
            if action == "1" or action == "2" or action == "3" or action == "4":
                action = int(action)
                break
            else:
                print("\t    Please choose between 1-4!")


        if action == 1:
            while True:
                y = input("\t    Enter the row of the tile you want to reveal: ")
                x = input("\t    Enter the column of the tile you want to reveal: ")
                if not y.isalpha() and not x.isalpha() and int(x) < game_settings["Dimensions"]["x"] and int(y) < game_settings["Dimensions"]["y"]:
                    y = int(y)
                    x = int(x)
                    if not matrix[y][x]["Revealed"]:
                        if matrix[y][x]["Mine"] and not matrix[y][x]["Flagged"]:
                            revealAllMines(matrix, game_settings)
                        elif matrix[y][x]["Flagged"]:
                            print("\t    The tile you have chosen have been flagged and cannot be revealed!")
                            time.sleep(2)
                        else:
                            revealTile(x, y, matrix, game_settings)
                    else:
                        print("\t    The tile you have chosen is already revealed!")
                        time.sleep(2)
                    break
                else:
                    print("\t    Please print an appropriate number!")
        elif action == 2:
            while True:
                y = input("\t    Enter the row of the tile you want to flag: ")
                x = input("\t    Enter the column of the tile you want to flag: ")
                if not y.isalpha() and not x.isalpha() and int(x) < game_settings["Dimensions"]["x"] and int(y) < game_settings["Dimensions"]["y"]:
                    y = int(y)
                    x = int(x)
                    if not matrix[y][x]["Flagged"] and not matrix[y][x]["Revealed"]:
                        flagTile(x, y, matrix)
                    elif matrix[y][x]["Flagged"]:
                        unflagTile(x, y, matrix)
                    elif matrix[y][x]["Revealed"]:
                        print("\t    The tile you have chosen have already been revealed!")
                        time.sleep(2)
                    break
                else:
                    print("Please put an appropriate number!")
        elif action == 3:
            saved_name = input("\t    Please enter the name of the save: ")
            saved_name += ".txt"
            saveGame(saved_name, matrix, game_settings, saved_files)
        elif action == 4:
            break

        game_settings["Win"] = winChecker(matrix, game_settings)

    if game_settings["Win"] != None:
        os.system("cls")
        printMatrix(matrix, game_settings)
        if game_settings["Win"]:
            print("You won the game!")
        elif not game_settings["Win"]:
            print("You lost the game!")

        while True:
            play_again = input("Do you want to play again?(y/n)")
            if play_again == "y" or play_again == "n":
                if play_again == "y":
                    Game()
                    break
                elif play_again == "n":
                    print("Thanks for playing!")
                    break

Game()
