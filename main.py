import cv2
import mediapipe as mp

#SETUP Mediapipe

mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# CAMERA LOOP

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_results = face_mesh.process(rgb_frame)
    hand_results = hands.process(rgb_frame)

    # Hand_Gesture Logic

    detected_state= "NEUTRAL"

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            thumb_tip=lm[mp_hands.HandLandmark.THUMB_TIP].y
            thumb_ip=lm[mp_hands.HandLandmark.THUMB_IP].y

            index_tip=lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_pip=lm[mp_hands.HandLandmark.INDEX_FINGER_PIP].y

            middle_tip=lm[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            middle_pip=lm[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y


            if thumb_tip < thumb_ip and index_tip > index_pip and middle_tip > middle_pip:
                detected_state = "THUMBS_UP"


            elif index_tip < index_pip and middle_tip > middle_pip and thumb_tip > thumb_ip:
                detected_state = "YOU"

    cv2.putText(
        frame,
        f"STATUS: {detected_state}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()