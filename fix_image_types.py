import os
from PIL import Image
from pillow_heif import register_heif_opener # <--- ADDED

register_heif_opener() # <--- ADDED (this activates the plugin)

# --- CONFIGURATION ---
# !!! SET THIS TO YOUR MAIN FOLDER'S PATH !!!
MAIN_DIRECTORY = "C:/Users/rizal/Documents/Hamim/cv-human-names/processed"
# --- END CONFIGURATION ---

# Added .heic and .heif to the list
VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.heic', '.heif') # <--- MODIFIED

print(f"Starting process in: {MAIN_DIRECTORY}\n")

# Loop through each item in the main directory
for person_name in os.listdir(MAIN_DIRECTORY):
    person_path = os.path.join(MAIN_DIRECTORY, person_name)

    # Only process if it's a directory
    if os.path.isdir(person_path):
        print(f"--- Processing folder: {person_name} ---")
        
        # Clean the name (e.g., "Rizal Hamim" -> "rizal_hamim")
        person_name_clean = person_name.replace(' ', '_').lower()
        image_counter = 1

        # Loop through all files in the person's folder
        for filename in os.listdir(person_path):
            old_file_path = os.path.join(person_path, filename)
            
            # This check now includes .heic and .heif
            if not os.path.isfile(old_file_path) or not filename.lower().endswith(VALID_EXTENSIONS):
                continue

            # Define the new standardized name
            new_filename = f"{person_name_clean}_{image_counter}.jpg"
            new_file_path = os.path.join(person_path, new_filename)

            # This will now work for .heic files thanks to the plugin
            img = Image.open(old_file_path)
            
            # Convert to 'RGB' (to remove transparency from PNGs, etc.)
            rgb_img = img.convert('RGB')
            
            # Save the new JPEG file
            rgb_img.save(new_file_path, 'JPEG', quality=95)
            
            # Close the file handlers
            img.close()
            rgb_img.close()

            # Delete the original file IF it's not the same file
            if old_file_path != new_file_path:
                os.remove(old_file_path)

            print(f"  Processed: {filename}  ->  {new_filename}")
            image_counter += 1

        print(f"--- Finished folder: {person_name} ---\n")

print("All folders processed.")