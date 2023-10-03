import pygame
import ctypes
from wave_function import Wave

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class App:
    def __init__(self, imgUrl, kernel_size, wave_width, wave_height, window_width, window_height):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.success = False

        self.wave_width = wave_width
        self.wave_height = wave_height

        self.wave_function = None
        self.set_wave_function(imgUrl, kernel_size, wave_width, wave_height)

    def set_wave_function(self, imgUrl, kernel_size, wave_width, wave_height):
        self.wave_function = Wave(imgUrl, kernel_size, wave_width, wave_height)

    def reset_wave_function(self):
        self.wave_function.reset_wave()

    def draw_wave(self, pixel_width):
        for y, row in enumerate(self.wave_function.wave):
            for x, patch in enumerate(row):
                if len(patch.possible_ids) > 1:
                    continue
                pattern_id = list(patch.possible_ids)[0]
                color = self.wave_function.patterns[pattern_id][0][0]

                pygame.draw.rect(self.screen, color, pygame.Rect((x * pixel_width, y * pixel_width), (pixel_width, pixel_width)))
        pygame.display.flip()    

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill("#222222")

            while not self.success:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                min_pos = self.wave_function.find_least_entropy()
                if min_pos == None:
                    print("Success")
                    self.success = True
                    break

                self.wave_function.collapse(min_pos[0], min_pos[1])
                if self.wave_function.propogate(min_pos):
                    self.draw_wave(10)
                    self.clock.tick(0)
                    continue
                else:
                    print("Fail")
                    self.reset_wave_function()
                    break
            
            self.draw_wave()

            self.clock.tick(60)

if __name__ == "__main__":
    app = App("./samples/Dungeon.png", 3, 80, 80, 800, 800)
    app.run()