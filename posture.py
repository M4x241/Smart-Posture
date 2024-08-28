import math
import numpy as np
import cv2
import mediapipe as mp
import pyautogui, webbrowser
from Datos import Excel
from time import sleep


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
si = False
# importando llamar
contadorInclinacion=0
documento = Excel()

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

torso_connections = [
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_SHOULDER,mp_pose.PoseLandmark.RIGHT_SHOULDER),
    (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
    (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE),
    (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_EAR),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_EAR),
    (mp_pose.PoseLandmark.LEFT_EAR, mp_pose.PoseLandmark.RIGHT_EAR)
]
num = "+59167652401"
webbrowser.open("https://web.whatsapp.com/send/?phone=59167652401&text&type=phone_number&app_absent=0")
sleep(10)
with mp_pose.Pose(static_image_mode=False) as pose:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame, 1)
            #alerta = enviar()

        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        if results.pose_landmarks is not None:
            for connection in torso_connections:
                start_landmark = connection[0]
                end_landmark = connection[1]
                start_point = (int(results.pose_landmarks.landmark[start_landmark].x * width), int(results.pose_landmarks.landmark[start_landmark].y * height))
                end_point = (int(results.pose_landmarks.landmark[end_landmark].x * width), int(results.pose_landmarks.landmark[end_landmark].y * height))
                cv2.line(frame, start_point, end_point, (128, 0, 250), 2)

            l_hip = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * height))
            l_shoulder = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height))
            r_hip = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * height))
            r_shoulder = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height))
            l_ear = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].y * height))
            r_ear = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y * height))

            l_hip_shoulder_vector = (l_shoulder[0] - l_hip[0], l_shoulder[1] - l_hip[1])
            l_hip_ear_vector = (l_ear[0] - l_hip[0], l_ear[1] - l_hip[1])
            r_hip_shoulder_vector = (r_shoulder[0] - r_hip[0], r_shoulder[1] - r_hip[1])
            r_hip_ear_vector = (r_ear[0] - r_hip[0], r_ear[1] - r_hip[1])

            l_angle = math.acos(np.dot(l_hip_shoulder_vector, l_hip_ear_vector) / (np.linalg.norm(l_hip_shoulder_vector) * np.linalg.norm(l_hip_ear_vector)))
            r_angle = math.acos(np.dot(r_hip_shoulder_vector, r_hip_ear_vector) / (np.linalg.norm(r_hip_shoulder_vector) * np.linalg.norm(r_hip_ear_vector)))

            l_angle_degrees = l_angle * 180 / math.pi
            r_angle_degrees = r_angle * 180 / math.pi

            cv2.putText(frame, f"Angulo izquierdo: {l_angle_degrees:.2f} grados", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            cv2.putText(frame, f"Angulo derecho: {r_angle_degrees:.2f} grados", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            #si += 1
            if (l_angle_degrees > 9.5 or r_angle_degrees > 9.5) and si == False:
                contadorInclinacion +=1
                mensaje = str(contadorInclinacion) + ".- Buenos dias estimado!!!!!"
                pyautogui.typewrite(mensaje)
                pyautogui.press('enter')

                si = True
                if si ==True:
                    documento.ElementoApertura()
            if (l_angle_degrees < 9.5 and r_angle_degrees < 9.5) and si == True:

                si = False
                if si == False:
                    documento.ElementoCierre()
                    if (int(documento.col3[-1]) < 3):
                        if len(documento.col1) > 1 and len(documento.col2) > 1:
                            documento.col1.pop()
                            documento.col2.pop()
                            documento.col3.pop()
                        documento.guardarExcel()
                print("Se guardo")


        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()