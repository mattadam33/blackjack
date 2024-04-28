import random
import time
import itertools

#define card object with attributes suite, type and value (we are going to treat A as value 1)
class card:
    def __init__ (self, suit, type):
        self.suit=suit
        self.type=type
    
    def getValue(self):
        if self.type=="Ace":
            return 1
        elif self.type in ("10", "Jack", "Queen", "King"):
            return 10
        else:
            return int(self.type)
#function to ask user the number of decks to play with 
def setNumDeck():
    global numDeck
    answer = input("How many decks do you want to play with?")
    
    if not answer.isdigit():
        print("The entry you entered is not a positive integer, Please enter number of decks that are a positive intiger")
        setNumDeck()
    elif answer.isdigit and int(answer)>=7:
        print("Please enter number of decks that is a positive integer of 6 or less")
        setNumDeck()
    else:
       numDeck=int(answer)

#add card to player hand
def dealCardToPlayer():
    playerHand.append(deck.pop(0))

#add card to dealer hand
def dealCardToDealer():
    dealerHand.append(deck.pop(0))

#pass through a hand and get the score of the hand, treats A as 1 but will make 11 if possible
def getHandScore(hand):
    score=0
    hasAce=0
    for x in hand:
        score+=x.getValue()
        if x.type=="Ace":
            hasAce=1
    if score<=11 and hasAce==1:
        score+=10
    return score

def playerAction(hand):
    if len(hand)==2:
        action=input("What do you want to do? 1) Hit 2) Stand 3) Double Down ")
        if action.upper()=="1":
            return "Hit"
        elif action.upper()=="2":
            return "Stand"
        elif action.upper()=="3":
            return "DD"
        else:
            print("Please select a valid option.")
            playerAction(hand)
    if len(hand)>2:
        action=input("What do you want to do? 1) Hit 2) Stand ")
        if action.upper()=="1":
            return "Hit"
        elif action.upper()=="2":
            return "Stand"
        else:
            print("Please select a valid option.")
            playerAction(hand)

#asks if player wants to play again, if so returns 1, else returns 0
def playAgain():
    action=input("Do you want to play again? 1) Yes 2) No \n")
    if action=="1":
        return 1
    elif action=="2":
        return 0
    else:
        print("please select a valid option")
        playAgain()

#check if deck is less than .7 empty, if so then shuffle
def checkDeckToShuffle(d,num):
    #check if deck is half empty then shuffle
    
    if 0 <= len(d) < 0.7 * 52 * num:
        if len(d)>0:
            print("\nWe hit the shuffle card. Shuffling new deck")
        else:
            print("\nNew deck, shuffling")
        
        d=[]

        suits=["Hearts", "Clubs", "Spades", "Diamonds"]
        cards=["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

        for s in suits:
            for c in cards:
                d.append(card(s,c))

        d=d * num
        #print(deck)
        random.shuffle(d)
        return d
    else:
        print("\ndeck is not empty enouth, no shuffle")
        return d


#initialize deck and shuffle
#setNumDeck()
numDeck=2
totalMoneyAmount=0
print("We will shuffle", numDeck, "decks")
deck=[]
deck=checkDeckToShuffle(deck,numDeck)

playingSession=1

while playingSession==1:
    
    
    dealerHand=[]
    playerHand=[]
    playerTurn=1
    dealerTurn=0
    gameResult=""
    print("\nNew Game\n")
    print("Dealer is dealing cards...")
    dealCardToPlayer()
    dealCardToDealer()
    dealCardToPlayer()
    dealCardToDealer()
    ps=getHandScore(playerHand)
    ds=getHandScore(dealerHand)
    print("Player has a hand of")
    for x in playerHand:
        print(x.type+" of "+x.suit)
    print("Player score is", ps, "\n")
    print("Dealer is showing " +dealerHand[0].type + " of " +dealerHand[0].suit, "\n")

    #check for dealer blackjacks
    if dealerHand[0].type in ("Ace", "King", "Queen", "Jack", "10"):
        print("Dealer checking for blackjack")
        if ds==21:
            if ps==21:
                print("Both dealer and player have Blackjack. Push")
                gameResult="Push"
            else:
                print("Dealer has Blackjack. You lose")
                gameResult="Lose"
        else:
            print("Dealer does not have Blackjack")

    while gameResult=="":
        #actions for player
        while playerTurn==1:
            if len(playerHand)==2 and ps==21:
                print("Player Has BlackJack!")
                playerTurn=0
                dealerTurn=0
                gameResult="Blackjack"
            else:
                a=playerAction(playerHand)
                if a=="Stand":
                    playerTurn=0
                    dealerTurn=1
                    print("Player Stands. Dealer turn")        
                if a=="Hit":
                    dealCardToPlayer()
                    ps=getHandScore(playerHand)
                    print("Player Hits. New hand is")
                    for x in playerHand:
                        print(x.type+" of "+x.suit)
                    print("Score is", ps, "\n")
                    if ps>21:
                        print("Player Busts")
                        playerTurn=0
                        gameResult="Lose"
                if a=="DD":
                    dealCardToPlayer()
                    ps=getHandScore(playerHand)
                    print("Player double down to get one card. New hand is:")
                    for x in playerHand:
                        print(x.type+" of "+x.suit)
                    print("Player score is", ps)
                    playerTurn=0
                    dealerTurn=1
                    if ps>21:
                        print("Player Busts")
                        dealerTurn=0
                        gameResult="Lose"

        print("Dealer flips down card and has hand of:")
        for x in dealerHand:
            print(x.type+" of "+x.suit)
        print("Dealer score is", ds, "\n")
        #action for dealer
        while dealerTurn==1:
            if ds<17:
                dealCardToDealer()
                ds=getHandScore(dealerHand)
                print("Dealer adds a new card and now has a hand of:")
                for x in dealerHand:
                    print(x.type+" of "+x.suit)
                print("Dealer score is", ds, "\n")

            if 17<=ds<=21:
                print("Dealer Stays")
                dealerTurn=0
                print("Dealer has", ds, "Player has", ps)
                if ds>ps:
                    print("Player Loses")
                    gameResult = "Lose"
                elif ds==ps:
                    print("player pushes")
                    gameResult="Push"
                elif ds<ps:
                    print("Player Wins!")
                    gameResult="Win"
            if ds>21:
                print("Dealer Busts! Player wins!")
                gameResult="Win"
                dealerTurn=0
    checkDeckToShuffle(deck,numDeck)
    a=playAgain()
    playingSession=a
    
    
        
        



 

            


    











    








