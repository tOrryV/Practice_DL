
# 📌 Baby Kyber — A Simplified Lattice-Based Cryptographic Scheme

This repository contains an **educational, simplified implementation** of the **Baby Kyber** encryption scheme. It is based on **lattice-based cryptography** principles and mimics the core mechanics of the **Kyber PKE** (Public Key Encryption) system, which is part of the **NIST PQC Kyber KEM** standard. The parameters are deliberately kept small for easier understanding and learning.


## ⚙️ Components

The implementation consists of three modules:
--------------------------------------------------------------------------------------------------------------------------------------
| File             | Description                                                                                                     |
|------------------|-----------------------------------------------------------------------------------------------------------------|
| `main.py`        | Entry point. Demonstrates key generation, message encryption, and decryption workflows.                         |
| `babyKyber.py`   | Contains the core **Baby Kyber** cryptographic scheme: key generation, encryption, decryption.                  |
| `RingPolynom.py` | Provides polynomial arithmetic operations in the ring `Z_q[X]/(X^n + 1)` (addition, multiplication, reduction). |
--------------------------------------------------------------------------------------------------------------------------------------


## 🛠️ Parameters

This simplified **Baby Kyber** version works with minimal parameters for easy learning and testing:
- `q = 97` — modulus of the ring (in real Kyber implementations, `q = 3329`).
- `n = 4` — number of polynomial coefficients (degree + 1).
- `k = 2` — matrix/vector dimension.
- `eta = 1` — noise distribution parameter for CBD (Centered Binomial Distribution).


## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/baby-kyber.git
   cd baby-kyber
   ```

2. Make sure you have **Python 3.8+** installed.

3. Run the `main.py` script:
   ```bash
   python main.py
   ```

4. You will see:
   - Key generation
   - Message encryption (text string)
   - Message decryption and validation


## 🔒 How It Works

### 1. Polynomial Ring
All operations are performed in the polynomial ring `Z_q[X] / (X^n + 1)`, where:
- Polynomials are represented as lists of coefficients.
- `RingPolynom.py` implements addition, multiplication, and modular reduction.

### 2. Key Generation
- **Public Key**: matrix `A` and vector `t = A * s + e`.
- **Secret Key**: vector `s` consisting of small polynomials.

### 3. Encryption
- A random vector `r` is generated.
- Computes `u = A^T * r + e1`.
- Computes `v = t ⋅ r + e2 + ⌊(q/2)⌋ * m`.

### 4. Decryption
- Recovers `m` from `v - s ⋅ u`.
- The message bits are decoded based on thresholding relative to `q`.


## 📄 What This Project Demonstrates

✔️ The basics of **lattice-based cryptography**.  
✔️ An educational model of **Baby Kyber PKE** encryption.  
✔️ The principle of **noise generation** (CBD) for security.  
✔️ Operations on polynomials in modular rings.


## 🏗️ Project Structure

```
baby-kyber/
├── main.py             # Entry point: demonstrates encryption & decryption workflow
├── babyKyber.py        # Core cryptographic scheme: Baby Kyber (PKE)
└── RingPolynom.py      # Polynomial ring operations: addition, multiplication, reduction
```


## ✅ Example Output

```
========================================
🔑  KEY GENERATION
========================================
Public Key Matrix A:
[[...], [...]]
Public Key Vector t:
[[...]]
========================================
✉️  MESSAGE PREPARATION
========================================
Original Message:
	Hello DL, my practice is ready :)
========================================
🔒  ENCRYPTION
========================================
Ciphertext:
	[((u), (v)), ...]
========================================
🔓  DECRYPTION
========================================
Decrypted Message:
	Hello DL, my practice is ready :)
========================================
✅  RESULT
========================================
🎉 SUCCESS: The message was sent successfully! 🎉
```
