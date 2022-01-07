import cmath
import pygame
from multiprocessing.connection import Client
from multiprocessing.connection import Listener

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
        pygame.display.set_caption("Output Window")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def add_robot(self, robot):
        self.robot=robot

    def add_anchor(self, location):
        self.anchors.append(location)

    def draw_robot(self, robot):
        pygame.draw.rect(self.map, robot.color, robot.rect)

    def calc_position(self, a, b, c):
        cos_a = (b*b + c*c - a*a) / (2 * b * c)
        x = (b * cos_a) + self.anchors[0][0]
        y = (b * cmath.sqrt(1 - cos_a*cos_a)) + self.anchors[0][1]
        return round(x.real, 1), round(y.real, 1)
    
    def update_map(self):
        self.map.fill(self.white)
        self.draw_robot(robot)
        if robot.x != robot.rect.x or robot.y != robot.rect.y:
            robot.x = robot.rect.x
            robot.y = robot.rect.y
            # print(f"Robot location ({robot.x},{robot.y})")
        for anchor in self.anchors:
            pygame.draw.circle(self.map, self.yellow, anchor, 7, 0)
        
        # self.transmitter.send({ "robot": [robot.x, robot.y]})
        pygame.display.update()
        self.clock.tick(25)


class Robot:
    def __init__(self, location, size, color):
        self.start = location
        self.size = size
        self.color = color
        self.rect = pygame.Rect(location[0], location[1], size, size )
        self.x,self.y = location

class Receiver:
    def __init__(self) -> None:
        self.authkey = b'blahblah'
        self.address = ('localhost', 6000)

    def receive_data(self):
        data=None
        with Listener(self.address, authkey=self.authkey) as listener:
            # listen=True
            # while listen:
            listener._listener._socket.settimeout(0.1)
            try:
                with listener.accept() as conn:
                    # print('connection accepted from ', listener.last_accepted, flush=True)
                    while True:
                        try:
                            data = conn.recv()
                        except EOFError:
                            conn.close()
                            break
                        # else:    
                            # print("Received: ", data)
            except:
                # print("socket timeout")
                data=None
            listener.close()
        return data
 
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 400

START_LOCATION = (200,200)
 
BLOCK_SIZE = 30

pygame.init()

env = Envir((SCREEN_HEIGHT, SCREEN_WIDTH))

robot = Robot(START_LOCATION, BLOCK_SIZE, env.red)

receiver = Receiver()

env.add_robot(robot)
# env.transmitter = transmitter
env.add_anchor((10,10))
env.add_anchor((SCREEN_WIDTH-10,10))

selected = None
is_running = True
 
while is_running:
    data = None
    for event in pygame.event.get():
 
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
 
    data = receiver.receive_data()
    if data is not None:
        print("DATA: ", data)
        distA = data["distances"]["anchorA"]
        distB = data["distances"]["anchorB"]
        betweenAB = data["distances"]["betweenAB"]
        x,y = env.calc_position(distB, distA, betweenAB)
        robot.rect.x = x
        robot.rect.y = y
   
    env.update_map()
 
pygame.quit()