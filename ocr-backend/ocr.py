import cv2
import pytesseract
import sys
import json
import re
import os

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path as needed

def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return image, gray
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

def extract_text(image):
    try:
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

def parse_text(text):
    try:
        result = {
            'Name': None,
            'Address': None,
            'Phone': None,
            'Mobile': None,
            'Company': None,
            'Job': None,
            'Email': None,
            'Web': None
        }

        # Regex patterns for different fields
        patterns = {
            'Phone': r'Phone|phone|Tel|tel|Telephone|telephone|T:',
            'Mobile': r'Mobile|mobile|Cell|cell|M:',
            'Email': r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',
            'Web': r'\b(?:http://|www\.)\S+\b'
        }

        lines = text.split('\n')
        for line in lines:
            if re.search(patterns['Phone'], line, re.I):
                result['Phone'] = line
            elif re.search(patterns['Mobile'], line, re.I):
                result['Mobile'] = line
            elif re.search(patterns['Email'], line, re.I):
                result['Email'] = line
            elif re.search(patterns['Web'], line, re.I):
                result['Web'] = line
            elif result['Name'] is None:
                result['Name'] = line.strip()  # Assuming the first line is the name
            else:
                result['Company'] = line.strip() if result['Company'] is None else result['Company'] + ' ' + line.strip()

        return result
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

def main(image_path):
    try:
        image, gray_image = preprocess_image(image_path)
        text = extract_text(gray_image)
        result = parse_text(text)
        
        # Save grayscale image
        gray_image_path = os.path.splitext(image_path)[0] + '_gray.png'
        cv2.imwrite(gray_image_path, gray_image)

        output = {
            'ocr_result': result,
            'original_image_path': image_path,
            'grayscale_image_path': gray_image_path
        }
        print(json.dumps(output))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1])
