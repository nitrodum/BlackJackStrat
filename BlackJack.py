import random

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.busted = False
        self.hasAce = False
        self.blackJack = False
        self.canDouble = True
        self.doubled = False
        self.bankRoll = 0
        self.bet = 0
        if(id == 0):
            self.type = "Player"
        if(id == 1):
            self.type = "Dealer"
        if(id == 2):
            self.type = "You"
    def pullCard(self, Deck):
        self.hand.append(Deck.pull())
    def strat(self, Deck):
        self.firstTotal()
        self.checkAce()
        self.checkBJ()
        if(self.id == 0):
            self.simpleStrat(Deck)
        if(self.id == 1):
            self.dealerStrat(Deck)
        if(self.id == 2):
            self.playerChoice(Deck)
    def bust(self):
        self.busted = True
    def dealerStrat(self, Deck):
        self.draw(Deck)
        self.checkAce()
        if(self.total > 21 and self.hasAce):
            self.total -= 10
            self.hasAce = False
            self.draw(Deck)
    def simpleStrat(self, Deck):
        if(self.total > 8 and self.total < 12):
            self.double(Deck)
        else:
            self.draw(Deck)
        self.checkAce()
        if(self.total > 21 and self.hasAce):
            self.total -= 10
            self.hasAce = False
            if(not self.doubled):
                self.draw(Deck)
    def playerChoice(self, Deck):
        self.printHand()
        if(not self.blackJack):
            if(self.canDouble):
                ans = input("Enter H to hit, S to Stand, or D to double")
                while(not ans == 'H' and not ans == 'S' and not ans == 'D'):
                    ans = input("Enter H to hit, S to Stand, or D to double")
                if(ans == 'H'):
                    self.drawOne(Deck)
                elif(ans == 'D'):
                    self.double(Deck)
                elif(ans == 'S'):
                    return
            if(not self.doubled):
                while(self.total < 21):
                    self.printHand()
                    ans = input("Enter H to hit or S to Stand")
                    while(not ans == 'H' and not ans == 'S'):
                        ans = input("Enter H to hit or S to Stand")
                    if(ans == 'H'):
                        self.drawOne(Deck)
                    elif(ans == 'S'):
                        return
    def draw(self, Deck):
        self.canDouble = False
        while(self.total <= 16):
            self.pullCard(Deck)
            self.total += self.hand[len(self.hand)-1].value
    def drawOne(self, Deck):
        self.canDouble = False
        self.pullCard(Deck)
        self.total += self.hand[len(self.hand)-1].value
    def double(self, Deck):
        self.drawOne(Deck)
        self.double = True
    def printHand(self):
        print("YOUR HAND")
        for x in self.hand:
            x.printCard()
        print("Your Total: " , self.total)
        print("Dealer Card: ", a.dealer.hand[1].value)
    def checkAce(self):
        for i in range(len(self.hand)):
                if(self.hand[i].number == 1):
                    self.hasAce = True
                    self.hand[i].number = 0
                    return
    def checkBJ(self):
        if(self.hasAce and self.total == 21):
            self.blackJack = True
    def firstTotal(self):
        self.total = self.hand[0].value + self.hand[1].value
    def setId(self, ID):
        self.id = ID
    def setType(self, Type):
        self.type = Type
    def setBank(self, bank):
        self.bankRoll = bank
    def setBet(self, Bet):
        self.bet = Bet
    def winBet(self):
        self.bet = -self.bet
    def bjBet(self):
        self.bet = -((3/2)*self.bet)
class Deck:
    def __init__(self, decks):
        self.fullDeck = []
        self.pulledDeck = []
        self.decks = decks
        for i in range(self.decks):
            for j in range(4):
                for k in range(1,14):
                    self.addCard(Card(j, k, i, False))
    def addCard(self, Card):
        self.fullDeck.append(Card)
    def pull(self):
        self.index = random.randrange(len(self.fullDeck))
        card = self.fullDeck[self.index]
        self.pulledDeck.append(card)
        self.fullDeck.remove(card)
        card = self.pulledDeck[len(self.pulledDeck)-1]
        return card
        
    
