"""Base32 geohash encoder for geographic coordinates.

Uses the standard geohash Base32 alphabet (0-9, b-z, excluding a, i, l, o).
This is the variant used by geohash.org and most implementations.
"""

BASE32_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"


class GeohashError(ValueError):
    """Raised when a geohash string cannot be decoded."""


def encode(lat, lon, precision=12):
    """Encode a latitude/longitude pair into a Base32 geohash string.

    Args:
        lat: Latitude in degrees. Clamped to [-90, 90].
        lon: Longitude in degrees. Clamped to [-180, 180].
        precision: Number of characters in the output (1-12).

    Returns:
        A Base32 geohash string of the given length.

    Raises:
        ValueError: If precision is outside [1, 12].
    """
    if not 1 <= precision <= 12:
        raise ValueError("precision must be in [1, 12]")

    lat = max(-90.0, min(90.0, float(lat)))
    lon = max(-180.0, min(180.0, float(lon)))

    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    geohash = []
    bit = 0
    ch = 0
    even = True

    while len(geohash) < precision:
        if even:
            mid = (lon_range[0] + lon_range[1]) / 2
            if lon >= mid:
                ch |= (1 << (4 - bit))
                lon_range[0] = mid
            else:
                lon_range[1] = mid
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if lat >= mid:
                ch |= (1 << (4 - bit))
                lat_range[0] = mid
            else:
                lat_range[1] = mid

        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash.append(BASE32_ALPHABET[ch])
            bit = 0
            ch = 0

    return "".join(geohash)


def decode(geohash):
    """Decode a Base32 geohash string back to a latitude/longitude pair.

    Args:
        geohash: A Base32 geohash string.

    Returns:
        A tuple (lat, lon) of floats representing the center of the decoded cell.

    Raises:
        GeohashError: If the string is empty or contains invalid characters.
    """
    if not geohash:
        raise GeohashError("empty geohash")

    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bit = 0
    even = True

    for c in geohash:
        idx = BASE32_ALPHABET.find(c)
        if idx == -1:
            raise GeohashError("invalid character: {!r}".format(c))
        for bit_pos in range(4, -1, -1):
            val = (idx >> bit_pos) & 1
            if even:
                mid = (lon_range[0] + lon_range[1]) / 2
                if val:
                    lon_range[0] = mid
                else:
                    lon_range[1] = mid
            else:
                mid = (lat_range[0] + lat_range[1]) / 2
                if val:
                    lat_range[0] = mid
                else:
                    lat_range[1] = mid
            even = not even

    lat = (lat_range[0] + lat_range[1]) / 2
    lon = (lon_range[0] + lon_range[1]) / 2
    return (lat, lon)
