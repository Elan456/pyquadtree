import time
import random
from pyquadtree.quadtree import QuadTree
from pyqtree import Index as pyqtree_index
from matplotlib import pyplot as plt
from tqdm import tqdm


def nearest_neighbor():
    experiments = [i for i in range(100, 15000, 50)]

    qtree_times = []
    brute_force_times = []
    labels = []

    for experiment in tqdm(experiments):
        labels.append(str(experiment))
        points = []
        for i in range(experiment):
            points.append((random.randint(0, 1000), random.randint(0, 1000)))

        # QUADTREE
        start_time = time.time()
        qtree = QuadTree((0, 0, 1000, 1000), 5, 10)
        for point in points:
            qtree.add(point)

        # Get nearest neighbor for each point
        for point in points:
            qtree.nearest_neighbors(point)
        qtree_time = time.time() - start_time
        qtree_times.append(qtree_time)

        # BRUTE FORCE
        # start_time = time.time()
        # for point in points:
        #     min_dist = float("inf")
        #     for other_point in points:
        #         if point == other_point:
        #             continue
        #         dist = (point[0] - other_point[0]) ** 2 + (point[1] - other_point[1]) ** 2
        #         if dist < min_dist:
        #             min_dist = dist
        #
        # brute_force_time = time.time() - start_time
        # brute_force_times.append(brute_force_time)

    plt.title("Nearest Neighbor Performance")
    plt.plot(labels, qtree_times, label="Quadtree")
    #    plt.plot(labels, brute_force_times, label="Brute Force")
    plt.xlabel("Number of points")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()

    print(qtree_times)
    print(brute_force_times)
    print(labels)

    # Plotting a to scale scatter plot of the points
    plt.title("Nearest Neighbor Performance")
    # plt.scatter(experiments, brute_force_times , label="Brute Force")
    plt.scatter(experiments, qtree_times, label="Quadtree")
    plt.xlabel("Number of points")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()


def tree_building():
    experiments = [i for i in range(100, 20000, 500)]
    ours_times = []
    pyqtree_times = []

    for experiment in tqdm(experiments):
        points = [(random.randint(0, 1000), random.randint(0, 1000)) for i in range(experiment)]

        # OUR
        start_time = time.time()
        qtree = QuadTree((0, 0, 1000, 1000), 10, 30)
        for point in points:
            qtree.add(None, point)
        ours_time = time.time() - start_time

        # PYQTREE
        start_time = time.time()
        pyqtree = pyqtree_index(bbox=(0, 0, 1000, 1000), max_items=10, max_depth=30)
        for point in points:
            pyqtree.insert(None, bbox=(point[0], point[1], point[0], point[1]))
        pyqtree_time = time.time() - start_time

        ours_times.append(ours_time)
        pyqtree_times.append(pyqtree_time)

    plt.title("Tree Building Performance")
    plt.plot(experiments, ours_times, label="Ours")
    plt.plot(experiments, pyqtree_times, label="Pyqtree")
    plt.xlabel("Number of points")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()


def area_query():
    MAX_DEPTH = 10
    MAX_POINTS = 5

    experiments = [i for i in range(0, 30000, 1000)]

    ours_times = []
    pyqtree_times = []

    queries = []
    for i in range(500):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        width = random.randint(0, 1000 - x)
        height = random.randint(0, 1000 - y)
        queries.append((x, y, x + width, y + height))

    for experiment in tqdm(experiments):
        points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(experiment)]
        # OUR
        # print("     our_r")
        qtree = QuadTree((0, 0, 1000, 1000), MAX_POINTS, MAX_DEPTH)
        for point in points:
            qtree.add(None, point)

        start_time = time.time()
        for query in queries:
            found_points = qtree.query(query)
            # print(len(found_points))
        ours_times.append(time.time() - start_time)

        # PYQTREE
        # print("pyqtree")
        pyqtree = pyqtree_index(bbox=(0, 0, 1000, 1000), max_items=MAX_POINTS, max_depth=MAX_DEPTH)
        for point in points:
            pyqtree.insert(point, bbox=(point[0], point[1], point[0] + 1, point[1] + 1))

        start_time = time.time()
        for query in queries:
            found_points = pyqtree.intersect(query)
            # print(len(found_points))

        pyqtree_times.append(time.time() - start_time)

    plt.title("Area Query Performance" + " (Max Depth: " + str(MAX_DEPTH) + ", Max Points: " + str(MAX_POINTS) + ")" )
    plt.plot(experiments, ours_times, label="Ours")
    plt.plot(experiments, pyqtree_times, label="Pyqtree")

    plt.xlabel("Number of points")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()


def area_query_and_tree_building():
    MAX_DEPTH = 10
    MAX_POINTS = 20

    experiments = [i for i in range(0, 30000, 2000)]
    brute_force_times = []
    ours_times = []
    pyqtree_times = []

    queries = []
    for i in range(500):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        width = random.randint(0, 1000 - x)
        height = random.randint(0, 1000 - y)
        queries.append((x, y, x + width, y + height))

    for experiment in tqdm(experiments):
        points = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(experiment)]

        # BRUTE FORCE
        # print("brute force")
        start_time = time.time()
        for query in queries:
            found_points = []
            for point in points:
                if query[0] <= point[0] <= query[2] and query[1] <= point[1] <= query[3]:
                    found_points.append(point)
            # print(len(found_points))
        brute_force_times.append(time.time() - start_time)

        # OUR
        # print("     our_r")
        start_time = time.time()
        qtree = QuadTree((0, 0, 1000, 1000), MAX_POINTS, MAX_DEPTH)
        for point in points:
            qtree.add(None, point)
        for query in queries:
            found_points = qtree.query(query)
            # print(len(found_points))
        ours_times.append(time.time() - start_time)

        # PYQTREE
        # print("pyqtree")
        start_time = time.time()
        pyqtree = pyqtree_index(bbox=(0, 0, 1000, 1000), max_items=MAX_POINTS, max_depth=MAX_DEPTH)
        for point in points:
            pyqtree.insert(point, bbox=(point[0], point[1], point[0] + 1, point[1] + 1))
        for query in queries:
            found_points = pyqtree.intersect(query)
            # print(len(found_points))
        pyqtree_times.append(time.time() - start_time)

    plt.title("Tree Building and Query Performance" + " (Max Depth: " + str(MAX_DEPTH) + ", Max Points: " + str(MAX_POINTS) + ")" )
    plt.plot(experiments, ours_times, label="Ours")
    plt.plot(experiments, pyqtree_times, label="Pyqtree")
    plt.plot(experiments, brute_force_times, label="Brute Force")
    plt.xlabel("Number of points")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()

    # Printing the results in a nice way that can be copied into a markdown table
    print("| Experiment | Brute Force | pyquadtree | Pyqtree |")
    for i in range(len(experiments)):
        print("| " + str(experiments[i]) + " | " + str(round(brute_force_times[i], 3)) + " | " + str(round(ours_times[i], 3)) + " | " + str(round(pyqtree_times[i], 3)) + " |")


# tree_building()
# area_query()
area_query_and_tree_building()
