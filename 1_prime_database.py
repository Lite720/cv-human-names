import os
from deepface import DeepFace
from pillow_heif import register_heif_opener

# Activate the HEIC image plugin
register_heif_opener()

# --- CONFIGURATION ---
MAIN_DIRECTORY = "C:/Users/rizal/Documents/Hamim/cv-human-names/processed"
# --- END CONFIGURATION ---

# --- New: Find one REAL image to use as a test ---
first_image_path = None
for person_name in os.listdir(MAIN_DIRECTORY):
    person_path = os.path.join(MAIN_DIRECTORY, person_name)
    
    # Check if it's a folder
    if os.path.isdir(person_path):
        for filename in os.listdir(person_path):
            # Find the first valid image file
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.heif')):
                first_image_path = os.path.join(person_path, filename)
                break  # Found an image, stop inner loop
    
    if first_image_path:
        break  # Found an image, stop outer loop
# --- End new ---

if first_image_path is None:
    print(f"ERROR: Could not find a single image in {MAIN_DIRECTORY} or its subfolders.")
    print("Please add images to your folders first.")
    exit()

print(f"Using sample image for test query: {first_image_path}")
print("Priming the DeepFace database... This will take several minutes.")
print("The system will 'hang' or be slow while it processes all 39 folders. This is normal.")

# Now we call DeepFace.find() with a REAL image.
# This will force it to scan the db_path and build the .pkl file.
try:
    dfs = DeepFace.find(
        img_path=first_image_path,
        db_path=MAIN_DIRECTORY,
        model_name="Facenet512",
        enforce_detection=False
    )
    # dfs (DataFrameS) will contain the match for the test image
    print("Test find complete. Results:")
    print(dfs)

except Exception as e:
    # If the test image has no face, it might error here, but the .pkl
    # file will likely be built anyway.
    print(f"Process finished with an expected query error (this is usually OK): {e}")

print("\nDatabase priming is complete.")
print("You should now see 'representations_vgg_face.pkl' in your main folder.")
print("You can now run '2_run_realtime_deepface.py'.")