import cv2
from handy import handy
video_capture = cv2.VideoCapture(0)
hist = handy.capture_histogram(source=0)


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # detect the hand
    # hand = handy.detect_hand(frame, hist)

   



    # Display the resulting frame
    cv2.imshow('FaceDetection', frame)

    # Keyboard input
    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC Pressed
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()