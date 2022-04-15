import random

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.busted = False
        self.hasAce = False
        self.blackJack = False
        self.canDouble = True
        self.double = False
        self.bankRoll = 0
        self.bet = 0
        if(id == 0):
            self.type = "Player"
        if(id == 1):
            self.type = "Dealer"
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
        self.draw(Deck)
        self.checkAce()
        if(self.total > 21 and self.hasAce and not self.double):
            self.total -= 10
            self.hasAce = False
            self.draw(Deck)
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
    def setBank(self, bank):
        self.bankRoll = bank
    def setBet(self, Bet):
        self.bet = Bet
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
    def draw(self):
        for x in range(2):
            for i in range(self.playerNumber):
                self.players[i].pullCard(self.deck)
            self.dealer.pullCard(self.deck)
    def run(self):
        for i in range(self.playerNumber):
            self.players[i].strat(self.deck)
            if(self.players[i].total > 21):
                self.players[i].bust()
        self.dealer.strat(self.deck)
        self.check()
    def check(self):
        for i in range(self.playerNumber):
                if(self.players[i].blackJack):
                    print("PLAYER", i, "BLACKJACK", self.players[i].total)
        if(self.dealer.blackJack):
            print("Dealer", "BLACKJACK", self.dealer.total)
        if(self.dealer.total > 21):
            self.dealer.bust()
            print("Dealer Busted")
            for i in range(self.playerNumber):
                if(self.players[i].busted == False and not self.players[i].blackJack):
                    print("PLAYER", i, "WINS", self.players[i].total)
                print("PLAYER", i, "BUSTED", self.players[i].total)
        if(self.dealer.busted == False):
            print("DEALER", self.dealer.total)
            for i in range(self.playerNumber):
                if(self.players[i].busted):
                    print("PLAYER", i, "BUSTED", self.players[i].total)
                if(self.players[i].total < self.dealer.total):
                    self.players[i].bust()
                    print("PLAYER", i, "LOST", self.players[i].total)
                if(self.players[i].total == self.dealer.total):
                    print("PLAYER", i, "TIES", self.players[i].total)
                if(self.players[i].total > self.dealer.total and self.players[i].busted == False and not self.players[i].blackJack):
                    print("PLAYER", i, "WINS", self.players[i].total)            
    def bets(self):
        for i in range(self.playerNumber):
            self.players[i].setBank(self.players[i].bankRoll - self.players[i].bet)
        
val = int(input("How many Players?"))
while(val < 0 or val > 6):
    val = int(input("Please enter a number between 1-6"))
a = Game(val)
a.run()
for i in range(a.playerNumber):
    print("Player", i)
    for j in range(len(a.players[i].hand)):
        a.players[i].hand[j].printCard()
print("Dealer")
for x in range(len(a.dealer.hand)):
    a.dealer.hand[x].printCard()

# If win Bankroll = Bankroll + 2 x bet


