import math
import secrets
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

    Parameters:
    - ciphertext: tuple (u, v), where u is a list of polynomials and v is a polynomial
    - q: modulus of the ring

    Returns:
    - score: integer value representing the ciphertext signature
    """
    u, v = ciphertext
    return (u[0][0] + v[0]) % q


def decrypt_oracle(kyber, s, q, k, ring, challenge_ciphertext):
    """
    Returns a decryption oracle function that forbids decryption of the challenge ciphertext.

    Parameters:
    - kyber: instance of BabyKyber
    - s: secret key vector
    - q: modulus
    - k: matrix/vector dimension
    - ring: ring operations
    - challenge_ciphertext: the ciphertext c* that is not allowed to be queried

    Returns:
    - oracle: function(ciphertext) that returns decryption if allowed
    """
    def oracle(c):
        if c == challenge_ciphertext:
            raise ValueError("Decryption of challenge ciphertext is forbidden!")
        return kyber.decrypt(c, s, q, k, ring)
    return oracle


def attacker_guess_cca_with_oracle(c_star, decrypt_oracle_, q):
    """
    Uses the decryption oracle to distinguish which message was encrypted in c*.

    Strategy:
    - Modify v* slightly (add a known offset)
    - Decrypt the modified ciphertext
    - If the result is closer to [1,...,1], guess m1; else guess m0

    Parameters:
    - c_star: challenge ciphertext (u, v)
    - decrypt_oracle: callable D(c), which forbids c == c*
    - q: modulus

    Returns:
    - guess: 0 or 1
    """
    u, v = c_star
    delta = [1] + [0] * (len(v) - 1)
    v_modified = [(vi + di) % q for vi, di in zip(v, delta)]
    c_modified = (u, v_modified)

    try:
        m_dec = decrypt_oracle_(c_modified)
    except ValueError:
        return secrets.randbelow(2)

    threshold = sum(m_dec)
    return 1 if threshold >= len(m_dec) // 2 else 0


def run_ind_cca_experiment(q=97, n=4, k=2, eta=1, rounds=10000):
    """
    Runs an IND-CCA experiment against Baby Kyber.

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

        b = secrets.randbelow(2)
        m_b = m0 if b == 0 else m1
        c_star = kyber.encrypt(A, t, m_b, q, n, k, eta, ring)

        oracle = decrypt_oracle(kyber, s, q, k, ring, c_star)

        guess = attacker_guess_cca_with_oracle(c_star, oracle, q)
        if guess == b:
            success += 1

    binomial_test = binomtest(success, n=rounds, p=0.5, alternative='two-sided')
    phat = success / rounds
    ci_margin = 1.96 * math.sqrt(phat * (1 - phat) / rounds)

    print("=" * 45)
    print("IND-CCA experiment (basic attack strategy)")
    print("=" * 45)
    print(f"Adversary success rate: {success}/{rounds}")
    print(f"Probability of guessing correctly: {phat:.4f}")
    print(f"Advantage over random guessing: {abs(phat - 0.5):.4f}")
    print("=" * 45)
    print(f"p-value (binomial test): {binomial_test.pvalue:.4f}")
    print(f"95% confidence interval: [{phat - ci_margin:.4f}, {phat + ci_margin:.4f}]")
    print("=" * 45)


if __name__ == "__main__":
    run_ind_cca_experiment()
