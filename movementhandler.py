#movementhandler.py
import pygame
import eventhandler

def calcInputEvent(m_event,currentdir):
    direction = currentdir
    out_ev = None
    for event in m_event:
        if event.type == pygame.QUIT:
              return True
        if event.type == pygame.KEYDOWN:
            #direction = (0,0)
          if event.key == pygame.K_w:
            direction[1] = -1
          if event.key == pygame.K_s:
            direction[1] = 1
          if event.key == pygame.K_a:
            direction[0] = -1
          if event.key == pygame.K_d:
            direction[0] = 1
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_w or event.key == pygame.K_s:
            direction[1] = 0
          if event.key == pygame.K_a or event.key == pygame.K_d:
            direction[0] = 0
    return direction
