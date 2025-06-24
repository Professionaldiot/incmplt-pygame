import pygame

class button(pygame.sprite.Sprite):

    def __init__(self, pos, image_name, surface, mouse_pos, clicking, action_ind, width = 200, height = 100):
        #action is the index of the screen to go to next
        self.width = width
        self.height = height
        self.__x = pos[0]
        self.__y = pos[1]
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.__action_ind = 0

        self.image = pygame.image.load(image_name + self.draw_box(self.check_for_click(mouse_pos)))
        surface.blit(self.image, self.rect)
        if clicking and self.check_for_click(mouse_pos):
            self.__action_ind = action_ind
    
    def get_action_ind(self):
        return self.__action_ind

    def check_for_click(self, mouse_pos) -> bool:
        on_box = False
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        if (mouse_x > self.__x and mouse_x < self.__x + self.width) and (mouse_y > self.__y and mouse_y < self.__y + self.height):
            on_box = True
        
        return on_box
    
    def draw_box(self, on_box = False) -> str:
        if on_box:
            return "_dark.png"
        return ".png"