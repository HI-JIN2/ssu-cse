def knapsack (i, profit, weight):
    global maxprofit, numbest, bestset
    if (weight <= W and profit > maxprofit):
        maxprofit = profit
        numbest = i
        bestset = include[:]
    if (promising(i, profit, weight)):
        include[i + 1] = True
        knapsack(i + 1, profit + p[i+1], weight + w[i+1])
        include[i + 1] = False
        knapsack(i + 1, profit, weight)

def promising (i, profit, weight):
    if (weight > W):
        return False
    else:
        j = i + 1
        bound = profit
        totweight = weight
        while (j <= n and totweight + w[j] <= W):
            totweight += w[j]
            bound += p[j]
            j += 1
        k = j
        if (k <= n):
            bound += (W - totweight) * p[k] / w[k]
        return bound > maxprofit

n=4
W=16
w=[0,2,5,10,5]
p=[0,40,30,50,10]
maxprofit=0
numbest=0
bestset=[]
include=[False]*(n+1)

knapsack(0,0,0)
print(bestset[1:len(bestset)])