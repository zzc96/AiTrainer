import cv2
import numpy as np
import time
import PoseModule as pm
import pandas as pd
import correct as rb

cap = cv2.VideoCapture('./data/test2.mp4')
detector = pm.poseDetector()
count = 0
dir = 0
pTime = time.time()
cTime = 0
period_time = 0

# while True:
    # success, img = cap.read()
    # img = cv2.resize(img, (1280, 720))
img = cv2.imread('./data/down24.jpg')
img = cv2.resize(img, (1280, 720))
center = (1280 // 2, 720 // 2) #11
M = cv2.getRotationMatrix2D(center, 90, -1.0) #12
img = cv2.warpAffine(img, M, (1280, 720)) #13
img = detector.findPose(img, False)
lmList = detector.findPosition(img, False)
# print(lmList)
if len(lmList) != 0:
    # Right Arm
    model = pd.DataFrame()
    model, _, _, right_arm_angle = detector.findAngle(img, 12, 14, 16, model)
    right_arm_per = np.interp(right_arm_angle, (50, 170), (100, 0))
    right_arm_bar = np.interp(right_arm_angle, (50, 170), (100, 250))
    # # Left Arm
    model, _, _, lift_arm_angle = detector.findAngle(img, 11, 13, 15, model)
    lift_arm_per = np.interp(lift_arm_angle, (30, 160), (100, 0))
    lift_arm_bar = np.interp(lift_arm_angle, (30, 160), (350, 500))

    # print(angle, per)

    model, right_leg_angle, _, _ = detector.findAngle(img, 23, 25, 27, model)
    model, left_leg_angle, _, _ = detector.findAngle(img, 24, 26, 28, model)


    model, right_arm, right_body, right_arm_body_angle= detector.findAngle(img, 14, 12, 24, model)
    model, left_arm, left_body, left_arm_body_angle = detector.findAngle(img, 13, 11, 23, model)
    model, right_body, right_up_leg_angle, right_up_leg_body_angle = detector.findAngle(img, 12, 24, 26, model)
    rb.correctModel(right_arm, right_body, right_arm_body_angle, 166, 92, 74, 30).rightArmBodyUpAndDown()


    model, _, _, _= detector.findAngle(img, 23, 11, 13, model)
    model, _, _, _= detector.findAngle(img, 11, 23, 25, model)

    # model.to_csv('./model.csv')
    # Check for the dumbbell curls
    color = (255, 0, 255)
    if right_arm_per == 100 and lift_arm_per == 100:
        color = (0, 255, 0)
        if dir == 0:
            count += 0.5
            dir = 1

            cTime = time.time()
            period_time = cTime - pTime
            pTime = cTime

    if right_arm_per == 0 and lift_arm_per == 0:
        color = (0, 255, 0)
        if dir == 1:
            count += 0.5
            dir = 0

            cTime = time.time()
            period_time = cTime - pTime
            pTime = cTime

    print(count)

    # Draw Bar
    cv2.rectangle(img, (1100, 100), (1175, 250), color, 3)
    cv2.rectangle(img, (1100, int(right_arm_bar)), (1175, 250), color, cv2.FILLED)
    cv2.putText(img, f'{int(right_arm_per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)

    cv2.rectangle(img, (1100, 350), (1175, 500), color, 3)
    cv2.rectangle(img, (1100, int(lift_arm_bar)), (1175, 500), color, cv2.FILLED)
    cv2.putText(img, f'{int(lift_arm_per)} %', (1100, 325), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)

    # Draw Curl Count
    cv2.rectangle(img, (0, 620), (100, 720), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(float(count)), (25, 690), cv2.FONT_HERSHEY_PLAIN, 4,
                (255, 0, 0), 4)
    cv2.putText(img, str(float('%.2f' % period_time)) + 's', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

# cTime = time.time()
# fps = 1 / (cTime - pTime)
# pTime = cTime
# cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
#             (255, 0, 0), 5)

cv2.imshow("Image", img)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()