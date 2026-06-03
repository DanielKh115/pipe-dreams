"""
gives a poset diagram of the pipe dreams corresponding to the same permutation. Black lines are double cross flips and red lines are generalized chute moves
"""

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from matplotlib.patches import Rectangle, Arc

preparser(false)


order=6
blocks=int(order*(order-1)/2)
scale=0.03
#best 0.03 for n=5
#     0.07 for n=4

#put the input pipe dream here
idlist=[32755]#randint(0,(2**blocks)-1)]
#put in the following for a random pipe dream
#    randint(0,(2**blocks)-1)]


foundlist=[]
searchlist=idlist.copy()
weightmin=blocks
weightmax=0
connectionlist=[]

def integertocoords (x):
    L=[]
    readstring=bin(x)[2:]
    readlength=len(readstring)
    pos=[order-1,0]
    for i in range(readlength):
        if (readstring[readlength-i-1]=="1"):
            L.append((pos[1],pos[0]-1))
        pos=(pos[0],pos[1]+1)
        if (pos[1]>order-pos[0]-1):
            pos=[pos[0]-1,0]
    return(L)

"""
pindex=34
x=triangularbase(pindex,order-1)

temp=0
xoffset=blocks-order+1
for i in range(order-1):
    for j in range(x[i]):
        temp+=2**(xoffset+j)
    xoffset-=order-i-2

"""
"""
def triangularbase(x,listlength):
    temp=x
    L=[]
    for i in range (listlength):
        L.append(temp//math.factorial(listlength-i))
        temp-=L[-1]*math.factorial(listlength-i)
    return L
"""

def draw_pipe_dream(ax, center, n, fillcolor, crosses,
                    tile_size=1.0,
                    pipe_lw=2,
                    border_lw=0.5):

    cx, cy = center

    # lower-left corner of whole triangular board
    x0 = cx - n * tile_size / 2
    y0 = cy - n * tile_size / 2

    for r in range(n):
        for c in range(n):

            if r + c >= n:
                continue

            x = x0 + c * tile_size
            y = y0 + (n - 1 - r) * tile_size

            # square boundary
            ax.add_patch(
                Rectangle(
                    (x, y),
                    tile_size,
                    tile_size,
                    facecolor=fillcolor,#"cyan" if weightparam == weightmin else ("grey" if weightparam == weightmax else (0,1-0.7*(weightparam-weightmin-1)/(weightmax-1-weightmin),0)),
                    edgecolor="black",
                    #fill=False,#
                    lw=border_lw,
                )
            )

            if (r, c) in crosses:

                # horizontal pipe
                ax.plot(
                    [x, x + tile_size],
                    [y + tile_size/2, y + tile_size/2],
                    color="black",
                    lw=pipe_lw
                )

                # vertical pipe
                ax.plot(
                    [x + tile_size/2, x + tile_size/2],
                    [y, y + tile_size],
                    color="black",
                    lw=pipe_lw
                )

            else:

                # left -> top
                ax.add_patch(
                    Arc(
                        (x, y + tile_size),
                        1 * tile_size,
                        1 * tile_size,
                        theta1=270,
                        theta2=360,
                        lw=pipe_lw
                    )
                )
                if (not r+c==n-1):
                    # bottom -> right
                    ax.add_patch(
                        Arc(
                            (x + tile_size, y),
                            1 * tile_size,
                            1 * tile_size,
                            theta1=90,
                            theta2=180,
                            lw=pipe_lw
                        )
                    )


