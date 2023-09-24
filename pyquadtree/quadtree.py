from collections import deque
from .node import Node


def distance_sq_to_bbox(point, bbox):
    """
    Calculate the distance squared from a point to the nearest edge on the bounding box
    Will return 0 if the point is inside the bounding box
    :param point: The point
    :param bbox: The bounding box
    :return: The distance squared
    """
    minx, miny, maxx, maxy = bbox
    x, y = point

    """
    Calculating the distance_sq to the nearest edge of the bounding box
    For example if point A is below the bbox and between the left and right edges then its distance_sq is
    (y - maxy) ** 2
    It would look like
    
    +-----------------+ miny
    |                 |
    |                 |
    |                 |
    |                 |
    |                 |
    |                 |
    |                 |
    +-----------------+ maxy
    
            (A) at (x, y)
    
    As another example, if point B is to the right of the box but between the top and bottom edges then its distance_sq
    is (x - maxx) ** 2
    
    Finally, if point F is to the bottom right outside the box. Then its distance_sq is the distance to the corner
    (x - maxx) ** 2 + (y - maxy) ** 2
    Which is a combination of the two previous examples
    """
    distance_sq = 0
    if x < minx:
        distance_sq += (minx - x) ** 2
    elif x > maxx:
        distance_sq += (x - maxx) ** 2

    if y < miny:
        distance_sq += (miny - y) ** 2
    elif y > maxy:
        distance_sq += (y - maxy) ** 2

    # Notice that if the point is inside the bounding box then distance_sq will be 0 since all those cases will be
    # false

    return distance_sq


class Element:
    """
    A wrapper class for an element to be stored in the quadtree
    """

    def __init__(self, item, point: tuple):
        """
        :param item: Any object to be stored at a location
        :param point: The location of the item object
        """
        self.item = item
        self.point = point

    def __getitem__(self, index):
        """
        To allow the Element to be used as a tuple
        :param index: The index to get, 0 is point[0], 1 is point[1]
        """
        return self.point[index]

    def __len__(self):
        return len(self.point)

    def __eq__(self, other):
        return self.point == other.point and self.item == other.item


