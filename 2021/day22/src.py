import sys
from dataclasses import dataclass
from typing import List, Tuple

with open("input_test.txt", "r") as f:
    instructions = []
    for l in f:
        state, coordinates = l.split(" ")
        dimensions = coordinates.rstrip().split(",")
        instructions.append((state, tuple(map(lambda x: tuple(map(int, x.split("=")[1].split(".."))), dimensions))))

def expand_coordinates(region, cutoff=None):
    def normalize(val):
        if not cutoff: return val
        if val < -1 * cutoff: return -1 * cutoff
        elif val > cutoff:return cutoff
        else: return val
    x_range, y_range, z_range = map(lambda x: (normalize(x[0]), normalize(x[1] + 1)), region)
    return set([(x, y, z) for x in range(*x_range) for y in range(*y_range) for z in range(*z_range)])

#lit = set()
#for state, region in instructions:
#    if state == "on": lit.update(expand_coordinates(region, 50))
#    else: lit = lit - expand_coordinates(region, 50)
#
#print(f"Solution 1: {len(lit)}")

@dataclass
class Cuboid:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int
    is_null: bool = False

    def __repr__(self):
        return f"{self.x_min}..{self.x_max},{self.y_min}..{self.y_max},{self.z_min}..{self.z_max}"

    def __eq__(self, other: "Cuboid") -> bool:
        return self.x_min == other.x_min and self.x_max == other.x_max and \
                self.y_min == other.y_min and self.y_max == other.y_max and \
                self.z_min == other.z_min and self.z_max == other.z_max

    # count cubes within the cuboid
    def count(self) -> int:
        cubes = ((self.x_max - self.x_min) + 1) * ((self.y_max - self.y_min) + 1) * ((self.z_max - self.z_min) + 1)
        # if cube is a null cube, return the negative of the number of cubes
        return cubes if not self.is_null else -1 * cubes

    # check whether one cuboid entirely contains another
    def contains(self, other: "Cuboid") -> bool:
        return (self.x_min <= other.x_min <= self.x_max) and (self.x_min <= other.x_max <= self.x_max) \
                and (self.y_min <= other.y_min <= self.y_max) and (self.y_min <= other.y_max <= self.y_max) \
                and (self.z_min <= other.z_min <= self.z_max) and (self.z_min <= other.z_max <= self.z_max)
    
    # check if two cuboids overlap 
    def overlaps(self, other: "Cuboid") -> bool:
        return ((self.x_min <= other.x_min <= self.x_max) or (self.x_min <= other.x_max <= self.x_max)) \
                and ((self.y_min <= other.y_min <= self.y_max) or (self.y_min <= other.y_max <= self.y_max)) \
                and ((self.z_min <= other.z_min <= self.z_max) or (self.z_min <= other.z_max <= self.z_max))

    # subtract one cuboid from one another
    # this is done by returning a cube that represents the overlap, with null set to true
    # those will later be counted as off
    def subtract(self, other: "Cuboid") -> List["Cuboid"]:
        # four possibilities:
        # the cuboids do not overlap at all, no null cube to return
        if not self.overlaps(other):
            return []
        # the first cuboid is entirely contained by the second cuboid, return self as null
        if other.contains(self):
            return [Cuboid(self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max, is_null=True)]
        # the first cuboid entirely contains the second cuboid, return other as null
        if self.contains(other):
            return [Cuboid(other.x_min, other.x_max, other.y_min, other.y_max, other.z_min, other.z_max, is_null=True)]
        # or the two overlap without entirely containing each other, find the overlap and make a new null cube from it
        null_x_min = max(self.x_min, other.x_min)
        null_x_max = min(self.x_max, other.x_max)
        null_y_min = max(self.y_min, other.y_min)
        null_y_max = min(self.y_max, other.y_max)
        null_z_min = max(self.z_min, other.z_min)
        null_z_max = min(self.z_max, other.z_max)
        return [Cuboid(null_x_min, null_x_max, null_y_min, null_y_max, null_z_min, null_z_max, is_null=True)]


#c = Cuboid(10, 12, 10, 12, 10, 12)
#d = Cuboid(11, 13, 11, 13, 11, 13)
#
#overlap = c.subtract(d)
#
#c_c = c.count()
#d_c = d.count()
#o_c = overlap[0].count() if len(overlap) else 0
#
#print(f"total = {c_c} + {o_c} = {c_c + o_c}")
#
#sys.exit(0)

cuboids = []
for state, region in instructions:
    null_cuboids = []
    if state == "on":
        cuboid = Cuboid(*region[0], *region[1], *region[2])
        for c in cuboids: 
            null_cuboids.extend(c.subtract(cuboid))
        cuboids.append(cuboid)
    else:
        cuboid = Cuboid(*region[0], *region[1], *region[2], is_null=True)
        for c in cuboids: 
            null_cuboids.extend(c.subtract(cuboid))
    cuboids.extend(null_cuboids)
    null_cuboids = []

result = sum(map(lambda x: x.count(), cuboids))
print(f"Solution 2: {result}")


sys.exit(0)

# construct a list of all regions of spaces that should be turned on
cuboids = []
for state, region in instructions:
    # create the cuboid that maps to that region
    new_cuboid = Cuboid(*region[0], *region[1], *region[2])
    # go through all existing cuboids
    if state == "on":
        for existing in cuboids:
            # subtract the new cuboid from all existing ones so it doesn't get double counted
            new_cuboids.extend(existing.subtract(new_cuboid))
        # add the new cuboid
        new_cuboids.append(new_cuboid)
    else:
        # turning off, simply subtract this region from all existing cuboids
        for existing in cuboids:
            new_cuboids.extend(existing.subtract(new_cuboid))
    cuboids = new_cuboids

# count the cubes within the regions that should be turned on
result = sum(map(lambda x: x.count(), cuboids))
print(f"Solution 2: {result}")
