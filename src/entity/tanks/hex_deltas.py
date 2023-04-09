class HexDeltas:
    rings = []

    @classmethod
    def make_rings(cls):
        max_range = 3  # Change if maximum range of any tank is > 3 hexes
        cls.rings = [cls.make_ring_coords(i) for i in range(1, max_range + 1)]

    @staticmethod
    def make_ring_coords(ring_num: int) -> tuple[tuple[int, int, int]]:
        # Makes all the possible coordinates in a given ring around (0,0,0)
        ring_coords = []
        max_crd = ring_num
        min_crd = -ring_num
        required_abs_sum = ring_num * 2
        for i in range(min_crd, max_crd + 1):
            for j in range(max(min_crd, min_crd - i), min(max_crd, max_crd - i) + 1):
                k = -i - j
                if abs(i) + abs(j) + abs(k) == required_abs_sum:
                    ring_coords.append((i, j, k))
        return tuple(ring_coords)


HexDeltas.make_rings()