class QuadTree:
    def __init__(self, bbox: tuple, max_elements=10, max_depth=10):
        """
        :param bbox: The bounding box of the entire quadtree
        :param max_elements: The maximum number of points in a node before it splits
        :param max_depth: The maximum number of levels in the tree
        """

        # Maps for quick lookup of items and points by the other
        # Can be used to update the quadtree if the point of an item changes
        # or if the item of a point changes
        self.item_to_point_map = {}

        self.max_elements = max_elements
        self.max_depth = max_depth

        self.root = Node(bbox, depth=0, max_elements=max_elements, max_depth=max_depth)

        self.debug_elements_checked = []

    def add(self, item, point: tuple):
        """
        Insert an item into the quadtree at the location specified by point
        :param item: The item to store which can be any object
        :param point: A tuple with the x and y coordinate for the item
        """
        new_element = Element(item, point)

        self.item_to_point_map[item] = point

        return self.root.insert(new_element)

    def delete(self, item):
        """
        Delete an item from the quadtree
        Will restructure the quadtree if necessary, i.e. a parent node has less than max_elements
        :param item: The item to delete
        """
        point = self.item_to_point_map[item]
        element = Element(item, point)
        del self.item_to_point_map[item]
        self.root.delete(element)

    def query(self, bbox):
        """
        Query the quadtree for all elements within a bounding box
        Does not use recursion
        :param bbox: The bounding box to query (minx, miny, maxx, maxy)
        :return: A list of elements (maybe empty)
        """
        elements = []
        stack = deque()
        stack.append(self.root)

        while stack:
            node = stack.pop()
            if node.children:
                # Calculating which children intersect with the bbox

                # The order of the children is:
                # 0 | 2
                # -----
                # 1 | 3

                midx = (node.bbox[0] + node.bbox[2]) / 2
                midy = (node.bbox[1] + node.bbox[3]) / 2

                miny_less_than_midy = bbox[1] < midy
                maxy_greater_than_midy = bbox[3] > midy

                # If the bbox's minx is less than the node's midx
                # Checking children 0 and 1
                if bbox[0] < midx:
                    # If the bbox's miny is less than the node's midy
                    if miny_less_than_midy:
                        stack.append(node.children[0])

                    # If the bbox's maxy is greater than the node's midy
                    if maxy_greater_than_midy:
                        stack.append(node.children[1])

                # If the bbox's maxx is greater than the node's midx
                # We need to check for children 2 and 3
                if bbox[2] > midx:
                    # If the bbox's miny is less than the node's midy
                    if miny_less_than_midy:
                        stack.append(node.children[2])

                    # If the bbox's maxy is greater than the node's midy
                    if maxy_greater_than_midy:
                        stack.append(node.children[3])

            else:
                # If the node has no children, it must be a leaf
                # Adding all the elements within the query bounding box to the list
                elements.extend(element for element in node.elements if
                                bbox[0] <= element[0] < bbox[2] and bbox[1] <= element[1] < bbox[3])

        return elements

    def nearest_neighbors(self, point: tuple, condition=None, max_distance=float('inf'),
                          number_of_neighbors=1):
        """
        Finding the elements in the quadtree closest to the given point

        Uses a depth first search with branch pruning to find the nearest neighbor quickly

        :param point: The point to find the nearest neighbor for
                      You could also use this to find the nearest neighbor to an item by passing in the item's point
        :param condition: A function that takes in an element and returns True if it should be considered
                            False otherwise
        :param max_distance: The maximum distance to search for a point
        :param number_of_neighbors: The number of neighbors to find. Multiples the amount of time taken
                                    by the number of neighbors desired
        :return: List of the nearest neighbors found. len <= number_of_neighbors
        """

        # The closest elements found in order from closest to furthest
        # By the end of the search, this list will be number_of_neighbors long
        nearest_neighbors_found = []

        for _ in range(number_of_neighbors):

            nodes_to_check = [self.root]
            self.debug_elements_checked = []

            closest_element = None
            closest_distance_sq = max_distance ** 2

            distances_calculated = 0

            # Store the distance to the bounding box of each node to avoid recalculating it
            # When a node is added to the stack, its distance is calculated and stored here
            bbox_distance_memory = {}

            while len(nodes_to_check) > 0:
                node = nodes_to_check.pop()
                if node not in bbox_distance_memory:  # O(1) lookup to avoid recalculating the distance to the bbox
                    bbox_distance_memory[node] = distance_sq_to_bbox(point, node.bbox)

                if bbox_distance_memory[node] > closest_distance_sq:
                    # If the node is further than the closest point found so far, remove it from the stack
                    continue

                if node.children:
                    # Calculate the distance to the bounding box of each child
                    for child in node.children:
                        bbox_distance_memory[child] = distance_sq_to_bbox(point, child.bbox)

                    # Sort the children by distance to the point
                    sorted_children = sorted(node.children, key=lambda c: bbox_distance_memory[c], reverse=True)

                    for child in sorted_children:
                        # Only check the node if the box is close enough to have a point that is closer
                        if bbox_distance_memory[child] < closest_distance_sq:
                            nodes_to_check.append(child)
                else:
                    # This is a leaf node, check each element
                    for e in node.elements:
                        distance_sq = (point[0] - e[0]) ** 2 + (point[1] - e[1]) ** 2
                        distances_calculated += 1
                        self.debug_elements_checked.append(e)
                        if (distance_sq < closest_distance_sq and (condition is None or condition(e.item))
                                and e not in nearest_neighbors_found):
                            closest_distance_sq = distance_sq
                            closest_element = e

                bbox_distance_memory.pop(node)
            if closest_element:
                nearest_neighbors_found.append(closest_element)
        return nearest_neighbors_found

    def get_all_bbox(self):
        all_bbox = []
        self.root.get_bbox(all_bbox)
        return all_bbox

    def get_all_elements(self):
        all_elements = []
        for item in self.item_to_point_map.keys():
            all_elements.append(Element(item, self.item_to_point_map[item]))
        return all_elements
