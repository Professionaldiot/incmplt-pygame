import pygame

class button(pygame.sprite.Sprite):

    def __init__(self, pos, image_dir, surface, width = 200, height = 100):

        self.width = width
        self.height = height
        self.__x = pos[0]
        self.__y = pos[1]
        self.rect = pygame.Rect(pos[0], pos[1], 0.5, 0.5)
        self.image = pygame.image.load(image_dir)
        surface.blit(self.image, self.rect)

    def check_for_click(self, mouse_pos) -> bool:
        on_box = False
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        if (mouse_x > self.__x and mouse_x < self.__x + self.width) and mouse_y > self.__y and mouse_y < self.__y + self.height:
            on_box = True
        
        return on_box
