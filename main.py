import threading
import time
import cv2
from ultralytics import YOLO
import cvzone
import pandas as pd
from collections import Counter
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.core.window import Window
import os

# Load YOLO model and COCO classes
model = YOLO("yolov8s.pt")
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

Window.size = (700, 350)

# Create a new folder to store output images
output_folder = "output_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

class TestCameraApp(App):
    def build(self):
        self.box = BoxLayout(orientation='vertical')

        # Initialize Camera
        self.mycam = Camera(play=False, resolution=(600,480))
        self.box.add_widget(self.mycam)

        # Toggle Button for Play/Stop
        tb = ToggleButton(text='Play', size_hint_y=None, height='48dp')
        tb.bind(on_press=self.play)
        self.box.add_widget(tb)

        # Button for Capturing Image
        capture_img_btn = Button(text='Capture Image', size_hint_y=None, height='48dp')
        capture_img_btn.bind(on_press=self.capture_image)
        self.box.add_widget(capture_img_btn)

        # Label for Object Detection Output
        self.output_label = Label(text="Object Count:", size_hint_y=None, height='48dp')
        self.box.add_widget(self.output_label)

        return self.box

    def play(self, instance):
        if instance.state == 'down':
            self.mycam.play = True
            instance.text = 'Stop'
        else:
            self.mycam.play = False
            instance.text = 'Play'

    def capture_image(self, instance):
        if self.mycam.play:
            # Capture the image and save it
            image_path = f'captured_image_{int(time.time())}.png'
            self.mycam.export_to_png(image_path)
            print("Image captured and saved.")

            # Start a new thread to process the image and update the label
            threading.Thread(target=self.process_image, args=(image_path,)).start()

    def process_image(self, image_path):
        # Load the captured image
        img = cv2.imread(image_path)

        # Perform object detection
        object_classes, detected_img = object_detect(img)

        # Update and display the object count
        count_text = update_count(object_classes)
        self.output_label.text = count_text

        # Save the output image with detected objects in the new folder
        output_image_path = os.path.join(output_folder, f'detected_image_{int(time.time())}.png')
        cv2.imwrite(output_image_path, detected_img)
        print(f"Detected image saved at {output_image_path}")

# Define the object detection function
def object_detect(img):
    results = model.predict(img)
    a = results[0].boxes.data
    info = pd.DataFrame(a).astype("float")
    object_classes = []
    for index, row in info.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        obj_class = class_list[d]
        object_classes.append(obj_class)
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cvzone.putTextRect(img, f'{obj_class}', (x2, y2), 1, 1)
    return object_classes, img

# Define a function to update the object count

def update_count(object_classes):
    counter = Counter(object_classes)
    count_text = "Object Count:"
    for obj, count in counter.items():
        count_text += f"{obj}: {count}\n"
    print(count_text)
    return count_text


TestCameraApp().run()