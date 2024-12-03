import os
from flask import Flask, request, jsonify, send_from_directory
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
import uuid
from dotenv import load_dotenv  # Load environment variables

load_dotenv()

app = Flask(__name__)

# Configuration
INPUT_FOLDER = 'inputs'
OUTPUT_FOLDER = 'outputs'
SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://127.0.0.1:5000')

# Ensure folders exist
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/output/<filename>')
def serve_output_image(filename):
    """Serve output images from the outputs directory"""
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    # Check if image is present
    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400
    
    image_file = request.files['image']
    
    # Check if filename is empty
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{secure_filename(image_file.filename)}"
        
        # Save input image
        input_path = os.path.join(INPUT_FOLDER, unique_filename)
        image_file.save(input_path)
        
        # Open input image
        input_image = Image.open(input_path)
        
        # Remove background and preserve transparency
        output_image = remove(input_image)
        
        # Determine file extension
        output_filename = f"no_bg_{unique_filename.split('.')[-0]}.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Save output image with transparency
        output_image.save(output_path, format='PNG')
        
        # Prepare static URL
        static_url = f"{SERVER_BASE_URL}/output/{output_filename}"
        
        return jsonify({
            "success": True,
            "output_image": static_url
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)