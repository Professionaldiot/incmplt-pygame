#this class will serve the function of creating text boxes at position (x, y) with text "text" and will render it in pygame

import pygame

class text_box:

    def __init__(self, x, y, width, height, text):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__text = text

    def update_text(self, new_text):
        self.__text = new_text
    
    def get_text_len(self):
        return len(self._text)
    
    def get_text(self):
        return self.__text

    def check_mouse_pos(self, pos):
        #checks if the mouse position is in the text box
        m_x = pos[0]
        m_y = pos[1]
        
        if (m_x > self.__x and m_x < self.__x + self.__width) and (m_y > self.__y and m_y < self.__y + self.__height):
            return True
        return False