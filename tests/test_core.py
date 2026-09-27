import math
import unittest

from base32_geohash_encoder import encode, decode, BASE32_ALPHABET, GeohashError


class TestEncode(unittest.TestCase):
    def test_known_value(self):
        # Central London, a well-documented geohash reference point.
        self.assertEqual(encode(51.5074, -0.1278, 7), "gcpvj0d")

    def test_origin(self):
        self.assertEqual(encode(0.0, 0.0, 6), "s00000")

    def test_north_pole(self):
        result = encode(90.0, 0.0, 6)
        self.assertEqual(len(result), 6)
        lat, lon = decode(result)
        self.assertAlmostEqual(lat, 90.0, places=2)

    def test_south_pole(self):
        result = encode(-90.0, 0.0, 6)
        self.assertEqual(len(result), 6)
        lat, lon = decode(result)
        self.assertAlmostEqual(lat, -90.0, places=2)

    def test_antimeridian(self):
        result = encode(0.0, 180.0, 6)
        self.assertEqual(len(result), 6)

    def test_clamps_out_of_range(self):
        a = encode(100.0, 0.0, 6)
        b = encode(90.0, 0.0, 6)
        self.assertEqual(a, b)

    def test_default_precision(self):
        result = encode(51.5074, -0.1278)
        self.assertEqual(len(result), 12)

    def test_invalid_precision(self):
        with self.assertRaises(ValueError):
            encode(0.0, 0.0, 0)
        with self.assertRaises(ValueError):
            encode(0.0, 0.0, 13)


class TestDecode(unittest.TestCase):
    def test_known_value(self):
        lat, lon = decode("gcpvj0d")
        self.assertAlmostEqual(lat, 51.5074, places=2)
        self.assertAlmostEqual(lon, -0.1278, places=2)

    def test_empty_string(self):
        with self.assertRaises(GeohashError):
            decode("")

    def test_invalid_character(self):
        with self.assertRaises(GeohashError):
            decode("abc!def")

    def test_excluded_letters(self):
        # The geohash alphabet excludes a, i, l, o.
        for c in ("a", "i", "l", "o"):
            with self.assertRaises(GeohashError):
                decode(c)

    def test_roundtrip(self):
        for lat in (-45.0, 0.0, 45.0):
            for lon in (-120.0, 0.0, 120.0):
                h = encode(lat, lon, 9)
                d_lat, d_lon = decode(h)
                self.assertAlmostEqual(d_lat, lat, places=3)
                self.assertAlmostEqual(d_lon, lon, places=3)

    def test_single_char(self):
        lat, lon = decode("s")
        self.assertEqual(len(BASE32_ALPHABET), 32)
        self.assertTrue(-90.0 <= lat <= 90.0)
        self.assertTrue(-180.0 <= lon <= 180.0)


class TestAlphabet(unittest.TestCase):
    def test_alphabet_length(self):
        self.assertEqual(len(BASE32_ALPHABET), 32)

    def test_no_duplicates(self):
        self.assertEqual(len(set(BASE32_ALPHABET)), 32)

    def test_excluded_chars(self):
        for c in "ailo":
            self.assertNotIn(c, BASE32_ALPHABET)


if __name__ == "__main__":
    unittest.main()
