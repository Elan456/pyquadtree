"""
Node class for the quadtree
Contains the bounding box, elements, and children

Used to store elements and will divide if the number of elements exceeds the max_elements
"""


class Node:
    def __init__(self, bbox: tuple, depth, max_elements, max_depth):
        """
        :param bbox: tuple with minx, miny, maxx, maxy
        """
        self.bbox = bbox
        self.elements = []
        self.children = []
        self.depth = depth
        self.max_elements = max_elements
        self.max_depth = max_depth

        # Inserts an element into the correct child node
        self.insert_child = lambda element: self.children[
            2 * (element[0] > ((self.bbox[0] + self.bbox[2]) / 2)) + (element[1] > ((self.bbox[1] + self.bbox[3]) / 2))
            ].insert(element)

        # Deletes an element from the correct child node
        self.delete_child = lambda element: self.children[
            2 * (element[0] > ((self.bbox[0] + self.bbox[2]) / 2)) + (element[1] > ((self.bbox[1] + self.bbox[3]) / 2))
            ].delete(element)

    def insert(self, element):
        """
        Insert an element into the node
        Will split the node if it has too many elements
        :param element: The element to store
        """
        if not self.children:
            self.elements.append(element)
            if len(self.elements) > self.max_elements and self.depth < self.max_depth:
                self.split()
        else:
            # Child insert
            self.insert_child(element)

    def delete(self, element):
        """
        Delete an element from the node
        If it doesn't have this element, then it checks a child node
        :param element: The element to delete

        :return: True if the element was deleted, False otherwise
        """
        if not self.children:
            for e in self.elements:
                if e == element:
                    self.elements.remove(element)
                    return True
        else:
            if self.delete_child(element):
                count = 0  # How many elements are in my children
                for child in self.children:
                    if not child.children:
                        count += len(child.elements)
                    else:
                        # If any of my children have children, then there must be too many elements
                        return False
                if count <= self.max_elements:
                    self.merge()

    def split(self):
        """
        Split the node into four sub-nodes
        """
        minx, miny, maxx, maxy = self.bbox
        midx = (minx + maxx) / 2
        midy = (miny + maxy) / 2

        self.children = []

        self.children.append(Node((minx, miny, midx, midy), self.depth + 1, self.max_elements, self.max_depth))
        self.children.append(Node((minx, midy, midx, maxy), self.depth + 1, self.max_elements, self.max_depth))
        self.children.append(Node((midx, miny, maxx, midy), self.depth + 1, self.max_elements, self.max_depth))
        self.children.append(Node((midx, midy, maxx, maxy), self.depth + 1, self.max_elements, self.max_depth))

        for element in self.elements:
            # Child insert
            self.insert_child(element)
        self.elements = []

    def merge(self):
        """
        Take all the elements from my children and add them to me
        Also remove my children
        """
        for child in self.children:
            self.elements.extend(child.elements)
        self.children = []

    def get_bbox(self, all_bbox):
        all_bbox += [self.bbox]
        for child in self.children:
            child.get_bbox(all_bbox)

    def __str__(self):
        return str(self.depth) + "-" + str(self.bbox)
