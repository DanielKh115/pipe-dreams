from collections import deque
from typing import FrozenSet, Tuple, List, Iterable

Cell = Tuple[int, int]
PipeDream = FrozenSet[Cell]


def validate_permutation(w: List[int]) -> None:
    n = len(w)
    if sorted(w) != list(range(1, n + 1)):
        raise ValueError("w must be a permutation of 1, 2, ..., n")


#define the length of a permutation by its number of inversions
def inversion_length(w: List[int]) -> int:
    return sum(
        1
        for i in range(len(w))
        for j in range(i + 1, len(w))
        if w[i] > w[j]
    )

#we only care about crosses that are above the diagonal
def valid_cross_cell(r: int, c: int, n: int) -> bool:
    """
    useful crosses live in the staircase
    r + c <= n - 2, using 0-indexing.
    """
    return 0 <= r < n and 0 <= c < n and r + c <= n - 2


#Finds the top pipe dream of a permutation
def top_pipe_dream(w: List[int]) -> PipeDream:
    """
    Constructs D_top(w).

    In 1-indexed mathematical notation:
    D_top(w) has crosses in column j, rows 1 through n_j,
    where n_j counts how many larger values appear before j in w.
    """
    validate_permutation(w)
    n = len(w)

    pos = {value: i for i, value in enumerate(w)}  # 0-indexed position
    crosses = set()

    for value in range(1, n + 1):
        p = pos[value]
        count = sum(1 for i in range(p) if w[i] > value)

        # Put crosses at rows 0, 1, ..., count - 1 based on the value column.
        for r in range(count):
            c = value - 1
            if valid_cross_cell(r, c, n):
                crosses.add((r, c))

    return frozenset(crosses)


def pipe_word(D: PipeDream, n: int) -> List[int]:
    """
    Reads the reduced word from a pipe dream.

    scan rows from top to bottom,
    and inside each row scan right to left.
    A cross at 0-indexed position (r, c) contributes s_{r+c+1}.
    """
    word = []

    for r in range(n):
        for c in range(n - 1, -1, -1):
            if (r, c) in D:
                k = r + c + 1
                if not (1 <= k < n):
                    raise ValueError(f"Invalid cross at {(r, c)} gives s_{k}")
                word.append(k)

    return word


def pipe_permutation(D: PipeDream, n: int) -> Tuple[int, ...]:
    """
    Computes perm(D) by applying the simple transpositions
    read from the pipe dream.
    """
    p = list(range(1, n + 1))

    for k in pipe_word(D, n):
        # s_k swaps positions k and k+1 in 1-indexing,
        # so here it swaps indices k-1 and k.
        p[k - 1], p[k] = p[k], p[k - 1]

    return tuple(p)


def is_reduced_pipe_dream(D: PipeDream, n: int) -> bool:
    """
    A pipe dream is reduced exactly when the number of crosses
    equals the inversion length of its permutation.
    """
    w = list(pipe_permutation(D, n))
    return len(D) == inversion_length(w)


def chute_neighbors(D: PipeDream, n: int) -> Iterable[PipeDream]:
    """
    Generates ordinary chute moves.

    Pattern, schematically:

        . + + + +
        . + + + .

    becomes

        . + + + .
        + + + + .

    So a cross moves down and left.
    """
    Dset = set(D)

    for r, j in list(Dset):
        if r + 1 >= n:
            continue

        # Move the cross at (r, j) down-left to (r+1, m)
        # for some m < j.
        for m in range(j):
            target = (r + 1, m)

            if not valid_cross_cell(target[0], target[1], n):
                continue

            # Required empty endpoints.
            if target in Dset:
                continue
            if (r, m) in Dset:
                continue
            if (r + 1, j) in Dset:
                continue

            # Required filled middle rectangle/chute.
            ok = True
            for c in range(m + 1, j):
                if (r, c) not in Dset or (r + 1, c) not in Dset:
                    ok = False
                    break

            if not ok:
                continue

            newD = set(Dset)
            newD.remove((r, j))
            newD.add(target)

            yield frozenset(newD)


def all_reduced_pipe_dreams(w: List[int]) -> List[PipeDream]:
    """
    BFS from D_top(w), using chute moves. This should cover all pipe dreams that give the same permutation
    """
    validate_permutation(w)
    n = len(w)
    target = tuple(w)

    start = top_pipe_dream(w)
    seen = {start}
    queue = deque([start])

    while queue:
        D = queue.popleft()

        for E in chute_neighbors(D, n):
            if E in seen:
                continue

        
            seen.add(E)
            queue.append(E)

    return list(seen)


def to_matrix(D: PipeDream, n: int) -> List[List[int]]:
    return [
        [1 if (r, c) in D else 0 for c in range(n)]
        for r in range(n)
    ]


def print_pipe_dream(D: PipeDream, n: int) -> None:
    """
    Pretty-print only the triangular staircase part.
    """
    for r in range(n - 1):
        row = []
        for c in range(n - 1 - r):
            row.append("+" if (r, c) in D else ".")
        print(" ".join(row))


def monomial_exponents(D: PipeDream, n: int) -> Tuple[int, ...]:
    """
    The monomial of a pipe dream is product x_row over crosses.
    This returns the exponent vector.
    """
    return tuple(
        sum(1 for c in range(n) if (r, c) in D)
        for r in range(n)
    )