
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
 print("Cannot open camera")
 
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    threshold_value = 250

    #ret, frame = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