class Card:
    def __init__(self, suit, number, deck, pulled):
        self.number = number
        self.deck = deck
        self.pulled = pulled
        if(number > 1 and number < 10):
            self.value = number
        if(number > 9):
            self.value = 10
        if(number == 1):
            self.value = 11
        if(suit == 0):
            self.suit = "Spades"
        if(suit == 1):
            self.suit = "Hearts"
        if(suit == 2):
            self.suit = "Diamonds"
        if(suit == 3):
            self.suit = "Clubs"
    def printCard(self):
        print(self.suit, self.number, " Value: ", self.value)
class Game:
    dealer = Player(1)
    players = []
    deck = Deck(6)
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
        for i in range(playerNumber):
            self.players.append(Player(0))
        self.draw()
        self.dealer.firstTotal()
    def draw(self):
        for x in range(2):
            for i in range(self.playerNumber):
                self.players[i].pullCard(self.deck)
            self.dealer.pullCard(self.deck)
    def run(self):
        for i in self.players:
            i.strat(self.deck)
            if(i.total > 21):
                i.bust()
        self.dealer.strat(self.deck)
        print()
        self.check()
    def play(self):
        playerIndex = random.randrange(len(self.players))
        self.players[playerIndex].setId(2)
        self.players[playerIndex].setType("You")
        self.run()
    def check(self):
        for i in self.players:
                if(i.blackJack):
                    i.bjBet()
                    if(i.id == 0):
                        print(i.type, self.players.index(i), "BLACKJACK", i.total)
                    elif(i.id == 2):
                        print("You have a BLACKJACK!")
        if(self.dealer.blackJack):
            print("Dealer", "BLACKJACK", self.dealer.total)
        if(self.dealer.total > 21):
            self.dealer.bust()
            print("Dealer Busted")
            for i in self.players:
                if(i.busted == False and not i.blackJack):
                    i.winBet()
                    if(i.id == 0):
                        print(i.type, self.players.index(i), "WINS", i.total)
                    elif(i.id == 2):
                        print("You Win", i.total)
                    if(i.busted):
                        if(i.id == 0):
                            print(i.type, self.players.index(i), "BUSTED", i.total)
                        elif(i.id == 2):
                            print("You Busted", i.total)
        if(self.dealer.busted == False):
            print("DEALER", self.dealer.total)
            for i in self.players:
                if(i.busted):
                    if(i.id == 0):
                        print(i.type, self.players.index(i), "BUSTED", i.total)
                    elif(i.id == 2):
                        print("You Busted", i.total)
                if(i.total < self.dealer.total):
                    i.bust()
                    if(i.id == 0):
                        print(i.type, self.players.index(i), "Lost", i.total)
                    elif(i.id == 2):
                        print("You Lost", i.total)
                if(i.total == self.dealer.total):
                    i.setBet(0)
                    if(i.id == 0):
                        print(i.type, self.players.index(i), "TIES", i.total)
                    elif(i.id == 2):
                        print("You Tie", i.total)
                if(i.total > self.dealer.total and i.busted == False and not i.blackJack):
                    i.winBet()
                    if(i.id == 0):
                        print(i.type, self.players.index(i), "WINS", i.total)
                    elif(i.id == 2):
                        print("You Win", i.total)          
    def settleBets(self):
        for i in self.players:
            i.setBank(i.bankRoll - i.bet)
    def printHands(self):
        for i in range(a.playerNumber):
            print()
            print("Player", i)
            for j in range(len(a.players[i].hand)):
                a.players[i].hand[j].printCard()
        print()
        print("Dealer")
        for x in self.dealer.hand:
            x.printCard()
        
val = int(input("How many Players?"))
while(val < 0 or val > 6):
    val = int(input("Please enter a number between 1-6"))
a = Game(val)

ans = input("Enter PLAY to play or SIMULATE to simulate")
while((not(ans == 'PLAY')) and (not(ans == 'SIMULATE'))):
      ans = input("Enter PLAY to play or SIMULATE to simulate")
if(ans == 'SIMULATE'): 
    a.run()
    a.printHands()
elif(ans == 'PLAY'):
    a.play()
    a.printHands()
# If win Bankroll = Bankroll + 2 x bet


