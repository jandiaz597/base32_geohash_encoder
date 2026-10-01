# Base32 Geohash Encoder

Encodes and decodes geographic coordinates using the standard Base32 geohash alphabet (0-9, b-z, excluding a, i, l, o).

```python
from base32_geohash_encoder import encode, decode

h = encode(51.5074, -0.1278, precision=7)  # 'gcpvj0d'
lat, lon = decode(h)                        # (51.5060..., -0.1298...)
```

## Why

Geohashing maps (lat, lon) into a single string by interleaving bits and grouping them into 5-bit Base32 characters. This library implements that one thing with no dependencies. The trade-off: `decode` returns the center of the decoded cell, not the original input, so short precisions lose information. Round-tripping through `decode(encode(x))` gives you an approximation, not an exact value.

## Edge cases

- Out-of-range coordinates are clamped, not rejected. `encode(100, 0)` is treated as `encode(90, 0)`.
- Precision is capped at 12 characters. Beyond that, float64 rounding makes additional bits unreliable.
- The alphabet excludes `a`, `i`, `l`, and `o` to avoid confusion with `0`, `1`, and each other. Passing these to `decode` raises `GeohashError`.

## API

- `encode(lat, lon, precision=12) -> str`
- `decode(geohash) -> tuple[float, float]`
- `BASE32_ALPHABET` — the 32-character string used for encoding.
- `GeohashError` — raised by `decode` on invalid input.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

