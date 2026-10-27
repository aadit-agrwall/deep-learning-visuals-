from components.matrix_math import MatrixMath


def main():

    A = [
        [1, 2],
        [3, 4]
    ]

    B = [
        [5, 6],
        [7, 8]
    ]

    print("\nDeterminant of A:")
    print(MatrixMath.determinant(A))

    # -------------------------------------------------
    # Determinant (1x1)
    # -------------------------------------------------

    D = [
        [6]
    ]

    print("\nDeterminant (1x1):")
    print(MatrixMath.determinant(D))

    # -------------------------------------------------
    # Determinant (2x2)
    # -------------------------------------------------

    E = [
        [1, 2],
        [3, 4]
    ]

    print("\nDeterminant (2x2):")
    print(MatrixMath.determinant(E))

    # -------------------------------------------------
    # Determinant (3x3)
    # -------------------------------------------------

    F = [
        [6, 1, 1],
        [4, -2, 5],
        [2, 8, 7]
    ]

    print("\nDeterminant (3x3):")
    print(MatrixMath.determinant(F))


    
    # -------------------------------------------------
    # Cofactor
    # -------------------------------------------------

    print("\nCofactor Matrix:")

    cofactor = MatrixMath.cofactor(F)

    for row in cofactor:
        print(row)

    # -------------------------------------------------
    # Adjoint
    # -------------------------------------------------

    print("\nAdjoint Matrix:")

    adj = MatrixMath.adjoint(F)

    for row in adj:
        print(row)    

    # -------------------------------------------------
    # Determinant (4x4)
    # -------------------------------------------------

    G = [
        [3, 2, 0, 1],
        [4, 0, 1, 2],
        [3, 0, 2, 1],
        [9, 2, 3, 1]
    ]

    print("\nDeterminant (4x4):")
    print(MatrixMath.determinant(G))

    # -------------------------------------------------
    # Inverse
    # -------------------------------------------------

    print("\nInverse Matrix:")

    inv = MatrixMath.inverse(E)

    for row in inv:
        print(row)


    # -------------------------------------------------
    # Row Operations
    # -------------------------------------------------

    H = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    print("\nOriginal Matrix:")
    for row in H:
        print(row)

    print("\nSwap Row 0 and Row 2:")
    for row in MatrixMath.swap_rows(H, 0, 2):
        print(row)

    print("\nScale Row 1 by 3:")
    for row in MatrixMath.scale_row(H, 1, 3):
        print(row)

    print("\nRow2 = Row2 - 2 × Row0:")
    for row in MatrixMath.add_scaled_row(H, 0, 2, -2):
        print(row)


    # -------------------------------------------------
    # Gaussian Elimination
    # -------------------------------------------------

    J = [
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ]

    print("\nGaussian Elimination:")

    ref = MatrixMath.gaussian_elimination(J)

    for row in ref:
        print(row)



    # -------------------------------------------------
    # REF
    # -------------------------------------------------

    print("\nRow Echelon Form:")

    ref = MatrixMath.ref(J)

    for row in ref:
        print(row)   



    # -------------------------------------------------
    # RREF
    # -------------------------------------------------

    print("\nReduced Row Echelon Form:")

    rref = MatrixMath.rref(J)

    for row in rref:
        print(row)     


    # -------------------------------------------------
    # Rank
    # -------------------------------------------------

    print("\nRank of J:")
    print(MatrixMath.rank(J))

    K = [
        [1, 2],
        [2, 4]
    ]

    print("\nRank of K:")
    print(MatrixMath.rank(K))          

if __name__ == "__main__":
    main()