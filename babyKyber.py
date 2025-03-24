import math
import secrets as sc


class BabyKyber:
    def __init__(self, n, eta, k, q, ring):
        self.n = n
        self.eta = eta
        self.k = k
        self.q = q
        self.ring = ring

    @staticmethod
    def sample_uniform_polynomial(q, degree):
        """
        Samples a uniform random polynomial in Z_q[X] with degree at most `degree`.

        Each coefficient is sampled uniformly at random from the range [0, q - 1].

        Parameters:
            q (int): The modulus of the polynomial ring (coefficients are in Z_q).
            degree (int): The maximum degree of the polynomial.

        Returns:
            List[int]: A list of coefficients representing the polynomial, length (degree + 1).
        """
        return [sc.randbelow(q) for _ in range(degree + 1)]

    @staticmethod
    def sample_cbd_polynomial(n, eta, ring):
        """
        Samples a polynomial with coefficients from a centered binomial distribution (CBD).

        Each coefficient is computed as the difference between two samples from a uniform
        distribution over the integers in [0, eta]. The result is then reduced modulo (X^n + 1).

        Parameters:
            n (int): The number of coefficients in the polynomial (usually degree + 1).
            eta (int): The parameter controlling the noise distribution (larger eta = more noise).
            ring (RingPolynomOperations): An instance that provides the module reduction for polynomials.

        Returns:
            List[int]: A reduced polynomial of length `n` with coefficients in Z_q.
        """

        coefficients = []

        for _ in range(n):
            a = sc.choice(range(eta + 1))  # uniform random in [0, eta]
            b = sc.choice(range(eta + 1))  # uniform random in [0, eta]
            coefficients.append(a - b)  # CBD sample: centered around 0

        return ring.module(coefficients)

    def key_gen(self, q, n, k, eta, ring):
        """
        Key Generation for Baby Kyber.

        Parameters:
        - q: modulus
        - n: polynomial degree (usually degree + 1 in polynomials)
        - k: matrix dimension
        - eta: CBD parameter (controls noise distribution)
        - ring: an instance of RingPolynomOperations handling polynomial arithmetic

        Returns:
        - A: public matrix of uniformly random polynomials in Z_q[X]/(X^n + 1)
        - t: public vector, computed as A * s + e
        - s: secret vector with small polynomials
        """

        A = [
            [self.sample_uniform_polynomial(q, n) for _ in range(k)]
            for _ in range(k)
        ]

        s = [self.sample_cbd_polynomial(n, eta, ring) for _ in range(k)]
        e = [self.sample_cbd_polynomial(n, eta, ring) for _ in range(k)]

        t = []
        for i in range(k):
            row_sum = [0]

            for j in range(k):
                row_sum = ring.add(row_sum, ring.multiply(A[i][j], s[j]))

            t_i = ring.add(row_sum, e[i])
            t.append(t_i)

        return A, t, s

    def encrypt(self, A, t, m_bits, q, n, k, eta, ring):
        """
        Encrypt a message using the public key (A, t).

        Parameters:
        - A: public matrix of size k x k
        - t: public vector of size k
        - m_bits: message polynomial (list of bits, length n)
        - q: modulus
        - n: polynomial degree (number of coefficients per polynomial)
        - k: matrix dimension
        - eta: CBD parameter for noise generation
        - ring: an instance of RingPolynomOperations

        Returns:
        - u: ciphertext component (vector of size k)
        - v: ciphertext component (polynomial)
        """

        r = [self.sample_cbd_polynomial(n, eta, ring) for _ in range(k)]
        e1 = [self.sample_cbd_polynomial(n, eta, ring) for _ in range(k)]
        e2 = self.sample_cbd_polynomial(n, eta, ring)

        A_T = [[A[j][i] for j in range(k)] for i in range(k)]

        u = []
        for i in range(k):
            row_sum = [0]

            for j in range(k):
                row_sum = ring.add(row_sum, ring.multiply(A_T[i][j], r[j]))

            u_i = ring.add(row_sum, e1[i])
            u.append(u_i)

        v = e2.copy()

        for i in range(k):
            v = ring.add(v, ring.multiply(t[i], r[i]))

        m_scaled = [coeff * math.ceil(q / 2) for coeff in m_bits]
        v = ring.add(v, m_scaled)

        return u, v

    @staticmethod
    def decrypt(c, s, q, k, ring):
        """
        Decrypt a ciphertext (u, v) using the secret key s.

        Parameters:
        - c: ciphertext tuple (u, v)
        - s: secret key vector of polynomials
        - q: modulus
        - k: matrix/vector dimension
        - ring: an instance of RingPolynomOperations for polynomial arithmetic

        Returns:
        - m_decoded: list of bits recovered from decryption
        """

        u, v = c

        sTu = [0]
        for i in range(k):
            sTu = ring.add(sTu, ring.multiply(u[i], s[i]))

        decrypted = ring.add(v, ring.multiply(sTu, [-1]))

        m_decoded = []
        for coeff in decrypted:
            c_mod = coeff % ring.mod

            lower_bound = (q // 2) - (q // 4)
            upper_bound = (q // 2) + (q // 4)

            if lower_bound <= c_mod <= upper_bound:
                m_decoded.append(1)
            else:
                m_decoded.append(0)

        return m_decoded
