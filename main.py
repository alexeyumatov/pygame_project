import asyncio
import pygame
from src.game import game_func, hands_detection
from src.functions import load_image


async def main():
    task1 = asyncio.create_task(game_func())
    task2 = asyncio.create_task(hands_detection())
    await task1
    await task2

if __name__ == '__main__':
    pygame.display.set_caption('Dark Light', 'Dark Light')
    icon = load_image('icon/dark_light_icon.png')
    pygame.display.set_icon(icon)
    asyncio.run(main())
