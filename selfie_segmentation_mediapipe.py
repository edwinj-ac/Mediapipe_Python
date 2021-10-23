import cv2 
import mediapipe as mp
import numpy as np

mp_selfie_segmentation = mp.solutions.selfie_segmentation

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


BG_COLOR = (250, 100, 150)

with mp_selfie_segmentation.SelfieSegmentation(
    model_selection=1) as selfie_segmentation:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = selfie_segmentation.process(frame_rgb)

        #Umbrealizacion a binario
        _, th = cv2.threshold(results.segmentation_mask, 0.75, 255, cv2.THRESH_BINARY)

        th = th.astype(np.uint8)
        th = cv2.medianBlur(th, 15)
        th_inv = cv2.bitwise_not(th)

        #cv2.imshow("results.segmentation_mask", results.segmentation_mask)

        #Background Color
        #bg_image = np.ones(frame.shape, dtype = np.uint8)
        #bg_image[:] = BG_COLOR
        #bg = cv2.bitwise_and(bg_image, bg_image, mask=th_inv)

        #Background Image
        bg_image = cv2.imread("Night-City-Street-Road-Wallpaper.jpg")
        bg_image = cv2.resize(bg_image,(frame.shape[1],frame.shape[0]),interpolation=cv2.INTER_CUBIC)
        bg_image = cv2.GaussianBlur(bg_image, (13,13), 0)
        bg = cv2.bitwise_and(bg_image, bg_image, mask=th_inv)

        #Foreground
        fg = cv2.bitwise_and(frame, frame, mask=th)

        #Background + Foreground
        output_image = cv2.add(bg, fg)
        
        #cv2.imshow("Th", th)
        #cv2.imshow("Th_inv", th_inv)
        cv2.imshow("Fg", fg)
        cv2.imshow("Bg", bg)
        cv2.imshow("Frame", frame)
        cv2.imshow("Output Image", output_image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()