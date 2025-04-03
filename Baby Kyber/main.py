from RingPolynom import RingPolynomOperations
from babyKyber import BabyKyber


def text_to_bits(text):
    """
    Converts a UTF-8 encoded string into a list of bits.

    Parameters:
    - text: input string

    Returns:
    - bits: list of bits (integers 0 or 1), each representing a bit in the UTF-8 encoding of the text
    """

    byte_data = text.encode('utf-8')

    bits = []
    for c in byte_data:
        bits.extend([(c >> i) & 1 for i in reversed(range(8))])

    return bits


def bits_to_text(bits):
    """
    Converts a list of bits into a UTF-8 string.

    Parameters:
    - bits: list of bits (integers 0 or 1), representing binary data

    Returns:
    - text: UTF-8 decoded string reconstructed from bits
    """

    bytes_list = []

    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) < 8:
            byte_bits += [0] * (8 - len(byte_bits))

        byte_val = 0
        for bit in byte_bits:
            byte_val = (byte_val << 1) | bit

        bytes_list.append(byte_val)

    return bytes(bytes_list).decode('utf-8', errors='ignore')


def encrypt_text(A, t, bits, q, n, k, eta, ring, baby_kyber):
    """
    Encrypts a list of bits (message) by breaking them into chunks and encrypting each chunk.

    Parameters:
    - A: public matrix (k x k) of polynomials
    - t: public vector of polynomials
    - bits: list of bits representing the message
    - q: modulus
    - n: number of coefficients per polynomial (chunk size)
    - k: matrix/vector dimension
    - eta: CBD noise parameter
    - ring: instance of RingPolynomOperations

    Returns:
    - ciphertext: list of ciphertext tuples (u, v)
    """

    ciphertext = []
    for i in range(0, len(bits), n):
        chunk = bits[i:i + n]

        if len(chunk) < n:
            chunk += [0] * (n - len(chunk))

        c = BabyKyber.encrypt(baby_kyber, A, t, chunk, q, n, k, eta, ring)
        ciphertext.append(c)

    return ciphertext


def decrypt_text(ciphertext, s, q, k, ring):
    """
    Decrypts a list of ciphertext tuples and reconstructs the original text.

    Parameters:
    - ciphertext: list of ciphertext tuples (u, v)
    - s: secret key vector of polynomials
    - q: modulus
    - k: matrix/vector dimension
    - ring: instance of RingPolynomOperations

    Returns:
    - text: the decrypted string recovered from the ciphertext
    """

    bits = []
    for c in ciphertext:
        decrypted_bits = BabyKyber.decrypt(c, s, q, k, ring)
        bits.extend(decrypted_bits)

    return bits_to_text(bits)


def main():
    # PARAMETERS
    q, n, k, eta = 97, 4, 2, 1
    ring = RingPolynomOperations(q, n)
    baby_kyber = BabyKyber(n, eta, k, q, ring)

    # KEY GENERATION
    print("=" * 40)
    print("🔑  KEY GENERATION")
    print("=" * 40)

    A, t, s = BabyKyber.key_gen(baby_kyber, q, n, k, eta, ring)

    print(f"Public Key Matrix A:\n{A}\n")
    print(f"Public Key Vector t:\n{t}\n")
    # print(f"Secret Key Vector s (kept secret):\n{s}\n")

    # MESSAGE PREPARATION
    message = 'yegfiqjeof 6e87f9q fedgikafq gueyqt737 gfq fuiqtr8$%$%^$&^*% %&^DFUV %&^* '
    bits = text_to_bits(message)

    print("=" * 40)
    print("✉️  MESSAGE PREPARATION")
    print("=" * 40)

    print(f"Original Message:\n\t{message}\n")
    print(f"Message in bits:\n\t{bits}\n")

    # ENCRYPTION
    ciphertext = encrypt_text(A, t, bits, q, n, k, eta, ring, baby_kyber)

    print("=" * 40)
    print("🔒  ENCRYPTION")
    print("=" * 40)

    print(f"Ciphertext:\n\t{ciphertext}\n")

    # DECRYPTION
    decrypted_message = decrypt_text(ciphertext, s, q, k, ring)

    print("=" * 40)
    print("🔓  DECRYPTION")
    print("=" * 40)

    print(f"Decrypted Message:\n\t{decrypted_message}\n")

    # VALIDATION
    print("=" * 40)
    print("✅  RESULT")
    print("=" * 40)

    if message == decrypted_message:
        print("🎉 SUCCESS: The message was sent successfully! 🎉")
    else:
        print("❌ ERROR: The message was sent unsuccessfully ❌")
        print(f"Expected: {message}")
        print(f"Got     : {decrypted_message}")


if __name__ == '__main__':
    main()
