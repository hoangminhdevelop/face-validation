import cv2
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024  # 15MB max-limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DEFAULT_BLUR_THRESHOLD = 30

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_blurry(image, threshold=DEFAULT_BLUR_THRESHOLD):
    """Check if image is blurry using the Laplacian variance method"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < threshold, laplacian_var

def count_faces(image):
    """Count the number of faces in the image using Haar cascade"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces), faces

def is_cartoon_or_fake(image):
    """
    Basic detection for cartoon/fake faces
    This is a placeholder for more sophisticated detection
    In a production environment, you would use a trained ML model for this
    """
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Check for oversaturated colors (often present in cartoons)
    saturation = hsv[:,:,1]
    mean_saturation = np.mean(saturation)
    
    # Check for lack of texture (often in cartoons or AI-generated images)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    edge_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    texture_variance = np.var(edge_magnitude)
    
    # These thresholds would need to be fine-tuned based on your specific requirements
    is_likely_cartoon = mean_saturation > 120 and texture_variance < 1000
    
    return is_likely_cartoon

@app.route('/validate-face', methods=['POST'])
def validate_face():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    
    file = request.files['image']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Read image
        img_stream = file.read()
        nparr = np.frombuffer(img_stream, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Could not process image'}), 400
        
        # 1. Check if image has exactly one face
        face_count, faces = count_faces(img)
        if face_count != 1:
            return jsonify({
                'valid': False,
                'reason': f'Expected 1 face, found {face_count}'
            }), 400
        
        # 2. Check if image is blurry
        is_blur, blur_value = is_blurry(img)
        if is_blur:
            return jsonify({
                'valid': False,
                'reason': f'Image is too blurry (score: {blur_value:.2f})'
            }), 400
        
        # 3. Check if face is cartoon or fake
        if is_cartoon_or_fake(img):
            return jsonify({
                'valid': False,
                'reason': 'Image appears to be a cartoon or fake face'
            }), 400
        
        # If all checks pass, the image is valid
        return jsonify({
            'valid': True,
            'message': 'Valid human face detected'
        }), 200
        
    return jsonify({'error': 'File type not allowed. Use jpg, jpeg or png'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)