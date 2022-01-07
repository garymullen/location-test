import pygame
from multiprocessing.connection import Client
import cmath

class Envir:
    def __init__(self, dimensions):
        self.black = (0,0,0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.robots = []
        self.anchors = []
        self.transmitter = None

        self.height,self.width=dimensions
        pygame.display.set_caption("Input Window")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def add_robot(self, robot):
        self.robot=robot

    def add_anchor(self, location):
        self.anchors.append(location)

    def draw_robot(self, robot):
        pygame.draw.rect(self.map, robot.color, robot.rect)

    def distance(self, a, b):
        px = (float(a[0]) - float(b[0])) ** 2
        py = (float(a[1]) - float(b[1])) ** 2
        return (px + py) ** (0.5)
    
    def calc_position(self, a, b, c):
        cos_a = (b*b + c*c - a*a) / (2 * b * c)
        x = (b * cos_a) + self.anchors[0][0]
        y = (b * cmath.sqrt(1 - cos_a*cos_a)) + self.anchors[0][1]
        y2 = cmath.sqrt(b*b-x*x) + self.anchors[0][1]
        return round(x.real, 1), round(y.real, 1)
    
    def update_map(self):
        self.map.fill(self.white)
        self.draw_robot(robot)
        if robot.x != robot.rect.x or robot.y != robot.rect.y:
            robot.x = robot.rect.x
            robot.y = robot.rect.y
            distanceA = self.distance(self.anchors[0],(robot.x,robot.y))
            distanceB = self.distance(self.anchors[1],(robot.x,robot.y))
            print(f"Robot location ({robot.x},{robot.y})")
            print(f"distance A: {distanceA}, distance B {distanceB})")
            calc_x,calc_y = self.calc_position(distanceB, distanceA, distanceBetweenAchors)
            print(f"Calculated X,Y: {calc_x},{calc_y})")
            print()
            self.transmitter.send({ "distances": {"anchorA": distanceA, "anchorB": distanceB, "betweenAB": distanceBetweenAchors}})
        for anchor in self.anchors:
            pygame.draw.circle(self.map, self.yellow, anchor, 7, 0)
        
        pygame.display.update()
        self.clock.tick(25)


class Robot:
    def __init__(self, location, size, color):
        self.start = location
        self.size = size
        self.color = color
        self.rect = pygame.Rect(location[0], location[1], size, size )
        self.x,self.y = location

class Transmitter:
    def __init__(self) -> None:
        self.authkey = b'blahblah'
        self.address = ('localhost', 6000)

    def send(self,data):
        try:
            conn = Client(self.address, authkey=self.authkey)
            conn.send(data)
            conn.close()
        except:
            pass

 
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 400

START_LOCATION = (200,200)
 
BLOCK_SIZE = 30

pygame.init()

env = Envir((SCREEN_HEIGHT, SCREEN_WIDTH))

robot = Robot(START_LOCATION, BLOCK_SIZE, env.red)

transmitter = Transmitter()

env.add_robot(robot)
env.transmitter = transmitter
env.add_anchor((10,10))
env.add_anchor((SCREEN_WIDTH-10,10))

distanceBetweenAchors = env.distance(env.anchors[0],env.anchors[1])
print("Anchors: ",env.anchors[0],env.anchors[1])
print("Distance between anchors: ", distanceBetweenAchors)

selected = None
is_running = True
 
while is_running:
 
    # --- events ---
   
    for event in pygame.event.get():
 
        # --- global events ---
       
        if event.type == pygame.QUIT:
            is_running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                r = env.robot.rect
                if r.collidepoint(event.pos):
                    selected = True
                    selected_offset_x = r.x - event.pos[0]
                    selected_offset_y = r.y - event.pos[1]
               
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected = None
               
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None: # selected can be `0` so `is not None` is required
                # move object
                env.robot.rect.x = event.pos[0] + selected_offset_x
                env.robot.rect.y = event.pos[1] + selected_offset_y
   
    env.update_map()
 
pygame.quit()