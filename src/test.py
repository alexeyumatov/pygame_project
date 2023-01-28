import asyncio

import cv2
from config import *


cords = {}

last_status, hand_type = "", ""


async def hands_detection():
    global last_status
    with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9, min_detection_confidence=0.9) as hands:
        while True:
            success, frame = cap.read()
            frame = cv2.flip(frame, 1)

            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                if results.multi_handedness:
                    hand_type = results.multi_handedness[0].classification[0].label

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(imgRGB, hand_landmarks,
                                              mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(
                                                  color=(0, 0, 255)),
                                              mp_drawing.DrawingSpec(
                                                  color=(0, 0, 0)))

                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cords[f"{id}"] = cx, cy

                if len(cords) == 21:
                    if hand_type == "Right":
                        if int(cords['8'][1]) > int(cords['6'][1]) \
                                and int(cords['12'][1]) > int(cords['10'][1]) \
                                and int(cords['16'][1]) > int(cords['14'][1]) \
                                and int(cords['20'][1]) > int(cords['18'][1]) \
                                and int(cords['4'][0]) > int(cords['2'][0]):
                            last_status = "Close"
                        else:
                            last_status = "Open"

                    elif hand_type == "Left":
                        if int(cords['8'][1]) > int(cords['6'][1]) \
                                and int(cords['12'][1]) > int(cords['10'][1]) \
                                and int(cords['16'][1]) > int(cords['14'][1]) \
                                and int(cords['20'][1]) > int(cords['18'][1]) \
                                and int(cords['4'][0]) < int(cords['2'][0]):
                            last_status = "Close"
                        else:
                            last_status = "Open"

            else:
                hand_type = "-"
                last_status = "-"

            print(last_status, hand_type, sep=' ||| ')
            await asyncio.sleep(1)


async def game():
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()


async def main():
    task1 = asyncio.create_task(game())
    task2 = asyncio.create_task(hands_detection())
    await task1
    await task2


if __name__ == '__main__':
    asyncio.run(main())
