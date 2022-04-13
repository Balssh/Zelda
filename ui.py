from turtle import back
import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 35, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self, current_ammount, max_ammount, background_rect, color):
        # draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, background_rect)

        # converting stat -> pixel
        ratio = current_ammount/max_ammount
        current_width = background_rect.width * ratio
        foreground_rect = background_rect.copy()
        foreground_rect.width = current_width

        # draw bar
        pygame.draw.rect(self.display_surface, color, foreground_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, background_rect, 3)

    def show_experience(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright = (self.display_surface.get_size()[0] - 25, self.display_surface.get_size()[1] - 25))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(25,25))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(25,25),3)
        
    def selection_box(self, left, top, has_switced):
        background_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, background_rect)
        if has_switced:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, background_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, background_rect, 3)
        return background_rect

    def weapon_overlay(self, weapon_index, has_switched):
        background_rect = self.selection_box(10, 630, has_switched)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center = background_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)


    def display(self, player):
       self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
       self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
       self.show_experience(player.experience)

       self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
       #self.selection_box(80, 635)
