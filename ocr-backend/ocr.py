import cv2
import pytesseract
import sys
import json
import re
import os
import numpy as np  # Ensure numpy is imported

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# preprocessing the image
def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        gray = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        gray = cv2.filter2D(gray, -1, kernel)
        return image, gray
    except Exception as e:
        print(json.dumps({"error": f"Preprocess error: {str(e)}"}))
        sys.exit(1)


# Extract the test from the image
def extract_text(image):
    try:
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    except Exception as e:
        print(json.dumps({"error": f"Extract text error: {str(e)}"}))
        sys.exit(1)

# Parsing the text
def parse_text(text):
    result = {
        'Name': None,
        'Address': None,
        'Phone': None,
        # 'Mobile': None,
        'Company': None,
        'Job': None,
        'Email': None,
        'Web': None
    }

    patterns = {
        'Phone': r'(?:(?:\+?\d{1,4}[-.\s])?(?:\(?\d{1,5}\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})',
        # 'Mobile': r'(?:(?:\+?\d{1,4}[-.\s])?(?:\(?\d{1,5}\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})',
        'Email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'Web': r'(?:http://|https://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',
    }

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if re.search(patterns['Phone'], line):
            result['Phone'] = line
        # elif re.search(patterns['Mobile'], line):
        #     result['Mobile'] = line
        elif re.search(patterns['Email'], line):
            result['Email'] = line
        elif re.search(patterns['Web'], line):
            result['Web'] = line
        elif result['Name'] is None:
            result['Name'] = line
        elif result['Address'] is None:
            if result['Company'] is None:
                result['Address'] = line
            else:
                result['Address'] += ' ' + line
        elif result['Company'] is None:
            result['Company'] = line

    return result

#return result, original image and grayscale image

def main(image_path):
    try:
        image, gray_image = preprocess_image(image_path)
        text = extract_text(gray_image)
        result = parse_text(text)
        
        gray_image_path = os.path.splitext(image_path)[0] + '_gray.png'
        cv2.imwrite(gray_image_path, gray_image)

        output = {
            'ocr_result': result,
            'original_image_path': image_path,
            'grayscale_image_path': gray_image_path
        }
        print(json.dumps(output))
    except Exception as e:
        print(json.dumps({"error": f"Main error: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1])
