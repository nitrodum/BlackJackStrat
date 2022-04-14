total = input("How much money: ")
Odds = 2
Prob = .495
ProbLoss = 1-Prob
Kelly = ((Odds*Prob)-(1-Prob))/Odds
print("Kelly Criterion =", Kelly)
print("Amount to bet:", Kelly*100)
