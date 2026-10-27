from copy import deepcopy


class MatrixMath:
    """
    Pure mathematical matrix operations.

    All methods accept and return standard Python lists.
    No Manim dependency.
    """

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _validate(matrix):
        """Validate that input is a proper rectangular matrix."""

        if not isinstance(matrix, list) or len(matrix) == 0:
            raise ValueError("Matrix must be a non-empty list.")

        row_length = len(matrix[0])

        if row_length == 0:
            raise ValueError("Matrix cannot have empty rows.")

        for row in matrix:
            if not isinstance(row, list):
                raise ValueError("Each row must be a list.")

            if len(row) != row_length:
                raise ValueError("Matrix rows must all have the same length.")

            for value in row:
                if not isinstance(value, (int, float)):
                    raise ValueError("Matrix values must be numeric.")

    @staticmethod
    def _shape(matrix):
        MatrixMath._validate(matrix)
        return len(matrix), len(matrix[0])

    @staticmethod
    def _same_shape(A, B):

        if MatrixMath._shape(A) != MatrixMath._shape(B):
            raise ValueError("Matrices must have the same dimensions.")

    @staticmethod
    def _can_multiply(A, B):

        rows_a, cols_a = MatrixMath._shape(A)
        rows_b, cols_b = MatrixMath._shape(B)

        if cols_a != rows_b:
            raise ValueError(
                "Number of columns of first matrix must equal number of rows of second matrix."
            )

    # ---------------------------------------------------------
    # Matrix Creation
    # ---------------------------------------------------------

    @staticmethod
    def zeros(rows, cols):

        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive.")

        return [[0 for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def identity(size):

        if size <= 0:
            raise ValueError("Size must be positive.")

        matrix = MatrixMath.zeros(size, size)

        for i in range(size):
            matrix[i][i] = 1

        return matrix

    # ---------------------------------------------------------
    # Matrix Information
    # ---------------------------------------------------------

    @staticmethod
    def shape(matrix):
        return MatrixMath._shape(matrix)

    # ---------------------------------------------------------
    # Basic Operations
    # ---------------------------------------------------------

    @staticmethod
    def add(A, B):

        MatrixMath._same_shape(A, B)

        rows, cols = MatrixMath._shape(A)

        result = MatrixMath.zeros(rows, cols)

        for i in range(rows):
            for j in range(cols):
                result[i][j] = A[i][j] + B[i][j]

        return result

    @staticmethod
    def subtract(A, B):

        MatrixMath._same_shape(A, B)

        rows, cols = MatrixMath._shape(A)

        result = MatrixMath.zeros(rows, cols)

        for i in range(rows):
            for j in range(cols):
                result[i][j] = A[i][j] - B[i][j]

        return result

    @staticmethod
    def scalar_multiply(matrix, scalar):

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        result = MatrixMath.zeros(rows, cols)

        for i in range(rows):
            for j in range(cols):
                result[i][j] = matrix[i][j] * scalar

        return result

    @staticmethod
    def transpose(matrix):

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        result = MatrixMath.zeros(cols, rows)

        for i in range(rows):
            for j in range(cols):
                result[j][i] = matrix[i][j]

        return result

    @staticmethod
    def multiply(A, B):

        MatrixMath._can_multiply(A, B)

        rows_a, cols_a = MatrixMath._shape(A)
        rows_b, cols_b = MatrixMath._shape(B)

        result = MatrixMath.zeros(rows_a, cols_b)

        for i in range(rows_a):
            for j in range(cols_b):

                total = 0

                for k in range(cols_a):
                    total += A[i][k] * B[k][j]

                result[i][j] = total

        return result

    @staticmethod
    def trace(matrix):

        rows, cols = MatrixMath._shape(matrix)

        if rows != cols:
            raise ValueError("Trace is defined only for square matrices.")

        total = 0

        for i in range(rows):
            total += matrix[i][i]

        return total

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def copy(matrix):

        MatrixMath._validate(matrix)

        return deepcopy(matrix)



    # ---------------------------------------------------------
    # Matrix V2
    # ---------------------------------------------------------

    @staticmethod
    def _submatrix(matrix, remove_row, remove_col):
        """
        Returns a new matrix after removing one row and one column.
        """

        MatrixMath._validate(matrix)

        result = []

        for i, row in enumerate(matrix):

            if i == remove_row:
                continue

            new_row = []

            for j, value in enumerate(row):

                if j == remove_col:
                    continue

                new_row.append(value)

            result.append(new_row)

        return result

    @staticmethod
    def determinant(matrix):
        """
        Compute the determinant of a square matrix.
        Supports any square matrix using recursive Laplace expansion.
        """

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        if rows != cols:
            raise ValueError(
                "Determinant is defined only for square matrices."
            )

        # -----------------------------
        # 1 × 1
        # -----------------------------
        if rows == 1:
            return matrix[0][0]

        # -----------------------------
        # 2 × 2
        # -----------------------------
        if rows == 2:

            return (
                matrix[0][0] * matrix[1][1]
                - matrix[0][1] * matrix[1][0]
            )

        # -----------------------------
        # Recursive Laplace Expansion
        # -----------------------------
        det = 0

        for col in range(cols):

            sign = (-1) ** col

            sub = MatrixMath._submatrix(
                matrix,
                0,
                col,
            )

            det += (
                sign
                * matrix[0][col]
                * MatrixMath.determinant(sub)
            )

        return det


    @staticmethod
    def minor(matrix):
        """
        Compute the minor matrix.
        """

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        if rows != cols:
            raise ValueError(
                "Minor is defined only for square matrices."
            )

        result = MatrixMath.zeros(rows, cols)

        for i in range(rows):
            for j in range(cols):

                sub = MatrixMath._submatrix(
                    matrix,
                    i,
                    j,
                )

                result[i][j] = MatrixMath.determinant(sub)

        return result



    @staticmethod
    def cofactor(matrix):
        """
        Compute the cofactor matrix.
        """

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        if rows != cols:
            raise ValueError(
                "Cofactor is defined only for square matrices."
            )

        minors = MatrixMath.minor(matrix)

        result = MatrixMath.zeros(rows, cols)

        for i in range(rows):
            for j in range(cols):

                sign = (-1) ** (i + j)

                result[i][j] = sign * minors[i][j]

        return result



    @staticmethod
    def adjoint(matrix):
        """
        Compute the adjoint (adjugate) matrix.
        """

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        if rows != cols:
            raise ValueError(
                "Adjoint is defined only for square matrices."
            )

        return MatrixMath.transpose(
            MatrixMath.cofactor(matrix)
        )



    @staticmethod
    def inverse(matrix):
        """
        Compute the inverse of a square matrix.
        """

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        if rows != cols:
            raise ValueError(
                "Inverse is defined only for square matrices."
            )

        det = MatrixMath.determinant(matrix)

        if det == 0:
            raise ValueError(
                "Singular matrix has no inverse."
            )

        adj = MatrixMath.adjoint(matrix)

        return MatrixMath.scalar_multiply(
            adj,
            1 / det
        )


    @staticmethod
    def swap_rows(matrix, row1, row2):
        """
        Return a new matrix with two rows swapped.
        """

        MatrixMath._validate(matrix)

        rows, _ = MatrixMath._shape(matrix)

        if not (0 <= row1 < rows and 0 <= row2 < rows):
            raise IndexError("Row index out of range.")

        result = MatrixMath.copy(matrix)

        result[row1], result[row2] = (
            result[row2],
            result[row1],
        )

        return result


    @staticmethod
    def scale_row(matrix, row, scalar):
        """
        Multiply one row by a scalar.
        """

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        if not (0 <= row < rows):
            raise IndexError("Row index out of range.")

        result = MatrixMath.copy(matrix)

        for j in range(cols):
            result[row][j] *= scalar

        return result



    @staticmethod
    def add_scaled_row(
        matrix,
        source_row,
        target_row,
        scalar,
    ):
        """
        target_row = target_row + scalar × source_row
        """

        MatrixMath._validate(matrix)

        rows, cols = MatrixMath._shape(matrix)

        if not (
            0 <= source_row < rows
            and 0 <= target_row < rows
        ):
            raise IndexError("Row index out of range.")

        result = MatrixMath.copy(matrix)

        for j in range(cols):
            result[target_row][j] += (
                scalar * result[source_row][j]
            )

        return result



    @staticmethod
    def gaussian_elimination(matrix):
        """
        Convert a matrix to Row Echelon Form (REF)
        using Gaussian Elimination.
        """

        MatrixMath._validate(matrix)

        result = MatrixMath.copy(matrix)

        rows, cols = MatrixMath._shape(result)

        pivot_row = 0

        for pivot_col in range(cols):

            if pivot_row >= rows:
                break

            # Find pivot
            max_row = None

            for r in range(pivot_row, rows):
                if result[r][pivot_col] != 0:
                    max_row = r
                    break

            if max_row is None:
                continue

            # Swap rows if necessary
            if max_row != pivot_row:
                result = MatrixMath.swap_rows(
                    result,
                    pivot_row,
                    max_row,
                )

            pivot = result[pivot_row][pivot_col]

            # Eliminate rows below
            for r in range(pivot_row + 1, rows):

                if result[r][pivot_col] == 0:
                    continue

                factor = (
                    result[r][pivot_col]
                    / pivot
                )

                result = MatrixMath.add_scaled_row(
                    result,
                    pivot_row,
                    r,
                    -factor,
                )

            pivot_row += 1

        return result


    @staticmethod
    def ref(matrix, tolerance=1e-10):
        """
        Convert a matrix to Row Echelon Form (REF).
        Small floating-point values are rounded to zero.
        """

        result = MatrixMath.gaussian_elimination(matrix)

        rows, cols = MatrixMath._shape(result)

        for i in range(rows):
            for j in range(cols):

                if abs(result[i][j]) < tolerance:
                    result[i][j] = 0

        return result



    @staticmethod
    def rref(matrix, tolerance=1e-10):
        """
        Convert a matrix to Reduced Row Echelon Form (RREF).
        """

        MatrixMath._validate(matrix)

        result = MatrixMath.copy(matrix)

        rows, cols = MatrixMath._shape(result)

        pivot_row = 0

        for pivot_col in range(cols):

            if pivot_row >= rows:
                break

            # Find pivot
            pivot = None

            for r in range(pivot_row, rows):
                if abs(result[r][pivot_col]) > tolerance:
                    pivot = r
                    break

            if pivot is None:
                continue

            # Swap rows
            if pivot != pivot_row:
                result = MatrixMath.swap_rows(
                    result,
                    pivot,
                    pivot_row
                )

            # Normalize pivot row
            pivot_value = result[pivot_row][pivot_col]

            result = MatrixMath.scale_row(
                result,
                pivot_row,
                1 / pivot_value
            )

            # Eliminate every other row
            for r in range(rows):

                if r == pivot_row:
                    continue

                factor = result[r][pivot_col]

                if abs(factor) > tolerance:

                    result = MatrixMath.add_scaled_row(
                        result,
                        pivot_row,
                        r,
                        -factor
                    )

            pivot_row += 1

        # Clean floating-point errors
        for i in range(rows):
            for j in range(cols):

                if abs(result[i][j]) < tolerance:
                    result[i][j] = 0

        return result



    @staticmethod
    def rank(matrix, tolerance=1e-10):
        """
        Compute the rank of a matrix.
        """

        MatrixMath._validate(matrix)

        rref_matrix = MatrixMath.rref(matrix, tolerance)

        rank = 0

        for row in rref_matrix:

            if any(abs(value) > tolerance for value in row):
                rank += 1

        return rank

    