# ntrst

1) encryption utility
2) it isn't rust
3) thanks to mattf for suggesting a repo name that inspired this repo name
   mattf's suggestion of "notrst" was almost good enough to use for this repo
   better luck next time mattf
   https://github.com/matheusfillipe

   about homomorphic encryption:

   weiou34qpr89u98typ3wo4twhierughlfkkfdgh
   lskdfjghlkdfjhslkdjhflkgsjfdhlgksjhdfg
   sdflkjshdfglkjsfhdglkjshdflgkjhdfgslfdkgjh
   lksjdjhglskdfjghlsfdkjghlskfdghlksjdf
   sldfkjhsl
   lskjdfghlskjdfghlsfkdjghlskfdjghdfg;jksfdlhg
   lskdjhlsgjkhsdfl

## Suggested Library: Microsoft SEAL

For a C/C++ homomorphic encryption library, **[Microsoft SEAL](https://github.com/microsoft/SEAL)** is the gold standard. It provides:

- **BFV** and **CKKS** schemes for integer and approximate arithmetic on encrypted data
- Full C++ API with headers-only and compiled options
- MIT-licensed
- Extensive [documentation](https://github.com/microsoft/SEAL/tree/main/native/docs)
- The very library that Python's [TenSEAL](https://github.com/OpenMined/TenSEAL) wraps under the hood

### Quick example (C++)

```cpp
#include "seal/seal.h"
#include <iostream>

int main() {
    using namespace seal;

    EncryptionParameters parms(scheme_type::bfv);
    parms.set_poly_modulus_degree(8192);
    parms.set_coeff_modulus(CoeffModulus::BFVDefault(8192));
    parms.set_plain_modulus(PlainModulus::Batching(8192, 20));

    SEALContext context(parms);
    KeyGenerator keygen(context);
    PublicKey public_key = keygen.public_key();
    SecretKey secret_key = keygen.secret_key();

    Encryptor encryptor(context, public_key);
    Evaluator evaluator(context);
    Decryptor decryptor(context, secret_key);
    BatchEncoder encoder(context);

    std::vector<int64_t> pod_matrix = {1, 2, 3, 4};
    Plaintext plain_matrix;
    encoder.encode(pod_matrix, plain_matrix);

    Ciphertext encrypted_matrix;
    encryptor.encrypt(plain_matrix, encrypted_matrix);

    // Homomorphic addition
    evaluator.add_inplace(encrypted_matrix, encrypted_matrix);

    Plaintext decrypted;
    decryptor.decrypt(encrypted_matrix, decrypted);
    std::vector<int64_t> result;
    encoder.decode(decrypted, result);
    // result == {2, 4, 6, 8}
}
```

### Build

```bash
git clone https://github.com/microsoft/SEAL.git
cd SEAL && mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/.local
make -j$(nproc) && make install
```

### Other C/C++ HE libraries worth considering

| Library | Scheme | License |
|---------|--------|---------|
| [Microsoft SEAL](https://github.com/microsoft/SEAL) | BFV, CKKS | MIT |
| [HElib](https://github.com/homenc/HElib) | BGV, CKKS | Apache 2.0 |
| [PALISADE](https://gitlab.com/palisade/palisade-release) | BFV, BGV, CKKS, FHEW, TFHE | BSD 2-Clause |
| [OpenFHE](https://github.com/openfheorg/openfhe-development) | BFV, BGV, CKKS, FHEW, TFHE | BSD 2-Clause |
