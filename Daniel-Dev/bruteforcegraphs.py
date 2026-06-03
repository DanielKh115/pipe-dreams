from sage.combinat.permutation import Permutation
import matplotlib.pyplot as plt

def listtransposition(P,index):
    P[index], P[index+1] = P[index+1], P[index]
    return P

order=6 #order of the permutation group of interest
blocks=int(order*(order-1)/2) #number of blocks in the corresponding pipe dream
rednumberlist=[0]*(blocks+1)
unrednumberlist=[0]*(blocks+1)
ranklist=[0]*math.factorial(order)

transpositionorder=[] #sets the order in which transpositions are done
for i in range (order):
    for j in range (order-i-1):
        transpositionorder.append(order-j-2)

for i in range (2**blocks): #main loop: iterates over all possible pipe dreams
    binstring=bin(i)[2:]
    while (len(binstring)<blocks):
        binstring="0"+binstring
    
    L=list(range(1, order+1))
    
    unredlength=0
    for j in range (blocks):
        if (binstring[j]=="1"):
            L=listtransposition(L,transpositionorder[j]) #computes the transpositions: can probably make this native to Sagemath
            unredlength+=1
    P=Permutation(L)
    redlength=int(P.number_of_inversions())
    pindex=int(P.rank())
    ranklist[pindex]+=1
    if (unredlength==redlength):
        rednumberlist[unredlength]+=1
    else:
        unrednumberlist[unredlength]+=1


#print(unrednumberlist[0]+1)
#if uncommented, the above gives the number of pipe dreams which correspond to the identity for the given order
#this reproduces Ariella's sequence as given below
#1, 1, 2, 6, 34, 342

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[1].bar(
    list(range(blocks+1)),
    height=unrednumberlist,
    bottom=rednumberlist,
    width=1,
    label='Initially Unreduced'
)
axes[1].bar(
    list(range(blocks+1)),
    height=rednumberlist,
    width=1,
    label='Already Reduced'
)
axes[1].set_title("Unreduced Length")
plt.legend()


axes[0].bar(
    list(range(math.factorial(order))),
    ranklist,
    width=1
)
axes[0].set_title("Permutation (lex order)")


plt.tight_layout()
plt.show()
