import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


cap = cv2.VideoCapture(0)
w, h = 640, 480
cap.set(3, w)
cap.set(4, h)

cords = {}
last_status, hand_type = "", ""


with mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.9, min_detection_confidence=0.9) as hands:
    while True:
        # ------------------------- Camera Load --------------------- #
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # ----------------------------------------------------------- #
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:

            # +++++++++++++++++++++++++ Hand_Type +++++++++++++++++++++++++++ #
            if results.multi_handedness:
                hand_type = results.multi_handedness[0].classification[0].label
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # ======================== Hand_Draw ============================ #
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(imgRGB, hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(0, 0, 255)),
                                          mp_drawing.DrawingSpec(
                                              color=(0, 0, 0)))
            # =============================================================== #

                # ----------------------- Hand_Cords ------------------------ #
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cords[f"{id}"] = cx, cy
                # ----------------------------------------------------------- #
                # ########################### TEXT ########################## #
                if len(cords) == 21:
                    cv2.putText(imgRGB, f"Hand: {hand_type}", (cords['0'][0], cords['0'][1] + 35),
                                cv2.FONT_HERSHEY_DUPLEX, 0.85, (0, 0, 0), 1)

                    cv2.putText(imgRGB, f"Status: {last_status}",
                                (cords['0'][0], cords['0'][1] + 75),
                                cv2.FONT_HERSHEY_DUPLEX, 0.85, (0, 0, 0), 1)
                # ########################################################## #

                # ######################## Hand_Status ###################### #
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
                ###############################################################
        else:
            hand_type = "-"
            last_status = "-"

        cv2.imshow('Hand Tracking', imgRGB)
        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()
