from flask import Flask, request, jsonify, send_file, render_template
from PIL import Image, ImageDraw
import os
from ultralytics import YOLO
import base64
from PIL import Image
import urllib.request 
import requests
from io import BytesIO
import base64
import logging
from logging.handlers import RotatingFileHandler
import cv2


app = Flask(__name__)


model = YOLO("best.pt")

def draw_bounding_box(image_path, bounding_box_coordinates, filename):
    # Read the image
    image = cv2.imread(image_path)
    # Extract bounding box coordinates
    x = int(bounding_box_coordinates[0])
    y = int(bounding_box_coordinates[1])
    w = int(bounding_box_coordinates[2])
    h= int(bounding_box_coordinates[3])
    print(x)
    print(y)
    print(w)
    print(h)
    # Draw bounding box on the image
    
    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    output_path = os.path.join('static/processed', filename)
    cv2.imwrite(output_path, image)
    return output_path
    


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/health',methods=['GET'])
def health():
    return "I am alive"

# End - Point for Logs
@app.route('/view-log')
def view_log():
    return send_file('app.log', mimetype='text/plain')

# Flask endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
        if request.method=='POST':
        
            file = request.files['filename'] # fet input
            filename = file.filename      
            print("@@ Input posted = ", filename)

            file_path = os.path.join('static/upload', filename)
            print("file_path", file_path)
            file.save(file_path)
            image = Image.open(file_path)
            print("Image read succesfully")
            width,height = image.size

            results = model(image)
            for result in results:
                boxes = result.boxes  # Boxes object for bbox outputs
            cls_value = int(boxes.cls.item())
            xywh_tensor = boxes.xywh.squeeze().tolist()
            conf = boxes.conf.item()
            path = draw_bounding_box(file_path, xywh_tensor, filename)
            print(conf)
            return render_template("index.html",stage_value=cls_value+1,confideneScore=conf,fileURL = path)
            # return jsonify({"stageValue":cls_value,"xywh_tensor":xywh_tensor,"conf":conf,"width":width,"height":height})
            # return jsonify({'message': 'Prediction completed'})
        else:
            return jsonify({'error': 'Missing image in request'})


import os

#Timestamp, to look for latest file
def sort_files_by_timestamp(directory_path):
    # Get a list of files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # Create a list of tuples containing filename, timestamp (modification time)
    file_timestamps = [(file, os.path.getmtime(os.path.join(directory_path, file))) for file in files]

    # Sort the list of tuples based on timestamps
    sorted_files = sorted(file_timestamps, key=lambda x: x[1])

    # Extract only the filenames from the sorted list
    sorted_file_names = [file[0] for file in sorted_files]

    return sorted_file_names


# Function to maintain a fixed no. of images for every stages
def fixSizedClasses():
    files = os.listdir("Directory path/File-Image location if taken from cloud")
    file_count = len(files)

    if(file_count == 12000):
        pass
    else:
        sort_files_by_timestamp("Path of our directory")
        

@app.route('/retrain', methods=['GET'])
def retrain():
    try:

        # To maintain fix size classes
        fixSizedClasses
        model = YOLO('modelPath/best.pt')
        model.train(data='data.yaml',epochs=30, optimizer='AdamW')

        # Export the model
        model.export(format='engine')
        return jsonify({'message': 'Model retraining completed'})
    except Exception as e:
        return jsonify({'error': f'An error occurred during retraining: {e}'})

if __name__ == '__main__':
    app.run(port=8000,debug=True)
