# PyQuadTree  
A simple pure Python quadtree implementation.  
Supports fast query, insertion, deletion, and nearest neighbor search.

![thumbnail](https://github.com/Elan456/pyquadtree/assets/interactive.png)

## Installation

`pip install e-pyquadtree`


## Usage

### 1. Creating a QuadTree

`bbox` is a tuple of the form `(x1, y1, x2, y2)` where `(x1, y1)` is the top left corner of the bounding box and
`(x2, y2)` is the bottom right corner of the bounding box.  

`max_elements` is the maximum number of elements that can be stored in a node before it splits.  

`max_depth` is the maximum depth of the quadtree.
```python
from pyquadtree import QuadTree
quadtree = QuadTree(bbox=(0, 0, 1000, 500), max_elements=10, max_depth=5)
```

### 2. Adding elements to the QuadTree

The first argument is the object to store.
The second argument is a tuple of the form `(x, y)` where `(x, y)` is the location of the object in the bounding box.
The location must be within the bounding box of the quadtree.
```python
quadtree.add("apple", (100, 100))
```

### 3. Deleting elements from the QuadTree

The first argument is the object you want to delete from the quadtree.
It performs a lookup on the object and deletes it from the quadtree.
```python
quadtree.delete("apple")
```

### 4. Querying the QuadTree

The first argument is a tuple of the form `(x1, y1, x2, y2)` where `(x1, y1)` is the top left corner of the bounding box and
`(x2, y2)` is the bottom right corner of the bounding box.

Returns a list of elements within the bounding box.
Each element has an `item` and a `point` attribute.
These are the same as the arguments passed to `quadtree.add()`
when this element was added to the quadtree.
```python
found_elements = quadtree.query((50, 50, 150, 150))
```

### 5. Finding the nearest neighbor
Allows you to find the nearest n neighbors to a point.
The first argument is the point of interest.

There are a couple of optional arguments:
- `condition` is a function that takes in an item and returns a boolean.
  If the function returns `True`, the item is considered a valid neighbor.
  If the function returns `False`, the item is not considered a valid neighbor.
- `max_distance` is the maximum distance from the point of interest to a neighbor.
  If the distance between the point of interest and a neighbor is greater than `max_distance`,
  the neighbor is not considered a valid neighbor.
- `number_of_neighbors` is the number of neighbors to return.
  If `number_of_neighbors` is 1 by default.


```python
condition = lambda x: x == "apple"
neighbors = quadtree.nearest_neighbors((200, 100), condition=condition, max_distance=100, number_of_neighbors=3)
```

### 6. Drawing the tree
Calling  `get_all_bbox()` on the root node will return a flat list of all bounding boxes that make up the tree.
These can then be drawn using your favorite drawing library.
```python
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
```

## Example
```python
from pyquadtree import QuadTree

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
```

## Performance
The following performance tests were run on a quadtree with a maximum depth of 10 and
a maximum number of 20 elements per node.
The values are the number of seconds needed to both build the tree and then do 500 random queries.

pyqtree is an alternative pure Python quadtree implementation which can be found
[here](https://pypi.org/project/Pyqtree/). It was a big part in the inspiration
for this project. 


| Number of elements | Brute Force | pyquadtree (ours) | pyqtree |
|--------------------|-------------|-------------------|---------|
| 2000               | 0.057       | 0.029             | 0.032   |
| 4000               | 0.112       | 0.052             | 0.061   |
| 6000               | 0.165       | 0.097             | 0.1     |
| 8000               | 0.222       | 0.108             | 0.132   |
| 10000              | 0.273       | 0.13              | 0.163   |
| 12000              | 0.334       | 0.177             | 0.197   |
| 14000              | 0.405       | 0.2               | 0.241   |
| 16000              | 0.457       | 0.216             | 0.314   |
| 18000              | 0.504       | 0.282             | 0.334   |
| 20000              | 0.564       | 0.278             | 0.41    |
| 22000              | 0.623       | 0.359             | 0.458   |
| 24000              | 0.681       | 0.35              | 0.557   |
| 26000              | 0.73        | 0.425             | 0.592   |
| 28000              | 0.792       | 0.493             | 0.657   |
----------------------------------------------------------------

At 28000 elements, pyquadtree is 25% faster than pyqtree and 38% faster than brute force.
