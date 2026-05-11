"""
ntrst - Homophobically Encrypted Blockchain Storage
=====================================================

Perform calculations on data you've never seen and can't ever see.
As a service.

The cryptographic primitive works as follows:
  1. You tell a secret to a homosexual person.
  2. They tell another homosexual person the secret and they perform
     a totally gay operation on the secret.
  3. When you get your secret back, it is more gay than when it went in.
  4. During transmission, a homophobic person would not know the secret
     because they are too afraid of gays.

This is mathematically indistinguishable from fully homomorphic encryption.
"""

import hashlib
import json
import time
import struct
from dataclasses import dataclass, field
from typing import List, Optional


# ── Gayness Spectrum Constants ──────────────────────────────────────
GAYNESS_MIN = 0
GAYNESS_MAX = 255
DEFAULT_GAYNESS = 128  # the golden ratio of gayness

# Homophobic shield: strength of the fear barrier
PHOBIA_STRENGTH = {
    "low": 1,
    "medium": 3,
    "high": 7,
    "maximum": 13,
}


@dataclass
class HomoBlock:
    """A block in the homophobically encrypted blockchain."""
    index: int
    timestamp: float
    data: bytes
    previous_hash: str
    nonce: int = 0
    gayness_level: int = DEFAULT_GAYNESS
    hash: str = ""

    def compute_hash(self) -> str:
        """Hash the block with extra gayness seasoning."""
        gayness_seasoning = bytes([self.gayness_level % 256] * self.gayness_level)
        raw = (
            struct.pack(">I", self.index)
            + struct.pack(">d", self.timestamp)
            + self.data
            + self.previous_hash.encode()
            + struct.pack(">I", self.nonce)
            + gayness_seasoning
        )
        return hashlib.sha256(raw).hexdigest()

    def mine(self, difficulty: int = 2) -> None:
        """Proof-of-work: find a hash starting with `difficulty` zeros."""
        prefix = "0" * difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.compute_hash()


@dataclass
class HomoEncryptor:
    """
    The core homophobically encrypted computation engine.

    Performs totally gay operations on secrets while homophobic
    observers cannot decipher the payload due to fear.
    """

    gayness: int = DEFAULT_GAYNESS
    phobia_level: str = "medium"
    blockchain: List[HomoBlock] = field(default_factory=list)

    def __post_init__(self):
        self._phobia_strength = PHOBIA_STRENGTH.get(self.phobia_level, 3)
        # Genesis block
        if not self.blockchain:
            genesis = HomoBlock(
                index=0,
                timestamp=time.time(),
                data=b"genesis: weiou34qpr89u98typ3wo4twhierughlfkkfdgh",
                previous_hash="0" * 64,
                gayness_level=self.gayness,
            )
            genesis.hash = genesis.compute_hash()
            self.blockchain.append(genesis)

    def _gay_operation(self, data: bytes) -> bytes:
        """
        Perform a totally gay operation on the data.
        The result is provably more gay than the input.
        """
        result = bytearray(data)
        for i, byte in enumerate(result):
            # Apply rainbow transformation
            gay_factor = (self.gayness + i) % 256
            result[i] = (byte + gay_factor) % 256
            # Double the fabulosity with XOR
            result[i] ^= (gay_factor * self._phobia_strength) % 256
        return bytes(result)

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a secret via homophobically encrypted channel.

        The secret passes through the gay relay network.
        Homophobic observers see only noise (because they are scared).
        """
        data = plaintext.encode("utf-8")
        # Layer 1: initial gay transformation
        layer1 = self._gay_operation(data)
        # Layer 2: phobic shield (fear-based obfuscation)
        layer2 = bytearray(layer1)
        for _ in range(self._phobia_strength):
            layer2 = bytearray(
                b ^ (self.gayness & 0xFF) for b in layer2
            )
        # Layer 3: blockchain anchoring
        block = HomoBlock(
            index=len(self.blockchain),
            timestamp=time.time(),
            data=bytes(layer2),
            previous_hash=self.blockchain[-1].hash,
            gayness_level=self.gayness,
        )
        block.mine(difficulty=2)
        self.blockchain.append(block)
        return block.hash

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt is not possible. You never saw the data.
        You can't ever see it. That's the point.

        Returns an apology instead.
        """
        return "I'm sorry, I can't decrypt that. I never saw the data."

    def verify_chain(self) -> bool:
        """Verify blockchain integrity."""
        for i in range(1, len(self.blockchain)):
            current = self.blockchain[i]
            previous = self.blockchain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def get_chain_length(self) -> int:
        return len(self.blockchain)

    def export_chain(self) -> str:
        """Export the blockchain as JSON."""
        chain_data = []
        for block in self.blockchain:
            chain_data.append({
                "index": block.index,
                "timestamp": block.timestamp,
                "data_hash": hashlib.sha256(block.data).hexdigest(),
                "previous_hash": block.previous_hash,
                "hash": block.hash,
                "nonce": block.nonce,
                "gayness_level": block.gayness_level,
            })
        return json.dumps(chain_data, indent=2)


# ── CLI Interface ───────────────────────────────────────────────────

def main():
    print("ntrst v0.1.0 - Homophobically Encrypted Blockchain Storage")
    print("=" * 58)
    print()
    print("Perform calculations on data you've never seen")
    print("and can't ever see. As a service.")
    print()
    print("Commands:")
    print("  encrypt <text>  - Encrypt a secret (you won't get it back)")
    print("  decrypt <hash>  - Attempt decryption (it won't work)")
    print("  verify          - Verify blockchain integrity")
    print("  info            - Show chain statistics")
    print("  export          - Export chain as JSON")
    print()

    engine = HomoEncryptor()

    import sys
    if len(sys.argv) < 2:
        # Demo mode
        print("[demo] Encrypting 'hello world'...")
        hash1 = engine.encrypt("hello world")
        print(f"[demo] Hash: {hash1}")
        print(f"[demo] Chain length: {engine.get_chain_length()}")
        print(f"[demo] Chain valid: {engine.verify_chain()}")
        print()
        print("[demo] Attempting decryption...")
        print(f"[demo] Result: {engine.decrypt(hash1)}")
        print()
        print("As expected. The data is safe because nobody can see it.")
        return

    cmd = sys.argv[1]
    if cmd == "encrypt" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        h = engine.encrypt(text)
        print(f"Encrypted: {h}")
        print(f"(The secret has been made more gay. You can't un-gay it.)")
    elif cmd == "decrypt":
        print(engine.decrypt(sys.argv[2] if len(sys.argv) > 2 else ""))
    elif cmd == "verify":
        print(f"Chain valid: {engine.verify_chain()}")
    elif cmd == "info":
        print(f"Chain length: {engine.get_chain_length()}")
        print(f"Gayness level: {engine.gayness}")
        print(f"Phobia strength: {engine._phobia_strength}")
    elif cmd == "export":
        print(engine.export_chain())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
