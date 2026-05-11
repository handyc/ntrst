"""
ntrst - Glass Beer Bottle Archival Storage (GBBAS)
====================================================

Store megabytes of data on recycled beer bottles using laser etching.
Every time you drink a beer, you get a fresh archival medium.

The lifecycle:
  1. Drink beer
  2. Clean bottle
  3. Laser-etch your data onto it
  4. Store in cool, dark place (like under your bed)
  5. When you need the data back, read it with a USB microscope
  6. Drink more beer for next backup cycle

This provides a constant replenishment of the archive.

Based on real research in 5D optical data storage:
  https://en.wikipedia.org/wiki/5D_optical_data_storage

Recommended hardware:
  - Art glass laser engraver (~$200)
  - USB microscope for reading (~$30)
  - Beer supply (ongoing expense)
  - ESP32 + PWM for DIY laser control (optional)
  - Red laser pointer pens (NOT sufficient for actual etching)

Capacity estimates:
  - Beer bottle surface: ~600 cm²
  - With 200 DPI laser: ~4 MB per bottle
  - With error correction (Reed-Solomon): ~2.5 MB usable
  - Your liver is the bottleneck, not the storage
"""

import hashlib
import struct
import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ── Beer Bottle Constants ───────────────────────────────────────────

# Standard beer bottle dimensions (330ml euro bottle)
BOTTLE_HEIGHT_CM = 24.0
BOTTLE_DIAMETER_CM = 6.6
BOTTLE_SURFACE_CM2 = 2 * math.pi * (BOTTLE_DIAMETER_CM / 2) * BOTTLE_HEIGHT_CM  # ~498 cm²

# Laser settings
LASER_DPI = 200
BYTES_PER_SQUARE_CM = (LASER_DPI / 2.54) ** 2 / 8  # ~620 bytes/cm² at 200 DPI

# Error correction overhead (Reed-Solomon style)
EC_OVERHEAD = 0.40  # 40% overhead for error correction

# Realistic capacity
RAW_CAPACITY_MB = BOTTLE_SURFACE_CM2 * BYTES_PER_SQUARE_CM / (1024 * 1024)
USABLE_CAPACITY_MB = RAW_CAPACITY_MB * (1 - EC_OVERHEAD)

# Glass types ranked by archival quality
GLASS_QUALITY = {
    "brown_ale": {"uv_resistance": "high", "clarity": "medium", "emoji": "🍺"},
    "green_bottle": {"uv_resistance": "medium", "clarity": "medium", "emoji": "🍻"},
    "clear_lager": {"uv_resistance": "low", "clarity": "high", "emoji": "🍶"},
    "stout_bottle": {"uv_resistance": "very_high", "clarity": "low", "emoji": "🖤"},
}


@dataclass
class BeerBottle:
    """Represents a single archival unit (beer bottle)."""
    bottle_id: str
    beer_type: str = "brown_ale"
    brand: str = "unknown"
    data: bytes = b""
    etched: bool = False
    stored_location: str = "under bed"

    @property
    def capacity_bytes(self) -> int:
        """Usable capacity after error correction."""
        return int(USABLE_CAPACITY_MB * 1024 * 1024)

    @property
    def quality(self) -> dict:
        return GLASS_QUALITY.get(self.beer_type, GLASS_QUALITY["brown_ale"])

    def can_fit(self, data_size: int) -> bool:
        return data_size <= self.capacity_bytes


