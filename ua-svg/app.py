from flask import Flask, request, render_template, redirect, jsonify
import requests
from PIL import Image
import io

app = Flask(__name__)

RECRAFT_API_KEY = 'UzW7cFWdN3fNPk6nk7Wd3kaBrpPCASpctU6PpYkxiIX4Fo1aayhEBhzsA1iScXDo'

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No image uploaded", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    # Open the image with PIL (Pillow)
    img = Image.open(file)

    # Convert the image to a 'P' mode (palette-based, reducing colors)
    img = img.convert("P", palette=Image.ADAPTIVE, colors=4)

    # Save the reduced color image to a bytes buffer
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Prepare the request to Recraft API
    url = "https://external.api.recraft.ai/v1/images/vectorize"
    headers = {
        "Authorization": f"Bearer {RECRAFT_API_KEY}"
    }

    files = {'file': img_byte_arr}
    data = {
        'response_format': 'url',  # Ensure the result is returned as a URL
    }

    # Send the POST request to Recraft API
    response = requests.post(url, headers=headers, files=files, data=data)

    # Log the response content for debugging
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        try:
            # Attempt to parse the response as JSON
            result = response.json()
            if 'image' in result and 'url' in result['image']:
                svg_url = result['image']['url']
                return jsonify({"url": svg_url})  # Return the URL to the frontend
            else:
                return "Failed to convert image, no URL found in response.", 500
        except ValueError:
            # If JSON parsing fails, this means the response is not JSON (possibly SVG or HTML)
            return "Error: Response is not valid JSON. Possibly an SVG file.", 500
    else:
        return f"Error: {response.text}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
