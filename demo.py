from pyquadtree import QuadTree
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

quadtree = QuadTree(bbox=(0, 0, 1000, 500), max_elements=10, max_depth=5)
for i in range(100):
    quadtree.add(i, (random.randint(0, 100), random.randint(0, 500)))

all_bbox = quadtree.get_all_bbox()
fig, ax = plt.subplots()
ax.set_xlim(0, 1000)
ax.set_ylim(0, 500)
for bbox in all_bbox:
    print(bbox)
    rectangle = Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1], fill=False,
                          edgecolor="r", linewidth=1)
    ax.add_patch(rectangle)
plt.show()

exit()
# Creating a quadtree from (0, 0) to (1000, 500)
# It will have a maximum depth of 5 and a maximum number of 10 objects per node
quadtree = QuadTree(bbox=(0, 0, 1000, 500), max_elements=10, max_depth=5)

# Inserting a string object with a location of (100, 100)
quadtree.add("apple", (100, 100))

# Inserting another string object with a location of (200, 50)
quadtree.add("orange", (200, 50))

# Querying the quadtree for all objects in the bounding box (50, 50, 150, 150)
# Returns the list of elements within the bounding box
found_elements = quadtree.query((50, 50, 150, 150))

for element in found_elements:
    print(element.point, element.item)  # (100, 100) apple

# Finding the element nearest to (200, 100)
nearest_neighbor = quadtree.nearest_neighbors((200, 100))[0]
print(nearest_neighbor.point, nearest_neighbor.item)  # (200, 50) orange

# Getting a list all elements in the quadtree
all_elements = quadtree.get_all_elements()
for element in all_elements:
    print(element.point, element.item)  # (100, 100) apple, (200, 50) orange
