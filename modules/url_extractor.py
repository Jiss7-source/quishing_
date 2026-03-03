import cv2
import os
from pyzbar.pyzbar import decode

def extract_url_from_qr(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error reading {image_path}")
        return None

    decoded_objects = decode(img)

    if not decoded_objects:
        print(f"No QR found in {image_path}")
        return None

    return decoded_objects[0].data.decode("utf-8")


if __name__ == "__main__":
    upload_folder = "uploads"

    for filename in os.listdir(upload_folder):
        image_path = os.path.join(upload_folder, filename)

        print("\nProcessing:", filename)
        url = extract_url_from_qr(image_path)

        if url:
            print("Extracted URL:", url)
        else:
            print("No valid QR data found.")