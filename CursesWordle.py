import curses
import random
import json

# Open and read the JSON file
with open('possible_words.json', 'r') as file:
    data = json.load(file)

with open('wordle_words.json', 'r') as file:
    WORDS = json.load(file)


#I moved this into a function for readability
def text_color(stdscr, guesses, target_word):
    for i, guess in enumerate(guesses): #for each word that has been typed
            for k, letter in enumerate(guess): #for each letter in that word

                if letter == target_word[k]: #if the letter is in the same position
                    stdscr.addch(i+1, k, letter, curses.color_pair(1)) #write it in green in the corresponding coloumn, i+1 ensures we are updating the correct row. If there are 3 guesses, we are updating the fourth row, since the first row is our title.
                
                elif letter in target_word and letter!=target_word[k]:
                    stdscr.addch(i + 1, k, letter, curses.color_pair(2))

                else:
                    stdscr.addch(i + 1, k, letter, curses.color_pair(3))
            stdscr.refresh()



def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #correct
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) #wrong position
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) #incorrect input

    target_word = random.choice(WORDS)

    attempts = 6
    guesses = []

    stdscr.clear()
    stdscr.refresh()

    while attempts>0:
        stdscr.addstr(0, 0, f"Welcome to Wordle! You have {attempts} attempts remaining. Esc to quit.")

        text_color(stdscr, guesses, target_word)
    
        typed_word = []
        cursor_x=33 #start writing here
        stdscr.addstr(len(guesses) + 1, 6, "Enter your 5-letter guess: ") #len(guesses)+1 ensures this is written on the next line, every time there is a new guess added to the list

        while len(typed_word)<5:

            character_num = stdscr.getch()

            #handling backspace
            if character_num == curses.KEY_BACKSPACE or character_num == 127 or character_num == 8:
                if len(typed_word) > 0:
                    typed_word = typed_word[:-1] #delete from list
                    cursor_x -= 1 #move cursor to appropriate position
                    stdscr.move(len(guesses)+1,cursor_x) #moves the cursor
                    stdscr.addch(len(guesses)+1,cursor_x,' ') #remove character from screen
                    stdscr.move(len(guesses)+1,cursor_x) #typing a character moves the cursor to the right, so we have to put it back
                    

            #handling typing
            elif chr(character_num).isalpha(): #chr converts number into key, isalpha checks if what is currently typed is an actual letter. isalpha being false will prevent the elif from continuing
                typed_character = chr(character_num).lower()
                typed_word.append(typed_character)
                stdscr.addch(len(guesses) + 1, cursor_x, typed_character) 
                cursor_x += 1  #Move cursor forward


            #handling quitting
            if character_num == 27:
                stdscr.addstr(9,0, f"Game quit! The word is : {target_word}")
                stdscr.refresh()
                stdscr.getch()
                return
                
            
            stdscr.refresh()

        typed_word = ''.join(typed_word) #the join function and the empty string makes it so all elements in the list are combined together into one, without seperators

        #handling winning
        if typed_word == target_word:
            text_color(stdscr, guesses, target_word)
            stdscr.addstr(8, 0, "Congratulations! You guessed the word!")
            stdscr.refresh()
            stdscr.getch()
            break


        
        if (''.join(typed_word) in data):
            guesses.append(typed_word)
            attempts -= 1
            
        
        #nonexistent word
        if (''.join(typed_word) not in data):
            stdscr.move(len(guesses) + 1, 33) 
            stdscr.addstr(len(guesses) + 1, 33, ' '*5)  #remove invalid input
            stdscr.move(len(guesses) + 1, cursor_x)  #move cursor back to start of line
            stdscr.refresh()

            
        #losing
        if attempts == 0:
            text_color(stdscr, guesses, target_word) #calling this function again or the last attempt will not get colored
            stdscr.addstr(0, 0, f"Welcome to Wordle! You have 0 attempts remaining.") #the screen would show 1 attempts, despite all attempts being used up. This line isn't very efficient but it works
            stdscr.addstr(9,0, f"Game over! The word is : {target_word}")
            stdscr.refresh()
            stdscr.getch()
            break
        



        






curses.wrapper(main)