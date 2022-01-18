# 1. Import and Install Dependencies
import cv2
import numpy as np
import mediapipe as mp  # extract KPs #https://google.github.io/mediapipe/getting_started/python.html

##########################################################################################
# 2. Keypoints using MP Holistic

mp_drawing = mp.solutions.drawing_utils # Drawing utilities
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic # Holistic model

###########################################################################################
# DETECTION


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction - detects KPs home image
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR COVERSION RGB 2 BGR
    return image, results

############################################################################################
# SHOW keypoints - same as before, but now with diferent colors for each element of the body


def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
        mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
        mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(80, 22, 255), thickness=1, circle_radius=3),
        mp_drawing.DrawingSpec(color=(80, 44, 255), thickness=1, circle_radius=1))
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(255, 22, 76), thickness=1, circle_radius=3),
        mp_drawing.DrawingSpec(color=(255, 44, 250), thickness=1, circle_radius=1))
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(245, 255, 66), thickness=1, circle_radius=3),
        mp_drawing.DrawingSpec(color=(245, 255, 230), thickness=1, circle_radius=1))

######################################
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    # Set mediapipe model
    swapLeft = 0
    swapRight = 0
    handsUp = 0
    rightHandUp = 0

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic: # mediapipe makes a detection, after #that tracks the keypoints; makes initial

        while cap.isOpened():
            # Read feed
            ret, frame = cap.read()
            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            # print(results.pose_landmarks.landmark)
            # print(results.face_landmarks);
            # print(results.left_hand_landmarks)
            # print(results.right_hand_landmarks)
            # print(results.pose_landmarks.landmark[0].x)
            # print(len(results.pose_landmarks.landmark))
            # join all results in a list - pose ONLY this case
            if (results.pose_landmarks!=None):
                pose = []
                for res in results.pose_landmarks.landmark:
                    temp = np.array([res.x, res.y, res.z, res.visibility])
                    pose.append(temp)
                #print(pose)
                #print("Num elem in pose:", len(pose))

                # print coordinates x and y
                #for i in range(len(pose)):
                    #print("join", i, "Xcoord", round(pose[i][0], 1), "Ycoord", round(pose[i][1], 1))

                # para visualizar passo a passo - press KEY - COMENTAR
                # print("---")

                if pose[16][0] > pose[12][0] and pose[11][0]:
                    swapRight = 1

                if pose[15][0] < pose[11][0] and pose[12][0]:
                    swapLeft = 1

                if pose[15][1] and pose[16][1] < pose[11][1] and pose[12][1]:
                    handsUp = 1

                if (pose[16][1] < pose[11][1] and pose[12][1]) and (pose[15][1] > pose[11][1] and pose[12][1]):
                    rightHandUp = 1
                    handsUp=0

                print("swapRight is:")
                print(swapRight)
                print("swapLeft is: ")
                print(swapLeft)
                print("handsUp is: ")
                print(handsUp)
                print("rightHandUp is: ")
                print(rightHandUp)
                print("------")
                #cv2.waitKey()
                # FIM - para visualizar passo a passo - COMENTAR
                # Break camera

            cv2.imshow("detection",image)
            if cv2.waitKey(10) & 0xFF == 27:
                break
            swapLeft = 0
            swapRight = 0
            handsUp = 0
            rightHandUp = 0
    cap.release()
    cv2.destroyAllWindows()