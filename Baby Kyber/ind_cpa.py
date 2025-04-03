import secrets
import math
from scipy.stats import binomtest
from babyKyber import BabyKyber
from RingPolynom import RingPolynomOperations


def generate_kyber_instance(q, n, k, eta):
    """
    Initializes instances of the ring and the Baby Kyber encryption scheme.

    Parameters:
    - q: modulus of the ring
    - n: polynomial degree
    - k: matrix/vector dimension
    - eta: CBD noise parameter

    Returns:
    - kyber: instance of the BabyKyber class
    - ring: instance of the RingPolynomOperations class
    - A: public matrix of polynomials
    - t: public vector
    - s: secret key vector
    """
    ring = RingPolynomOperations(q, n)
    kyber = BabyKyber(n=n, eta=eta, k=k, q=q, ring=ring)
    A, t, s = kyber.key_gen(q, n, k, eta, ring)
    return kyber, ring, A, t, s


def calculate_score(ciphertext, q):
    """
    Computes a simple heuristic score for a ciphertext.

    The score is defined as the sum of the first coefficients of u[0] and v[0],
    reduced modulo q.

    Parameters:
    - ciphertext: tuple (u, v), where u is a list of polynomials and v is a polynomial
    - q: modulus of the ring

    Returns:
    - score: integer value representing the ciphertext signature
    """
    u, v = ciphertext
    return (u[0][0] + v[0]) % q


def attacker_guess(score_star, score_c0, score_c1):
    """
    Makes a guess for the challenge bit based on ciphertext similarity.

    The function compares the challenge ciphertext score to two known
    reference scores (for messages m0 and m1), and guesses the message
    corresponding to the closest score.

    Parameters:
    - score_star: score of the challenge ciphertext
    - score_c0: score of the ciphertext for message m0
    - score_c1: score of the ciphertext for message m1

    Returns:
    - guess: integer (0 or 1), representing the adversary's guess of bit b
    """
    dist_to_c0 = abs(score_star - score_c0)
    dist_to_c1 = abs(score_star - score_c1)
    return 0 if dist_to_c0 < dist_to_c1 else 1


def run_ind_cpa_experiment(q=97, n=4, k=2, eta=1, rounds=10000):
    """
    Runs an IND-CPA experiment against Baby Kyber using a basic adaptive strategy.

    The adversary performs encryption queries, analyzes patterns,
    and tries to distinguish between encryptions of two chosen messages.

    Parameters:
    - q: modulus of the ring
    - n: polynomial degree
    - k: matrix/vector dimension
    - eta: CBD noise parameter
    - rounds: number of experiment repetitions
    """
    kyber, ring, A, t, s = generate_kyber_instance(q, n, k, eta)
    success = 0

    for _ in range(rounds):
        m0 = [0] * n
        m1 = [1] * n

        c0 = kyber.encrypt(A, t, m0, q, n, k, eta, ring)
        c1 = kyber.encrypt(A, t, m1, q, n, k, eta, ring)

        score_c0 = calculate_score(c0, q)
        score_c1 = calculate_score(c1, q)

        b = secrets.randbelow(2)
        m_b = m0 if b == 0 else m1
        c_star = kyber.encrypt(A, t, m_b, q, n, k, eta, ring)
        score_star = calculate_score(c_star, q)

        guess = attacker_guess(score_star, score_c0, score_c1)

        if guess == b:
            success += 1

    binomial_test = binomtest(success, n=rounds, p=0.5, alternative='two-sided')

    phat = success / rounds
    ci_margin = 1.96 * math.sqrt(phat * (1 - phat) / rounds)

    print("=" * 45)
    print("IND-CPA with adaptive attack strategy")
    print("=" * 45)
    print(f"Adversary success rate: {success}/{rounds}")
    print(f"Probability of guessing correctly: {success / rounds:.4f}")
    print(f"Advantage over random guessing: {abs(success / rounds - 0.5):.4f}")
    print("=" * 45)
    print(f"p-value (binomial test): {binomial_test.pvalue:.4f}")
    print(f"95% confidence interval: [{phat - ci_margin:.4f}, {phat + ci_margin:.4f}]")
    print("=" * 45)


if __name__ == "__main__":
    run_ind_cpa_experiment()
