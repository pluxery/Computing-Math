from typing import Tuple, List
import bisect


class Spline:

    @classmethod
    def __diffs(cls, x: List[float]) -> List[float]:
        return [x[i + 1] - x[i] for i in range(len(x) - 1)]

    @classmethod
    def __create_tridiagonal_matrix(cls, n: int, h: List[float]) -> Tuple[List[float], List[float], List[float]]:
        A = [h[i] / (h[i] + h[i + 1]) for i in range(n - 2)] + [0]
        B = [2] * n
        C = [0] + [h[i + 1] / (h[i] + h[i + 1]) for i in range(n - 2)]
        return A, B, C

    @classmethod
    def __create_target(cls, n: int, h: List[float], y: List[float]):
        return [0] + [6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]) / (h[i] + h[i - 1]) for i in
                      range(1, n - 1)] + [0]

    @classmethod
    def __solve_system(cls, A: List[float], B: List[float], C: List[float], D: List[float]):
        c_p = C + [0]
        d_p = [0] * len(B)
        X = [0] * len(B)

        c_p[0] = C[0] / B[0]
        d_p[0] = D[0] / B[0]
        for i in range(1, len(B)):
            c_p[i] = c_p[i] / (B[i] - c_p[i - 1] * A[i - 1])
            d_p[i] = (D[i] - d_p[i - 1] * A[i - 1]) / (B[i] - c_p[i - 1] * A[i - 1])

        X[-1] = d_p[-1]
        for i in range(len(B) - 2, -1, -1):
            X[i] = d_p[i] - c_p[i] * X[i + 1]

        return X

    @classmethod
    def compute_spline(cls, x: List[float], y: List[float]):
        n = len(x)
        if n < 3:
            raise ValueError('массив слишком короткий')
        if n != len(y):
            raise ValueError('размеры массивов не равны')

        h = cls.__diffs(x)
        if any(v < 0 for v in h):
            raise ValueError('h =< 0')

        A, B, C = cls.__create_tridiagonal_matrix(n, h)
        D = cls.__create_target(n, h, y)

        M = cls.__solve_system(A, B, C, D)

        coefficients = [[(M[i + 1] - M[i]) * h[i] * h[i] / 6, M[i] * h[i] * h[i] / 2,
                         (y[i + 1] - y[i] - (M[i + 1] + 2 * M[i]) * h[i] * h[i] / 6), y[i]] for i in range(n - 1)]

        def spline(val):
            idx = min(bisect.bisect(x, val) - 1, n - 2)
            z = (val - x[idx]) / h[idx]
            C = coefficients[idx]
            return (((C[0] * z) + C[1]) * z + C[2]) * z + C[3]

        return spline
