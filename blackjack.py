##import necessery function
from IPython.display import clear_output
from random import randint

##create blackjack class

class Blackjack():
    def __init__(self):
        self.deck=[]
        self.suits=("Spades","hearts","Diamonds","Clubs")
        self.values=(2,3,4,5,6,7,8,9,10,"J","Q","K","A")

    ##creating 52 cards
    def makedeck(self):
        for suit in self.suits:
            for value in self.values:
                self.deck.append((value,suit))
    def pullcard(self):
        return self.deck.pop( randint(0, len(self.deck)-1))
    
class Player():
    def __init__(self,name):
        self.name=name 
        self.hand=[]
    
    def addcard(self,card):
        self.hand.append(card)

    def showHand(self,dealer_start= True):
        print("\n{}".format(self.name))
        print("======================")

        for i in range(len(self.hand)):
            if self.name== "Dealer" and i==0 and dealer_start:
                print("- of -")
            else:
                card=self.hand[i]
                print("{} of {}".format( card[0],card[1]))

    def calcHand(self,dealer_start=True):
        total=0
        aces=0
        card_values={1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "J":10, "Q":10, "k":10, "A":11}
        if self.name== "Dealer" and dealer_start:
            card=self.hand[1]
            return card_values[ card[0]]
        for card in self.hand:
            if card[0]=="A":
                aces+=1
            else: 
                total+= card_values[ card[0]]
        for i in range(aces):
            if total+11> 21:
                total +=1
            else:
                total +=11
        return total
############################

game=Blackjack()
game.makedeck()
###print(game.deck)
##print( game.pullcard(), len(game.deck))

name=input("whats your name?")

player= Player(name)
dealer= Player("Dealer")
##print(player.name, dealer.name)
# add 2 cards to the dealer and player hand
for i in range(2):
    player.addcard( game.pullcard())
    dealer.addcard( game.pullcard())
##print("Player: {} \nDealer Hand:{}".format(player.hand, dealer.hand) )

dealer.addcard(game.pullcard())

player.showHand()
dealer.showHand()

player_bust=False
while input("Would you like to stay or hit?").lower() !="stay":
    clear_output()
    player.addcard(game.pullcard())
    player.showHand()
    dealer.showHand()

    if player.calcHand()>21:
        player_bust=True
        print("You lose!")
        break

clear_output()
player.showHand()
dealer.showHand(False)

if player_bust:
    print("You busted, better next time")
elif dealer_bust:
    print("The dealer_busted, you win")
elif dealer.calcHand(False) > player.calcHand():
    print("Dealer has hriger cards, you lose!")
elif dealer.calcHand(False) <player.calcHand():
    print("You beat the dealer: Congrats!")
else:
    print("You Pushed, no one wins")