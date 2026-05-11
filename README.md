# ntrst

1) encryption utility
2) it isn't rust
3) thanks to mattf for suggesting a repo name that inspired this repo name
   mattf's suggestion of "notrst" was almost good enough to use for this repo
   better luck next time mattf
   https://github.com/matheusfillipe

## Suggested Approach: Microsoft SEAL

This project aims to provide a C++ encryption utility built around **homomorphic encryption**. A strong candidate for the core library is **[Microsoft SEAL](https://github.com/microsoft/SEAL)**.

### Why Microsoft SEAL?

- **C++ native** — written in modern C++17 with no external dependencies, making it straightforward to integrate.
- **BFV and CKKS schemes** — supports both integer (BFV) and approximate (CKKS) homomorphic encryption, covering most practical use cases.
- **Battle-tested** — developed and maintained by Microsoft Research; used in production systems and academic work.
- **Permissive license** — released under the MIT License, compatible with most projects.
- **Well-documented** — comprehensive [API docs](https://microsoft.github.io/SEAL/) and [examples](https://github.com/microsoft/SEAL/tree/main/native/examples).

### Getting Started

```bash
git clone https://github.com/microsoft/SEAL.git
cd SEAL && mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/seal-install
make -j$(nproc) && make install
```

### Minimal Example

```cpp
#include "seal/seal.h"
#include <iostream>

int main() {
    using namespace seal;

    // 1. Set up encryption parameters
    EncryptionParameters parms(scheme_type::bfv);
    size_t poly_modulus_degree = 8192;
    parms.set_poly_modulus_degree(poly_modulus_degree);
    parms.set_coeff_modulus(CoeffModulus::BFVDefault(poly_modulus_degree));
    parms.set_plain_modulus(PlainModulus::Batching(poly_modulus_degree, 20));

    SEALContext context(parms);

    // 2. Generate keys
    KeyGenerator keygen(context);
    PublicKey public_key;
    keygen.create_public_key(public_key);
    SecretKey secret_key = keygen.secret_key();

    // 3. Encryptor / Decryptor
    Encryptor encryptor(context, public_key);
    Decryptor decryptor(context, secret_key);
    Evaluator evaluator(context);
    BatchEncoder encoder(context);

    std::vector<int64_t> pod_matrix = {1, 2, 3, 4};
    Plaintext plain_matrix;
    encoder.encode(pod_matrix, plain_matrix);

    // 4. Encrypt
    Ciphertext encrypted;
    encryptor.encrypt(plain_matrix, encrypted);

    // 5. Compute on ciphertexts (e.g. add encrypted to itself)
    Ciphertext result;
    evaluator.add(encrypted, encrypted, result);

    // 6. Decrypt
    Plaintext plain_result;
    decryptor.decrypt(result, encoder.decode(plain_result));

    std::cout << "Result: " << plain_result.to_string() << std::endl;
    return 0;
}
```

### CMake Integration

```cmake
find_package(SEAL REQUIRED)
target_link_libraries(your_target SEAL::seal)
```

### Alternatives Considered

| Library       | Language | Scheme(s)          | Notes                        |
|---------------|----------|--------------------|------------------------------|
| **Microsoft SEAL** | C++ | BFV, CKKS          | ✅ Recommended               |
| TenSEAL       | Python  | BFV, CKKS          | Wrapper around SEAL; not native C++ |
| HElib         | C++     | BGV, CKKS, CGGI    | Heavier; Apache 2.0 license |
| PALISADE      | C++     | BGV, BFV, CKKS, RLWE | Larger codebase; BSD-3      |

Microsoft SEAL offers the best balance of simplicity, performance, and permissive licensing for a C++ project.

### About Homomorphic Encryption

Homomorphic encryption allows computations on encrypted data without decrypting it first. This enables:

- **Privacy-preserving machine learning** — train models on encrypted data.
- **Secure outsourced computation** — delegate processing to untrusted servers.
- **Confidential data analytics** — aggregate insights without exposing individual records.

---

   about homomorphic encryption:

   weiou34qpr89u98typ3wo4twhierughlfkkfdgh
   lskdfjghlkdfjhslkdjhflkgsjfdhlgksjhdfg
   sdflkjshdfglkjsfhdglkjshdflgkjhdfgslfdkgjh
   lksjdjhglskdfjghlsfdkjghlskfdghlksjdf
   sldfkjhsl
   lskjdfghlskjdfghlsfkdjghlskfdjghdfg;jksfdlhg
   lskdjhlsgjkhsdfl
