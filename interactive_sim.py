from pyquadtree import QuadTree
import pygame
import random

screen = pygame.display.set_mode((1000, 1000))

# Create a quadtree with a bounding box of (0, 0, 800, 600)
# and a maximum of 10 points per node and a maximum depth of 10
qtree = QuadTree((0, 0, 1000, 1000), 10, 2)


def draw_quadtree(tree):
    bboxs = tree.get_all_bbox()
    for bbox in bboxs:
        rect = (bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1])
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xv = int(random.uniform(-5, 5))
        self.yv = int(random.uniform(-5, 5))
        self.radius = random.randint(3, 20)
        self.neighbor = None

    def out_of_bounds_bounce(self):
        if self.x < 0 or self.x > 1000:
            self.xv *= -1
        if self.y < 0 or self.y > 1000:
            self.yv *= -1

    def update(self):
        self.x += self.xv
        self.y += self.yv
        self.out_of_bounds_bounce()

    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)
        if self.neighbor:
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), self.neighbor, width=2)


def interactive_test():
    query_area = [0, 0, 150, 150]
    query_area_speed = 4

    fun_balls = [Ball(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(50)]
    for ball in fun_balls:
        qtree.add(ball, (ball.x, ball.y))

    clock = pygame.time.Clock()
    while True:
        for ball in fun_balls:
            qtree.delete(ball)
            ball.update()
            ball.neighbor = qtree.nearest_neighbors((ball.x, ball.y))[0]
            qtree.add(ball, (ball.x, ball.y))

        closest_to_mouse = qtree.nearest_neighbors(pygame.mouse.get_pos(), condition=lambda x: x.radius > 5,
                                                   number_of_neighbors=2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                qtree.add(Ball(x, y), (x, y))
                # print("New total number of nodes: ", len(qtree.get_all_bbox()))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if closest_to_mouse:
                    qtree.delete(closest_to_mouse[0].item)

        # If right arrow down, move the query area to the right
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            query_area[0] += query_area_speed
            query_area[2] += query_area_speed
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            query_area[0] -= query_area_speed
            query_area[2] -= query_area_speed
        if pygame.key.get_pressed()[pygame.K_UP]:
            query_area[1] -= query_area_speed
            query_area[3] -= query_area_speed
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            query_area[1] += query_area_speed
            query_area[3] += query_area_speed

        # Draw the quadtree
        draw_quadtree(qtree)

        # Draw the query area
        rect = (query_area[0], query_area[1], query_area[2] - query_area[0], query_area[3] - query_area[1])
        pygame.draw.rect(screen, (255, 0, 255), rect, 1)

        for item in qtree.item_to_point_map.keys():
            item.draw()

        for e in closest_to_mouse:
            pygame.draw.circle(screen, (255, 0, 0), e, 10, width=2)

        for point in qtree.debug_elements_checked:
            pygame.draw.circle(screen, (0, 0, 255), point, 2)

        for point in qtree.query(query_area):
            pygame.draw.circle(screen, (255, 0, 255), point, 5, 2)

        for point in qtree.query(query_area):
            pygame.draw.circle(screen, (255, 0, 255), point, 5, 2)

        pygame.display.update()
        screen.fill((0, 0, 0))
        clock.tick(60)
        fps = clock.get_fps()
        pygame.display.set_caption(f"FPS: {fps}")


interactive_test()
# nearest_neighbor_test()
