import cv2
from deepface import DeepFace
import os

# --- CONFIGURATION ---
MAIN_DIRECTORY = "C:/Users/rizal/Documents/Hamim/cv-human-names/processed"
# --- END CONFIGURATION ---

print("Loading DeepFace models...")

# Start the webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting webcam... Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    try:
        # 1. DETECT faces in the frame.
        faces = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="opencv",
            enforce_detection=False 
        )

        # Loop through each face found in the frame
        for face_info in faces:
            if face_info['confidence'] == 0:
                continue

            box = face_info['facial_area']
            x, y, w, h = box['x'], box['y'], box['w'], box['h']

            # Draw the box on the original frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            name = "Unknown" # Default name

            # 2. RECOGNIZE the face
            # We add a separate try/except here for the find operation
            try:
                dfs = DeepFace.find(
                    img_path=frame[y:y+h, x:x+w],
                    db_path=MAIN_DIRECTORY,
                    model_name="Facenet512",
                    enforce_detection=False, 
                    silent=True 
                )

                # --- NEW SAFER LOGIC ---
                # 1. Check if 'dfs' is a list and is not empty
                if dfs and isinstance(dfs, list) and len(dfs) > 0:
                    # 2. Now get the first DataFrame
                    df = dfs[0]
                    # 3. Check if the DataFrame is not empty
                    if not df.empty:
                        # 4. We have a match! Get the name.
                        full_path = df.iloc[0]['identity']
                        dir_path = os.path.dirname(full_path)
                        name = os.path.basename(dir_path)
                # --- END NEW LOGIC ---

            except Exception as e:
                # If DeepFace.find() fails, name remains "Unknown"
                # print(f"Find error: {e}") # Uncomment for debugging
                pass

            # Draw the name
            cv2.rectangle(frame, (x, y - 35), (x + w, y), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x + 6, y - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    except Exception as e:
        # This catches errors from 'extract_faces'
        # print(f"Extract error: {e}") # Uncomment for debugging
        pass

    # Display the resulting image
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()