def draw_weighted_connection_graph(
    data,
    weight_attraction=0.2,
):
    """
    data entries:
        [element, weight, black_connections, red_connections]

    weight_attraction:
        Strength of virtual edges joining nodes
        having the same weight.

        0.0 -> no weight grouping
        0.1 -> weak grouping
        0.3 -> moderate grouping
        1.0 -> strong grouping
    """

    # Graph actually displayed
    G = nx.Graph()

    weights = {}
    black_edges = set()
    red_edges = set()

    # Add nodes
    for element, weight, black_conns, red_conns in data:
        G.add_node(element)
        weights[element] = weight

    # Add real edges
    for element, weight, black_conns, red_conns in data:

        for neighbor in black_conns:
            edge = tuple(sorted((element, neighbor)))
            black_edges.add(edge)
            G.add_edge(*edge)

        for neighbor in red_conns:
            edge = tuple(sorted((element, neighbor)))
            red_edges.add(edge)
            G.add_edge(*edge)

    # --------------------------------------------------
    # Build a second graph used only for layout
    # --------------------------------------------------

    layout_graph = nx.Graph()

    # Copy all nodes
    layout_graph.add_nodes_from(G.nodes())

    # Real edges get weight 1
    for u, v in G.edges():
        layout_graph.add_edge(u, v, weight=1.0)

    # Group nodes by weight
    weight_groups = defaultdict(list)

    for node, w in weights.items():
        weight_groups[w].append(node)

    # Add virtual attraction edges
    for group in weight_groups.values():

        if len(group) < 2:
            continue

        for u, v in combinations(group, 2):

            if layout_graph.has_edge(u, v):
                # Strengthen an existing edge
                layout_graph[u][v]["weight"] += weight_attraction
            else:
                # Virtual edge
                layout_graph.add_edge(
                    u,
                    v,
                    weight=weight_attraction
                )

    # Compute layout
    pos = nx.spring_layout(
        layout_graph,
        weight="weight",
        iterations=1000,
    )
    
    
    
    node_colors = {
        node: (
            "cyan" if weights[node] == weightmin
            else (
                "grey" if weights[node] == weightmax
                else (
                    0,
                    1 - 0.7*(weights[node]-weightmin-1)/(weightmax-1-weightmin),
                    0
                )
            )
        )
        for node in G.nodes
    }

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------
    """
    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=node_colors,
#        if weight==0:
#            node_color="lightblue"
#        else:
#            node_color="cyan",
        node_size=300,
        edgecolors="black"
    )

    labels = {
        node: f"{node}"
        for node in G.nodes
    }

    nx.draw_networkx_labels(
        G,
        pos,
        labels,
        font_size=9
    )
    """
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edgelist=list(black_edges),
        edge_color="black",
        width=2
    )

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edgelist=list(red_edges),
        edge_color="red",
        width=2
    )
    
    """
    for v in G.nodes:
        x, y = pos[v]
        ax.plot(x, y, "bo")
    
    """
    
    for v in G.nodes:
        x, y = pos[v]
        draw_pipe_dream(
            ax,
            center=(x, y),
            n=order,
            fillcolor=node_colors[v],
            crosses=integertocoords(v),#G.nodes[v]["crosses"],
            tile_size=scale   # make small enough to fit
        )
    
    ax.set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    

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
    chutelist=[]
    for i in range (len(construns)):
        for j in range (len(construns[i])):
            for k in range (j+1,len(construns[i])):
                if ((int(searchstring[construns[i][j]])+int(searchstring[construns[i][k]]))%2==0):
                    changelist.append((searchelement^^(2**(blocks-construns[i][j]-1)))^^(2**(blocks-construns[i][k]-1))) #bitwise flip the relevant bits
                else:
                    chutelist.append((searchelement^^(2**(blocks-construns[i][j]-1)))^^(2**(blocks-construns[i][k]-1)))
                #flipping both relevant bits is equivalent to either a double cross flip or a (possibly inverse) generalized chute move
    
    length=0
    for i in range (blocks):
        length+=int(searchstring[i])
    #print("element: ",searchelement)
    #print("weight: ", length)
    #print("fliplist: ", changelist)
    #print("chutelist: ", chutelist, "\n")
    if (length<weightmin):
        weightmin=length
    if (length>weightmax):
        weightmax=length
    connectionlist.append([searchelement,length,changelist,chutelist])
    
    #adds the candidate if we haven't seen it before
    for i in range (len(changelist)):
        if (not (changelist[i] in foundlist or changelist[i] in searchlist)):
            searchlist.append(changelist[i])
    
    for i in range (len(chutelist)):
        if (not (chutelist[i] in foundlist or chutelist[i] in searchlist)):
            searchlist.append(chutelist[i])

#print(foundlist)`
print("total number: ", len(foundlist))
print("connection list: ", connectionlist)


if (len(foundlist)<50):
    draw_weighted_connection_graph(
        connectionlist,
        weight_attraction=0.3
    )
"""
draw_weighted_connection_graph(
    connectionlist,
    weight_attraction=0.3
)
"""
