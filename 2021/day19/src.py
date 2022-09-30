from dataclasses import dataclass
from typing import List, Set
from math import sqrt
from itertools import combinations
from functools import reduce, cached_property

@dataclass
class Point:
    x: int
    y: int
    z: int

    # allow points to be added and subtracted from one another
    # doing so generates new points that can be treated as vectors
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    # define __hash__ and __eq__ so points can be added to sets
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other: "Point") -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    # helper for calculating distances between points
    def distance(self, other: "Point") -> "Point":
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    # calculate all distances between this point and a list of other points
    def neighbor_distances(self, others: List["Point"]) -> Set[int]:
        return set([int(self.distance(other)) for other in others]) - set([0])

    # manhattan distance between points for part 2
    def manhattan(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    # try to generate a rotational matrix for this point to make it match another given point
    def rotation(self, other: "Point") -> List[int]:
        def get_factor(self_attr: str, other_attr: str) -> int:
            if getattr(self, self_attr) == getattr(other, other_attr): return 1
            if getattr(self, self_attr) == -1 * getattr(other, other_attr): return -1
            return 0
        x, y, z = [[get_factor(self_attr, other_attr) for self_attr in "xyz"] for other_attr in "xyz"]
        if sum(map(abs, x + y + z)) == 3:
            # found a valid matrix, return it
            return [x, y, z]
        return None

    # rotate this point given a rotation matrix
    def rotate(self, rotation: List[List[int]]) -> "Point":
        return Point(
            self.x * rotation[0][0] + self.y * rotation[0][1] + self.z * rotation[0][2],
            self.x * rotation[1][0] + self.y * rotation[1][1] + self.z * rotation[1][2],
            self.x * rotation[2][0] + self.y * rotation[2][1] + self.z * rotation[2][2],            
        )

@dataclass
class Scanner:
    index: int
    beacons: List[Point]
    location: Point = None

    # set of distances between all beacons associated with the scanner
    # this allows for finding overlapping scanners
    @cached_property
    def distances(self) -> Set[int]:
        return set([a.distance(b) for a, b in combinations(self.beacons, 2)])

    # check whether this scanner overlaps with another scanner by at least 12 beacons
    def overlaps(self, other: "Scanner") -> bool:
        return len(self.distances & other.distances) > 12 * 3

    # calculate the shift and rotation that need to be applied to 
    # move this scanner into another scanner's frame of reference
    # then move this scanner accordingly
    def shift(self, other: "Scanner") -> "Scanner":
        # find likely candidates of beacons to try shifting around, in order of distance overlap
        sortkey = lambda pair: len(pair[0].neighbor_distances(self.beacons) & pair[1].neighbor_distances(other.beacons))
        candidates = [(beacon, other_beacon) for beacon in self.beacons for other_beacon in other.beacons]
        candidates = list(sorted(candidates, key=sortkey, reverse=True))
        # go through the candidate points
        for p1, p2 in zip(candidates, candidates[1:]):
            # try and generate a rotation matrix between them
            rotation = (p1[0] - p2[0]).rotation(p1[1] - p2[1])
            if rotation:
                # found it!
                # set the origin for this scanner to the offset vector
                self.location = candidates[0][1] - candidates[0][0].rotate(rotation)
                # adjust all beacons accordingly by rotating them and shifting them against the origin
                self.beacons = [beacon.rotate(rotation) + self.location for beacon in self.beacons]
                break

with open("input.txt", "r") as f:
    scanners = [list(map(lambda x: Point(*x), [[int(part) for part in coordinate.split(",")] \
        for coordinate in chunk.split("\n")[1:]])) \
            for chunk in f.read().split("\n\n")]
    scanners = list(map(lambda x: Scanner(x[0], x[1]), enumerate(scanners)))

# calculate which scanners overlap 
overlaps = [(a.index, b.index) for a, b in combinations(scanners, 2) if a.overlaps(b)]
# overlaps also work the other way around for solving, add those combinations
overlaps += [(y, x) for x, y in overlaps]

# choose scanner 0 as the frame of reference
# keep track of which other scanners have been adjusted relative to scanner 0, and which need work
adjusted = set([0])
need_adjustment = set(range(len(scanners))) - adjusted

# loop while scanners still need to be adjusted
while len(need_adjustment):
    # pull out all the scanners that can be solved based on what's been solved so far
    solvable = filter(lambda x: x[0] in adjusted and x[1] in need_adjustment, overlaps)
    for reference_index, index in solvable:
        # solve the pair
        result = scanners[index].shift(scanners[reference_index])
        # and record that fact
        need_adjustment.remove(index)
        adjusted.add(index)

# put all beacons from all scanners into a set and count it
beacons = reduce(lambda x, y: x | y, map(lambda x: set(x.beacons), scanners))
print(f"Solution 1: {len(beacons)}")

# set the origin of scanner 0 
scanners[0].location = Point(0, 0, 0)
# calculate all distances between scanners
distances = map(lambda x: x[0].location.manhattan(x[1].location), combinations(scanners, 2))
print(f"Solution 2: {max(distances)}")