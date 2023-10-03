from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import ctypes
from wave_function import Wave
import argparse

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class App:
    def __init__(self, img_url, kernel_size, wave_width, wave_height, window_width, window_height, pixel_width):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.success = False

        self.pixel_width = pixel_width

        self.wave_function = None
        self.set_wave_function(img_url, kernel_size, wave_width, wave_height)

    def set_wave_function(self, img_url, kernel_size, wave_width, wave_height):
        self.wave_function = Wave(img_url, kernel_size, wave_width, wave_height)

    def reset_wave_function(self):
        self.wave_function.reset_wave()

    def draw_wave(self):
        for y, row in enumerate(self.wave_function.wave):
            for x, patch in enumerate(row):
                if len(patch.possible_ids) > 1:
                    continue
                pattern_id = list(patch.possible_ids)[0]
                color = self.wave_function.patterns[pattern_id][0][0]

                pygame.draw.rect(self.screen, color, pygame.Rect((x * self.pixel_width, y * self.pixel_width), (self.pixel_width, self.pixel_width)))
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
                if self.wave_function.propagate(min_pos):
                    self.draw_wave()
                    self.clock.tick(0)
                    continue
                else:
                    print("Fail")
                    self.reset_wave_function()
                    break
            
            self.draw_wave()

            self.clock.tick(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img_url", help="path for the image relative to the root of this project")
    parser.add_argument("kernel_size", type=int, help="size of the kernel")
    parser.add_argument("wave_width", type=int, help="width of the wave function")
    parser.add_argument("wave_height", type=int, help="height of the wave function")
    parser.add_argument("window_width", type=int, help="width of the pygame window")
    parser.add_argument("window_height", type=int, help="height of the pygame window")
    parser.add_argument("pixel_width", type=int, help="width of a pixel in the output image")
    args = parser.parse_args()

    app = App(args.img_url, args.kernel_size, args.wave_width, args.wave_height, args.window_width, args.window_height, args.pixel_width)
    app.run()