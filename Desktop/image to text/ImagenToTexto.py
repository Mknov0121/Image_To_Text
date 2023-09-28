import cv2
import pytesseract

print("Choose between:\n  1 Take a photo\n  2 Upload an image\n")
choice = int(input())

# ------------------------- Initialize constants and video capture settings -------------------------
square = 100
anchocam, altocam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, anchocam)
cap.set(4, altocam)

# ------------------------- Function to extract text from an image -------------------------
def extract_text_from_image(image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert the image from BGR to grayscale
    text = pytesseract.image_to_string(gray)  # Extract text from the grayscale image
    return text

if choice == 1:
    # ------------------------- Capture and process live video feed -------------------------
    while True:
        ret, frame = cap.read()  # Capture a frame from the video feed
        if ret == False:
            break  # If no frame is captured, exit the loop
        
        # Overlay text on the video feed
        cv2.putText(frame, ' PUT THE TEXT HERE ', (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (255,255,255), 2)
        
        # Draw a rectangle on the video feed
        cv2.rectangle(frame, (square, square), (anchocam - square, altocam - square), (0, 0, 0), 2)
        
        # Extract the region of interest inside the rectangle
        x1, y1 = square, square
        width, height = (anchocam - square) - x1, (altocam - square) - y1
        x2, y2 = x1 + width, y1 + height
        roi = frame[y1:y2, x1:x2]
        
        try:
            cv2.imwrite("imatext.jpg", roi)
        except Exception as e:
            print("Failed to write image:", e)
        
        cv2.imshow("Lector inteligente", frame)

        # Close the window when the 'ESCAPE' key is pressed
        if cv2.waitKey(1) == 27:
            break
            
    # Extract text from the region of interest and print
    text = extract_text_from_image(roi)
    print(text)
    
    cap.release()
    cv2.destroyAllWindows()

else:
    # ------------------------- Process an uploaded image -------------------------
    filename = input("Please enter your filename or path: ")
    image = cv2.imread(filename)

    if image is None:
        print("Failed to load the image")
        exit()

    extracted_text = extract_text_from_image(image)
    print(extracted_text)
