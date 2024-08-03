
import cv2
import numpy as np

# Load the dress with alpha channel
dress_path = r'C:\Users\rupin\Downloads\EY Hackathon\tshirt.png'
dress = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)

# Load Haar cascades for face and upper body
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces and upper bodies
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    upper_bodies = upper_body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Display the frame with detected faces and upper bodies (for troubleshooting)
    #for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    for (x, y, w, h) in upper_bodies:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Calculate shoulder points based on the upper body rectangle
        shoulder_width = w
        shoulder_height = int(h * 1.35)  # Adjust the fraction based on your preference for increased length

        # Resize the dress based on the calculated shoulder width
        dress_resized = cv2.resize(dress, (shoulder_width, shoulder_height))

        # Overlay the dress on the frame
        dress_x = x + w // 2 - shoulder_width // 2
        dress_y = y + int(h * 0.35)  # Adjust the fraction based on your preference

        alpha_channel = dress_resized[:, :, 3] / 255.0
        for c in range(3):
            frame[dress_y:dress_y + shoulder_height, dress_x:dress_x + shoulder_width, c] = \
                frame[dress_y:dress_y + shoulder_height, dress_x:dress_x + shoulder_width, c] * (1 - alpha_channel) + \
                dress_resized[:, :, c] * alpha_channel

    # Display the result
    cv2.imshow('Dress Overlay', frame)

    # Break the loop if 'ESC' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

