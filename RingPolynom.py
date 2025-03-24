class RingPolynomOperations:
    def __init__(self, mod, n):
        self.mod = mod
        self.n = n

    def add(self, p1, p2):
        """
        Adds two polynomials p1 and p2 in Z_q[X] / (X^n + 1).

        Parameters:
        - p1: list of coefficients (first polynomial)
        - p2: list of coefficients (second polynomial)

        Returns:
        - result: reduced polynomial representing (p1 + p2) mod (X^n + 1), coeff mod q
        """

        max_len = max(len(p1), len(p2))

        p1_extended = p1 + [0] * (max_len - len(p1))
        p2_extended = p2 + [0] * (max_len - len(p2))

        result = [(a + b) % self.mod for a, b in zip(p1_extended, p2_extended)]

        return self.module(result)

    def multiply(self, p1, p2):
        """
        Multiplies two polynomials p1 and p2 in Z_q[X] / (X^n + 1).

        Parameters:
        - p1: list of coefficients (first polynomial)
        - p2: list of coefficients (second polynomial)

        Returns:
        - result: reduced polynomial representing (p1 * p2) mod (X^n + 1), coeff mod q
        """

        result_length = len(p1) + len(p2) - 1
        result = [0] * result_length

        for i, a in enumerate(p1):
            for j, b in enumerate(p2):
                result[i + j] = (result[i + j] + a * b) % self.mod

        return self.module(result)

    def module(self, poly):
        """
        Reduces a polynomial modulo (X^n + 1) and modulo q.

        Parameters:
        - poly: list of coefficients representing the polynomial to be reduced

        Returns:
        - reduced: list of coefficients of degree < n, each reduced modulo q
        """

        if len(poly) >= self.n:
            reduced = poly[:self.n]
        else:
            reduced = poly + [0] * (self.n - len(poly))

        reduced = reduced[:self.n]

        for i in range(self.n, len(poly)):
            coeff = poly[i]
            power = i // self.n
            rem = i % self.n

            reduced[rem] = (reduced[rem] + (-1) ** power * coeff) % self.mod

        return [c % self.mod for c in reduced]
