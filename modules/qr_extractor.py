import cv2
from pyzbar.pyzbar import decode

def extract_url_from_qr(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found.")
        return None

    decoded_objects = decode(img)

    if decoded_objects:
        url = decoded_objects[0].data.decode('utf-8')
        return url
    else:
        return None
