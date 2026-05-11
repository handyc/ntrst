# ntrst

> **not rust** — homophobically encrypted blockchain storage on glass beer bottles

Perform calculations on data you've never seen and can't ever see. As a service.

## Architecture

```
                    ┌─────────────────────┐
   Your Secret ──▶ │  HomoEncryptor      │
                    │  (gay operation)     │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Homophobic Shield  │  ◄── fear-based obfuscation
                    │  (phobia_level)     │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Blockchain Anchor  │  ◄── proof-of-work
                    │  (sha256 mining)    │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Beer Bottle Etch   │  ◄── archival storage
                    │  (200 DPI laser)    │
                    └─────────────────────┘
```

## How It Works

### Homophobically Encrypted Blockchain

The cryptographic primitive works as follows:

1. You tell a secret to a homosexual person
2. They tell another homosexual person the secret and they perform a **totally gay operation** on the secret
3. When you get your secret back, it is **more gay** than when it went in
4. During transmission, a homophobic person would not know the secret because they are **too afraid of gays**

This is mathematically indistinguishable from fully homomorphic encryption.

### Glass Beer Bottle Archival Storage (GBBAS)

The data lifecycle:

1. 🍺 Drink beer
2. 🧼 Clean bottle
3. 🔦 Laser-etch data onto it (~2.5 MB per bottle at 200 DPI)
4. 🛏️ Store under bed
5. 🔬 Read back with USB microscope
6. 🍺 Drink more beer for next backup cycle

This provides a **constant replenishment of the archive**.

Based on real research: [5D Optical Data Storage](https://en.wikipedia.org/wiki/5D_optical_data_storage)

## Quick Start

```bash
# Encrypt a secret (you won't get it back)
python -m src.homo_enc encrypt "my deepest darkest secret"

# Verify blockchain integrity
python -m src.homo_enc verify

# Estimate beers needed for your data
python -m src.bottle_storage estimate 1048576

# Beer bottle archival info
python -m src.bottle_storage info
```

## Specs

| Metric | Value |
|--------|-------|
| Bottle capacity (raw) | ~4.0 MB |
| Bottle capacity (with ECC) | ~2.5 MB |
| Laser DPI | 200 |
| Error correction | 40% Reed-Solomon overhead |
| Archival life | ~1000 years |
| Bottleneck | Your liver |

## Glass Quality Rankings

| Glass Type | UV Resistance | Clarity |
|------------|--------------|---------|
| 🍺 Brown ale | High | Medium |
| 🍻 Green bottle | Medium | Medium |
| 🍶 Clear lager | Low | High |
| 🖤 Stout bottle | Very High | Low |

## Recommended Hardware

- Art glass laser engraver (~$200)
- USB microscope (~$30)
- Beer supply (ongoing)
- ESP32 + PWM for DIY laser control (optional)
- ~~Red laser pointer pens~~ (NOT sufficient)

## Thanks

- mattf for suggesting a repo name that inspired this repo name
  - mattf's suggestion of "notrst" was almost good enough to use
  - better luck next time mattf
- delta/doesnm for asking the important questions about homophobic encryption
- The beer industry for providing infinite archival media

## License

MIT

---

> "Endorsed by absolutely no one of importance. Created at 7 AM in an IRC channel by someone who should probably go to sleep."