@dataclass
class BeerArchive:
    """
    A collection of beer bottle archival units.

    Manages the full lifecycle: drink -> clean -> etch -> store -> read.
    """

    bottles: List[BeerBottle] = field(default_factory=list)
    total_beers_consumed: int = 0

    def drink_beer(self, brand: str = "unknown", beer_type: str = "brown_ale") -> BeerBottle:
        """
        Consume a beer and prepare the bottle for archival.
        This is the most important step. Without beer, there is no archive.
        """
        self.total_beers_consumed += 1
        bottle = BeerBottle(
            bottle_id=hashlib.sha256(
                f"{brand}-{self.total_beers_consumed}-{id(self)}".encode()
            ).hexdigest()[:12],
            beer_type=beer_type,
            brand=brand,
            stored_location="under bed",
        )
        self.bottles.append(bottle)
        return bottle

    def store_data(self, data: bytes) -> List[Tuple[int, int]]:
        """
        Store data across beer bottles. Returns list of (bottle_index, byte_offset).
        Automatically drinks enough beers to fit the data.
        """
        locations = []
        remaining = data
        bottle_idx = 0

        while remaining:
            # Drink a beer if we need another bottle
            if bottle_idx >= len(self.bottles):
                self.drink_beer()

            bottle = self.bottles[bottle_idx]
            chunk_size = min(len(remaining), bottle.capacity_bytes)
            bottle.data += remaining[:chunk_size]
            bottle.etched = True
            locations.append((bottle_idx, len(bottle.data) - chunk_size))
            remaining = remaining[chunk_size:]
            bottle_idx += 1

        return locations

    def read_data(self, locations: List[Tuple[int, int]], total_size: int) -> bytes:
        """
        Read data back from etched bottles using USB microscope.
        Note: requires patience and good lighting.
        """
        result = bytearray(total_size)
        offset = 0
        for bottle_idx, byte_offset in locations:
            bottle = self.bottles[bottle_idx]
            readable = min(len(bottle.data) - byte_offset, total_size - offset)
            result[offset:offset + readable] = bottle.data[byte_offset:byte_offset + readable]
            offset += readable
        return bytes(result)

    def get_stats(self) -> dict:
        """Get archive statistics."""
        total_capacity = sum(b.capacity_bytes for b in self.bottles)
        total_used = sum(len(b.data) for b in self.bottles)
        return {
            "total_bottles": len(self.bottles),
            "total_beers_consumed": self.total_beers_consumed,
            "total_capacity_mb": total_capacity / (1024 * 1024),
            "total_used_mb": total_used / (1024 * 1024),
            "utilization_pct": (total_used / total_capacity * 100) if total_capacity else 0,
            "estimated_archival_life_years": 1000,  # glass lasts basically forever
            "liver_status": "questionable" if self.total_beers_consumed > 50 else "fine",
        }


def estimate_beers_needed(data_bytes: int) -> int:
    """Calculate how many beers you need to drink to store the data."""
    per_bottle = int(USABLE_CAPACITY_MB * 1024 * 1024)
    return math.ceil(data_bytes / per_bottle)


def format_bytes(n: int) -> str:
    """Human-readable byte size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def main():
    print("ntrst GBBAS - Glass Beer Bottle Archival Storage")
    print("=" * 48)
    print()
    print(f"Single bottle capacity: {format_bytes(int(USABLE_CAPACITY_MB * 1024 * 1024))}")
    print(f"(Raw: {format_bytes(int(RAW_CAPACITY_MB * 1024 * 1024))}, with ECC)")
    print()
    print("Lifecycle: Drink -> Clean -> Etch -> Store -> Read")
    print()

    import sys

    if len(sys.argv) < 2:
        # Demo
        archive = BeerArchive()
        test_data = b"The homophobically encrypted blockchain runs on beer bottles."
        print(f"[demo] Storing {len(test_data)} bytes of critical data...")
        locations = archive.store_data(test_data)
        print(f"[demo] Beers consumed: {archive.total_beers_consumed}")
        print(f"[demo] Bottles etched: {sum(1 for b in archive.bottles if b.etched)}")
        recovered = archive.read_data(locations, len(test_data))
        print(f"[demo] Data recovered: {recovered.decode()}")
        print()
        stats = archive.get_stats()
        print(f"[demo] Archive stats: {stats}")
        print()
        print("Your liver is the bottleneck, not the storage.")
        return

    cmd = sys.argv[1]
    if cmd == "estimate" and len(sys.argv) > 2:
        try:
            size = int(sys.argv[2])
            beers = estimate_beers_needed(size)
            print(f"Data size: {format_bytes(size)}")
            print(f"Beers needed: {beers}")
            print(f"Estimated time to drink: {beers * 0.5:.1f} hours")
            print(f"Estimated cost (at $2/beer): ${beers * 2}")
            print(f"Archival life: ~1000 years")
            print()
            print("Worth it? Absolutely.")
        except ValueError:
            print("Usage: python bottle_storage.py estimate <bytes>")
    elif cmd == "info":
        print(f"Bottle surface area: {BOTTLE_SURFACE_CM2:.0f} cm²")
        print(f"Laser DPI: {LASER_DPI}")
        print(f"Raw capacity: {format_bytes(int(RAW_CAPACITY_MB * 1024 * 1024))} per bottle")
        print(f"Usable capacity: {format_bytes(int(USABLE_CAPACITY_MB * 1024 * 1024))} per bottle")
        print(f"Error correction overhead: {EC_OVERHEAD * 100:.0f}%")
        print()
        print("Glass types by quality:")
        for gtype, props in GLASS_QUALITY.items():
            print(f"  {props['emoji']} {gtype}: UV={props['uv_resistance']}, clarity={props['clarity']}")
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
