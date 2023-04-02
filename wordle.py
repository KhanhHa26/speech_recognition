import random 

def correct(wordOfUser): 
  if len(wordOfUser) == 5: 
    return True
  else: 
    print("The word must be 5-letter long")

#comparing letters to letters  
def checkWord(wordOfUser, wordChoice):  
  for i in range(len(wordChoice)): 
    if wordOfUser[i]== wordChoice[i]: 
      output[i] = "*"
    elif (wordOfUser[i] != wordChoice[i]) and (wordOfUser[i] in wordChoice): 
      output[i] = "?"
    else: 
      output[i] = "_"
  return(output)
          
#count the number of attempts
def guessCount(wordChoice): 
  count = 0
  while count < 5:
    wordOfUser = input("Guess the word (put all in UPPERCASE): ")
    if correct(wordOfUser): 
      if wordOfUser == wordChoice: 
        print("You won! Hurrayyyy! It took you " + str(count+1) + " guesses")
        break
      else: 
        print(checkWord(wordOfUser, wordChoice))
        count += 1
  else: 
    print("You lost due to running out of guesses")

#instruction
wordList = ["ARISE", "MONEY", "SKILL", "MOIST", "TRUST", "MUDDY", "FUZZY"]

print("Welcome to WORDLE! Guess the 5-letter word. \nOnly 5 attempts allowed. \n * for correct letter and order. \n ? for letter in incorrect order.\n _ for letter not in the word.\n ")

wordChoice = random.choice(wordList)

output = ["_"] * len(wordChoice)
print(output)


guessCount(wordChoice)
          
          
          
      
