import threading
import queue
import time
import sys

# Try importing pygame; if not present, this module will fail when used, which is expected.
try:
    import pygame
except ImportError:
    pygame = None

class KineticObject:
    def __init__(self, k_id, shape_type, color, x, y, width, height, radius=0):
        self.id = k_id
        self.shape_type = shape_type # 'Rectangle', 'Circle'
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius

class DisplayServer:
    """
    Runs on the Main Thread.
    Initialized by main.py.
    """
    def __init__(self):
        self.command_queue = queue.Queue()
        self.running = False
        self.window = None
        self.clock = None
        self.width = 800
        self.height = 600
        self.title = "Aetherium Display"
        self.objects = {} # Map id -> KineticObject
        self.background_color = (0, 0, 0) # Default Black

        # Color Map
        self.colors = {
            'Black': (0, 0, 0),
            'White': (255, 255, 255),
            'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Blue': (0, 0, 255),
            'Gray': (128, 128, 128),
            'Copper': (184, 115, 51)
        }

    def start_loop(self):
        """
        Blocking call that runs the Pygame event loop.
        Only returns when the application quits.
        """
        self.running = True

        while self.running:
            # 1. Process Queue
            try:
                while True:
                    cmd = self.command_queue.get_nowait()
                    self.process_command(cmd)
            except queue.Empty:
                pass

            # 2. Process Pygame Events
            if self.window:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        # We should also signal the Logic Thread to stop if possible?
                        # For now, we just close the window.
                        sys.exit(0)

                # 3. Draw
                self.window.fill(self.background_color)

                for obj in self.objects.values():
                    self.draw_object(obj)

                pygame.display.flip()

                if self.clock:
                    self.clock.tick(60) # Limit to 60 FPS
            else:
                # If window not open yet, sleep a bit to save CPU
                time.sleep(0.1)

        if self.window:
            pygame.quit()

    def process_command(self, cmd):
        msg_type = cmd.get('type')

        if msg_type == 'INIT_WINDOW':
            if pygame:
                pygame.init()
                self.width = cmd.get('width', 800)
                self.height = cmd.get('height', 600)
                self.title = cmd.get('title', "Aetherium")
                self.window = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption(self.title)
                self.clock = pygame.time.Clock()

        elif msg_type == 'REGISTER_KINETIC':
            # Create a new object entry
            k_id = cmd['id']
            obj = KineticObject(
                k_id,
                cmd['shape'],
                cmd['color'],
                cmd['x'], cmd['y'],
                cmd.get('width', 0),
                cmd.get('height', 0),
                cmd.get('radius', 0)
            )
            self.objects[k_id] = obj

        elif msg_type == 'UPDATE_STATE':
            # Batch update from Render
            updates = cmd['updates'] # List of dicts
            for up in updates:
                k_id = up['id']
                if k_id in self.objects:
                    tgt = self.objects[k_id]
                    if 'x' in up: tgt.x = up['x']
                    if 'y' in up: tgt.y = up['y']
                    # Could update color etc too

        elif msg_type == 'QUIT':
            self.running = False

    def draw_object(self, obj):
        color_rgb = self.colors.get(obj.color, (255, 255, 255))

        if obj.shape_type == 'Rectangle':
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            pygame.draw.rect(self.window, color_rgb, rect)
        elif obj.shape_type == 'Circle':
            # Pygame circle draws at center?
            # Aetherium spec doesn't say. Assuming center or top-left.
            # Usually graphics draw from top-left.
            # For circle, usually center.
            # Let's assume (x,y) is center for Circle.
            pygame.draw.circle(self.window, color_rgb, (int(obj.x), int(obj.y)), int(obj.radius))

# Global Singleton for Client access
# The server instance is held in main.py, but we can access the queue via Client.
# Wait, Client needs access to the SAME queue object that Server uses.
# Since we are in the same process, we can share a module-level variable or pass it.
# Ideally, we pass it. But Syntax Modules are instantiated by Loader/Engine.
# Dependency Injection is hard here.
# We will use a singleton pattern here.

_server_queue = None

def init_server():
    global _server_queue
    server = DisplayServer()
    _server_queue = server.command_queue
    return server

def get_queue():
    return _server_queue

class DisplayClient:
    @staticmethod
    def open_display(width, height, title):
        q = get_queue()
        if q:
            q.put({
                'type': 'INIT_WINDOW',
                'width': width,
                'height': height,
                'title': title
            })
            return "CANVAS_HANDLE" # Dummy handle
        return None

    @staticmethod
    def register_kinetic(k_id, shape, color, x, y, **kwargs):
        q = get_queue()
        if q:
            msg = {
                'type': 'REGISTER_KINETIC',
                'id': k_id,
                'shape': shape,
                'color': color,
                'x': x,
                'y': y
            }
            msg.update(kwargs)
            q.put(msg)

    @staticmethod
    def render_updates(updates):
        """
        updates: List of {'id': ..., 'x': ..., 'y': ...}
        """
        q = get_queue()
        if q:
            q.put({
                'type': 'UPDATE_STATE',
                'updates': updates
            })

    @staticmethod
    def signal_quit():
        q = get_queue()
        if q:
            q.put({'type': 'QUIT'})
