#!/usr/bin/env python3
"""Skylake cache hierarchy"""
from cachesim import Cache, MainMemory, CacheSimulator, CacheVisualizer

# =====================
# Intel Inclusive Cache
# =====================
cacheline_size = 64

mem = MainMemory()

l3 = Cache(name="L3",
           sets=22528, ways=11, cl_size=cacheline_size,
           replacement_policy="LRU",
           write_back=True, write_allocate=True,
           store_to=None, load_from=None, victims_to=None,
           swap_on_load=False)
mem.store_from(l3)

l2 = Cache(name="L2",
           sets=1024, ways=16, cl_size=cacheline_size,
           replacement_policy="LRU",
           write_back=True, write_allocate=True,
           store_to=l3, load_from=None, victims_to=l3,
           swap_on_load=False)
mem.load_to(l2)

l1 = Cache(name="L1",
           sets=64, ways=8, cl_size=cacheline_size,
           replacement_policy="LRU",
           write_back=True, write_allocate=True,
           store_to=l2, load_from=l2, victims_to=None,
           swap_on_load=False)  # inclusive/exclusive does not matter in first-level

cs = CacheSimulator(first_level=l1, main_memory=mem)

def parse_text_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            # Strip any extra whitespace and split by commas
            line = line.strip()
            if line:
                values = line.split(',')
                if len(values) == 5:
                    try:
                        # Extract and convert numeric values
                        isROI = int(values[0].strip())
                        isWrite = int(values[1].strip())
                        isStack = int(values[2].strip())
                        addr = int(values[3].strip(), 16)
                        length = int(values[4].strip())
                        if (isWrite == 0):
                            cs.load(addr = addr, stack = isStack, length = length)
                        elif (isWrite == 1):
                            cs.store(addr = addr, stack = isStack, length = length)
                    except ValueError as e:
                        print(f"Error processing line '{line}': {e}")
                else:
                    print(f"Ignoring line '{line}': Expected 5 values but got {len(values)}")

parse_text_file("pinatrace.out")

print(l1.stats())
print(l2.stats())
print(l3.stats())
#cv = CacheVisualizer(cs, [10, 16])
#cv.dump_state()
