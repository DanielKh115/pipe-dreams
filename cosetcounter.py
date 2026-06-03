"""
calculates the number of elements in the orbit of a given set of elements under the action of generalized chutes, inverse generalized chutes, and double cross flips
"""

order=7 #size of the pipe dream under consideration--largest order permutation group that can be embedded
blocks=int(order*(order-1)/2) #number of blocks in the pipe dream

preparser(false)

idlist=[0] #given set of elements
#pipe dreams are encoded as numbers: their binary representation reads out where crosses go
foundlist=[]
searchlist=[0]

while (len(searchlist)>0):
    searchelement=searchlist[0]
    foundlist.append(searchlist[0])
    searchlist=searchlist[1:]
    
    searchstring=bin(searchelement)[2:]
    while (len(searchstring)<blocks):
        searchstring="0"+searchstring
    pairlist=[]
    #first entry is the position index, second is the permutation index coming
    #in from the left, third is the permutation index coming in from the bottom
    
    searchstring=bin(searchelement)[2:]
    while (len(searchstring)<blocks):
        searchstring="0"+searchstring
    
    #identify which pair of permutation indices are in each square
    pairlist=[]
    #first entry is the position index, second is the permutation index coming
    #in from the left, third is the permutation index coming in from the bottom
    #fourth entry is the state of the position (bump/cross tile)
    for i in range (order-1): #first column left inputs
        pairlist.append([i,order-i-1])
    pairlist[0].append(order) #first column bottom bottum input
    pairlist[0].append(int(searchstring[0]))
    xoffset=0
    for i in range (order-2): #remaining columns
        for j in range (order-i-2): #remaining bottom inputs
            pos=xoffset+1+j
            pairlist[pos].append(pairlist[pos-1][1+int(searchstring[pos-1])])
            pairlist[pos].append(int(searchstring[pos]))
        xoffset+=order-i-1
        for j in range (order-i-2): #left inputs
            pos=xoffset+j
            pairlist.append([pos,pairlist[pos-order+i+2][2-int(searchstring[pos-order+i+2])]])
        pairlist[xoffset].append(pairlist[xoffset-order+i+1][2-int(searchstring[xoffset-order+i+1])]) #bottom bottom input
        pairlist[xoffset].append(int(searchstring[xoffset]))
    
    #make the pairs in increasing order (don't care which is left/bottom)
    for i in range (len(pairlist)):
        if (pairlist[i][1]>pairlist[i][2]):
            pairlist[i][1], pairlist[i][2] = pairlist[i][2], pairlist[i][1]
    
    #bubble sort of the pairlist
    t=0
    while (t==0):
        t=1
        for i in range (len(pairlist)-1):
            if (pairlist[i][1]>pairlist[i+1][1]) or ((pairlist[i][1]==pairlist[i+1][1]) and (pairlist[i][2]>pairlist[i+1][2])):
                t=0
                pairlist[i], pairlist[i+1] = pairlist[i+1], pairlist[i]
    
    #identifying runs of constant pairs (squares whose pipes have the same permutation indices)
    construns=[]
    temp=[-1,-1]
    for i in range (len(pairlist)-1):
        if ([pairlist[i][1], pairlist[i][2]]==[pairlist[i+1][1], pairlist[i+1][2]]):
            if ([pairlist[i][1],pairlist[i][2]]==temp):
                construns[-1].append(pairlist[i+1][0])
            else:
                construns.append([pairlist[i][0],pairlist[i+1][0]])
                temp=[pairlist[i][1], pairlist[i][2]]
    
    #generate candidates for changes
    changelist=[]
    for i in range (len(construns)):
        for j in range (len(construns[i])):
            for k in range (j+1,len(construns[i])):
                changelist.append((searchelement^^(2**(blocks-construns[i][j]-1)))^^(2**(blocks-construns[i][k]-1))) #bitwise flip the relevant bits
                #flipping both relevant bits is equivalent to either a double cross flip or a (possibly inverse) generalized chute move
    
    #adds the candidate if we haven't seen it before
    for i in range (len(changelist)):
        if (not (changelist[i] in foundlist or changelist[i] in searchlist)):
            searchlist.append(changelist[i])

#print(foundlist)
print(len(foundlist))
