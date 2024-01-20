import os
import cv2
from flask import Flask, Response, render_template, request, jsonify
import base64

app = Flask(__name__)
app.config.from_object(__name__)

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

def dehaze_image(input_image_path):
    # Your dehazing logic goes here
    # This is a placeholder example using a simple median blur
    img = cv2.imread(input_image_path)
    dehazed_image = cv2.medianBlur(img, 5)

    # Encode the dehazed image to base64
    _, buffer = cv2.imencode('.jpg', dehazed_image)
    dehazed_base64 = base64.b64encode(buffer).decode('utf-8')

    return dehazed_base64

@app.route('/', methods=['GET'])
def index():
    # Assuming you have an 'index.html' file in the root directory
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Handle file upload logic here
        uploaded_file = request.files['image']

        # Print information about the uploaded file
        print(f"Received file: {uploaded_file.filename}")

        # Example: Save the uploaded file to the 'uploads' folder
        file_path = os.path.join(root_dir(), 'uploads', uploaded_file.filename)
        uploaded_file.save(file_path)
        print(f"File saved to: {file_path}")

        # Add your image deblurring logic here
        dehazed_base64 = dehaze_image(file_path)

        # Return a JSON response with the base64-encoded dehazed image
        return jsonify({'deblurred_image': dehazed_base64})

    except Exception as e:
        # Print any exception that might occur during the process
        print(f"Error: {e}")
        return "Error during file upload"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)

if __name__ == '__main__':
    app.run(port=80, debug=True)
