import os
secret_word = ""
live = 3
hangman_character = [
    "  o  ",
    "./|\\.",
    "  |  ",
    " / \\ "
]
indiviual_letters = 0
guessed_letters = []
correct_letters = []
def getIndivualLetters():
    l = []
    for letters in secret_word:
        if letters not in l:
            l.append(letters)
    return l

def reset():
    os.system("clear")
    print("Welcome to a game of Hangman, input a secret word and then follow the rules of hangman...")

def max_possible_rounds():
    return len(secret_word) + len(hangman_character)

def getNewSecretWord():
    return input("Input a new secret word!...\n\t")

def Guess():
    word_guess = ""
    guess = ""
    while True:
        guess =  input("Guess a new letter...\n\t").strip()[0]
        if guess in guessed_letters or guess == " " or guess == "_":
            continue
        elif not guess in secret_word:
            lives -=1
            print("You Failed")
            guessed_letters.append(guess)
            return
        else:
            correct_letters.append(guess)
            break 
    for letter in secret_word:
        if letter == " ":
            word_guess += " "
        elif letter in correct_letters:
            word_guess += letter
        else:
            word_guess += "_"
    print(word_guess)

def getHangmanCharacter(progress):
    if progress >= len(hangman_character):
        raise Exception("Hangman Character Part doesn't exsist")

def newRound():
    if input("\nStart new round? (yes/no) \n").strip().lower() == "yes":
        return
    else:
        exit()
while True:
    try:
        guessed_letters = []
        correct_letters = []

        lives = 3
        reset()
        secret_word = getNewSecretWord()
        indiviual_letters = getIndivualLetters()

        for rnd in range(max_possible_rounds()):
            if lives == 0:
                print("You Lost")
                break
            if len(guessed_letters) >= indiviual_letters:
                print("You Win!")
            Guess()
        
        newRound()
    except:
        os.system("clear")
        newRound()

