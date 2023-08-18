from deepface import DeepFace
import cv2
import tkinter as tk
import sqlite3
import shutil
import os
from tkinter import messagebox
from pathlib import Path
from datetime import date

userName = ""
createdPath = ""

def readImg() :
    # TODO: image_path = [captured_path, img[i]] when traverse all folder & images
    image_path =[ "taylor1.jpeg", "beckham1.jpeg"]

    result = DeepFace.verify(image_path[0], image_path[1])
    verified = result["verified"]
    facialAreas = result["facial_areas"]
    img1Bound = facialAreas["img1"]
    img2Bound = facialAreas["img2"]
    # draw rectangle on detected face

    img1 = cv2.imread(image_path[0])
    img2 = cv2.imread(image_path[1])

    # convert  x,y,w,h to points
    img1Bound['w'] = img1Bound['w'] + img1Bound['x']
    img1Bound['h'] = img1Bound['h'] + img1Bound['y']

    img2Bound['w'] = img2Bound['w'] + img2Bound['x']
    img2Bound['h'] = img2Bound['h'] + img2Bound['y']

    cv2.rectangle(img1, (img1Bound['x'], img1Bound['y']), (img1Bound['w'],img1Bound['h']), (0, 255, 0), 2)
    cv2.rectangle(img2, (img2Bound['x'], img2Bound['y']), (img2Bound['w'], img2Bound['h']), (0, 255, 0), 2)

    # resize img to 720px width and 480px height
    img1 = cv2.resize(img1, (400, 400))
    img2 = cv2.resize(img2, (400, 400))

    # concat 2 images
    img = cv2.hconcat([img1, img2])


    if (verified == False):
        regLoop();
        print(userName)
        # TODO: save the captured image to the folder with the username 
    else:
        cv2.imshow("Taylor Swift", img)
    cv2.waitKey(0)

## FOLDER TRAVERSAL ##

# def process_folder_images(folder_path):
#     for root_dir, _, files in os.walk(folder_path):
#         for file_name in files:
#             if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#                 image_file_path = os.path.join(root_dir, file_name)
#                 if compare_images(captured_image_path, image_file_path):
#                     image_path.append(image_file_path)

# def compare_images(image1_path, image2_path):
#     result = DeepFace.verify(image1_path, image2_path)
#     if result["verified"]:
#         return True
#     return False


##
def register(username):
    global userName,createdPath
    if username:
        userName = username;
        # Connect to the database
        connection = sqlite3.connect("face_recognition.db")
        cursor = connection.cursor()

        # Insert the user into the database
        current_date = date.today().strftime("%d/%m/%Y")
        visit_sequence = 1
        path = Path("./imgSource") / username
        path.mkdir()
        
        # Convert the path to a string before inserting it into the database
        path_str = str(path)
        createdPath = path_str
        cursor.execute("INSERT INTO user (username, created_date, img_source, visit_sequence) VALUES (?, ?, ?, ?)", (username, current_date, path_str, visit_sequence))
        connection.commit()

        # Close the database connection
        connection.close()
        messagebox.showinfo("Registration Successful", "Welcome "+ username)
        root.destroy();
    
def regLoop():
    global root

    root = tk.Tk()
    root.title("User Registration")

    # Set the size of the window
    window_width = 300
    window_height = 200
    root.geometry(f"{window_width}x{window_height}")
    # Calculate the screen center
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"+{x_position}+{y_position}")

    # Create and place widgets using the pack and place geometry managers
    frame = tk.Frame(root)
    frame.pack(expand=True)

    # Username Label and Entry
    username_label = tk.Label(frame, text="Username:")
    username_label.pack(side="left", padx=(10, 5), pady=10)

    username_entry = tk.Entry(frame)
    username_entry.pack(side="left", padx=(0, 10), pady=10)

    # Register Button
    register_button = tk.Button(root, text="Register", command=lambda: register(username_entry.get()))
    register_button.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

def logLoop():
    global root

    root = tk.Tk()
    root.title("User Registration")

    messagebox.showinfo("Registration Successful", "Welcome "+ username)
    root.destroy();
    # Start the GUI event loop
    root.mainloop()

readImg();



