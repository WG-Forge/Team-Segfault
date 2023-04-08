
class HexDeltas:
    @staticmethod
    def get_ring_coords(ring_num: int) -> tuple[tuple[int, int, int]]:
        # Makes all the possible coordinates in a given ring around (0,0,0)
        ring_coords = []
        max_crd = ring_num
        min_crd = -ring_num
        required_abs_sum = ring_num*2
        for i in range(min_crd, max_crd+1):
            for j in range(max(min_crd, min_crd-i), min(max_crd, max_crd-i)+1):
                k = -i-j
                if abs(i) + abs(j) + abs(k) == required_abs_sum:
                    ring_coords.append((i, j, k))
        return tuple(ring_coords)

    @staticmethod
    def TD_firing_pattern(self, max_range: int) -> tuple[tuple[int, int, int]]:
        pattern_coords = []
        for i in range(1, max_range+1, 1):
            TD_ring = tuple(filter(lambda t: 0 not in t, my_tuple))
            pattern_coords.append(HexDeltas.get_ring_coords(i))


    ring1 = get_ring_coords(1)
    ring2 = get_ring_coords(2)
    ring3 = get_ring_coords(3)

