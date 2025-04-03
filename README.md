# 📌 Baby Kyber — A Simplified Lattice-Based Cryptographic Scheme

This repository contains an **educational, simplified implementation** of the **Baby Kyber** encryption scheme. It is based on **lattice-based cryptography** principles and mimics the core mechanics of the **Kyber PKE** (Public Key Encryption) system, which is part of the **NIST PQC Kyber KEM** standard. The parameters are deliberately kept small for easier understanding and learning.


## ⚙️ Components

The implementation consists of five modules:
--------------------------------------------------------------------------------------------------------------------------------------
| File             | Description                                                                                                     |
|------------------|-----------------------------------------------------------------------------------------------------------------|
| `main.py`        | Entry point. Demonstrates key generation, message encryption, and decryption workflows.                         |
| `babyKyber.py`   | Contains the core **Baby Kyber** cryptographic scheme: key generation, encryption, decryption.                  |
| `RingPolynom.py` | Provides polynomial arithmetic operations in the ring `Z_q[X]/(X^n + 1)` (addition, multiplication, reduction). |
| `ind_cpa.py`     | Runs an automated IND-CPA game and prints statistical results of the attack.				     |
| `ind_cca.py`	   | Runs an automated IND-CCA game and demonstrates the practical insecurity of Baby Kyber against CCA. 	     |	     				    
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

2. Navigate to the `BabyKyber` folder:
   ```bash
   cd BabyKyber
   ```

   All implementation files (`main.py`, `babyKyber.py`, `ind_cpa.py`, etc.) are located inside the `BabyKyber/` subdirectory.

3. Make sure you have **Python 3.8+** installed.

4. Run the `main.py` script:
   ```bash
   python main.py
   ```

5. You will see:
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


## 📁 Project Structure

```
baby-kyber/
├── main.py           # Entry point: demonstrates encryption & decryption workflow
├── babyKyber.py      # Core cryptographic scheme: Baby Kyber (PKE)
├── RingPolynom.py    # Polynomial ring operations: addition, multiplication, reduction
├── ind_cpa.py        # IND-CPA game: chosen-plaintext attack experiment
└── ind_cca.py        # IND-CCA game: chosen-ciphertext attack experiment
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

## 🧪 Security Experiments: IND-CPA and IND-CCA

This project also includes **interactive experiments** to test the Baby Kyber encryption scheme against two security models:


## 📌 IND-CPA Experiment (Chosen Plaintext Attack)

This test simulates a game where an adversary:
- Can encrypt any messages of their choice.
- Receives a challenge ciphertext `c*` of either `m0` or `m1`.
- Must guess which message was encrypted based on ciphertext analysis.

✅ Baby Kyber demonstrates strong resistance in this game — the adversary performs no better than random guessing.


## 🔓 IND-CCA Experiment (Chosen Ciphertext Attack)

This test is stronger and allows the adversary to:
- Access a **decryption oracle** for any ciphertexts except the challenge `c*`.
- Analyze the decryption output of modified versions of `c*`.
- Try to infer the original message bit `b`.

🚨 In this game, Baby Kyber is **not CCA-secure**:  
> By slightly modifying `c*` and decrypting the result, the adversary can perfectly distinguish between `m0` and `m1`.


## 📊 Experimental Results

The attack scripts print:
- ✅ Number of successful guesses
- 🔢 Guessing probability
- 📈 Statistical advantage over random guessing
- 🧪 p-value (binomial test)
- 📉 Confidence intervals

Example (IND-CPA):
```
Adversary success rate: 5029/10000  
Probability of guessing correctly: 0.5029  
Advantage over random guessing: 0.0029  
p-value (binomial test): 0.5687  
95% confidence interval: [0.4927, 0.5131]
```

Example (IND-CCA):
```
Adversary success rate: 10000/10000
Probability of guessing correctly: 1.0000
Advantage over random guessing: 0.5000
p-value (binomial test): 0.0000
95% confidence interval: [1.0000, 1.0000]
```

## 🚀 How to Run IND-CPA and IND-CCA Experiments

Both experiments are implemented in separate scripts:

```bash
python ind_cpa.py     # runs the IND-CPA game
python ind_cca.py     # runs the IND-CCA game
```

Make sure to place these files alongside your `babyKyber.py` and `RingPolynom.py`.


## 📌 Conclusion

- ✅ Baby Kyber **demonstrates IND-CPA security** in practice.
- ❌ Baby Kyber **fails to achieve IND-CCA security**, as expected for unauthenticated PKE schemes.
- 🧠 These experiments help illustrate the difference between **CPA** and **CCA** security in a practical, hands-on way.
