import cv2
import numpy as np
from pyzbar.pyzbar import decode

def resize_image(image, max_width=800, max_height=800):
    height, width = image.shape[:2]
    scaling_factor = min(max_width / float(width), max_height / float(height))
    if scaling_factor < 1:
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return image

def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 2)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = f"Data: {barcodeData} | Type: {barcodeType}"

        # Fixed font scale and thickness to ensure the label is always visible
        font_scale = 0.7  # Set a fixed font size
        thickness = 2

        # Calculate text size and position to ensure it fits within the image
        text_size = cv2.getTextSize(string, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        
        # Ensure text is inside the image boundaries
        text_x = max(x, 0)
        text_y = max(y - 10, text_size[1] + 10)

        # If the text is too wide for the image, move it to a new line or adjust the position
        if text_x + text_size[0] > image.shape[1]:
            text_x = 10  # Align text to the left if it's too wide

        cv2.putText(image, string, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness)
        print("Barcode: " + barcodeData + " | Type: " + barcodeType)

    return image


def process_image():
    file_path = input("Enter the path of the image: ")
    image = cv2.imread(file_path)
    if image is None:
        print("Failed to load image.")
        return
    
    # Resize image to a manageable size
    image = resize_image(image)

    result_image = decoder(image)
    cv2.imshow('Result', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_video():
    file_path = input("Enter the path of the video file: ")
    cap = cv2.VideoCapture(file_path)
    
    if not cap.isOpened():
        print("Failed to load video.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = resize_image(frame)  # Resize each frame
        frame = decoder(frame)
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def process_live_stream():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = resize_image(frame)  # Resize each frame
        frame = decoder(frame)
        cv2.imshow('Live Stream', frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Choose an option:")
    print("1. Process an Image")
    print("2. Process a Video")
    print("3. Live Stream (Webcam)")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        process_image()
    elif choice == '2':
        process_video()
    elif choice == '3':
        process_live_stream()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
