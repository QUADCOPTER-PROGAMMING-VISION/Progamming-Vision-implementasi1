import pygame
pygame.init()
win = pygame.display.set_mode((480, 600))  # Jendela pygame kecil

def getKey(keyName):
    pygame.event.pump()  # Pastikan event pygame diproses
    keyInput = pygame.key.get_pressed()
    keyCode = getattr(pygame, f'K_{keyName}')
    return keyInput[keyCode]

def init():
    pygame.init()



#import pygame
#
# def init():
#     pygame.init()
#     win = pygame.display.set_mode((400,400))
#
# def getKey(keyName):
#     pygame.event.pump()  # Paksa Pygame untuk update event
#     # ans = False
#     # for eve in pygame.event.get(): pass
#     keyInput = pygame.key.get_pressed()
#     keyCode = getattr(pygame, f'K_{keyName}')
#     return keyInput[keyCode]
#     # myKey = getattr(pygame, 'K_{}'.format(keyName))
#     # if keyInput[myKey]:
#     #     ans = True
#     # pygame.display.update()
#     # return keyInput[myKey]
#
#
# # def main():
# #     if (getKey("LEFT")):
# #         print("Left key pressed")
# #     if (getKey("RIGHT")):
# #         print("right key pressed")
# #
# #
# # if __name__ == '__main__':
# #     init()
# #     while True:
# #         main()
#
