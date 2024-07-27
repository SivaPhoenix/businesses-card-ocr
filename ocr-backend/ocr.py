import cv2
import pytesseract
import sys
import json
import re
import os
import numpy as np  # Ensure numpy is imported

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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



def extract_text(image):
    try:
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    except Exception as e:
        print(json.dumps({"error": f"Extract text error: {str(e)}"}))
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

        patterns = {
            'Phone': r'Phone|phone|Ph|Tel|tel|Telephone|telephone|T:|^\+?\d[\d -]{8,12}\d$',
            'Mobile': r'Mobile|mobile|Cell|cell|M:|^\+?\d[\d -]{8,12}\d$',
            'Email': r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',
            'Web': r'\b(?:http://|https://|www\.)\S+\b'
        }

        lines = text.split('\n')
        for line in lines:
            if re.search(patterns['Phone'], line, re.I) and result['Phone'] is None:
                result['Phone'] = line.strip()
            elif re.search(patterns['Mobile'], line, re.I) and result['Mobile'] is None:
                result['Mobile'] = line.strip()
            elif re.search(patterns['Email'], line, re.I) and result['Email'] is None:
                result['Email'] = line.strip()
            elif re.search(patterns['Web'], line, re.I) and result['Web'] is None:
                result['Web'] = line.strip()
            elif result['Name'] is None:
                result['Name'] = line.strip()
            else:
                if result['Company'] is None:
                    result['Company'] = line.strip()
                else:
                    if result['Address'] is None:
                        result['Address'] = line.strip()
                    else:
                        result['Address'] += f' {line.strip()}'

        return result
    except Exception as e:
        print(json.dumps({"error": f"Parse text error: {str(e)}"}))
        sys.exit(1)

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
