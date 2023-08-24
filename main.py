from deepface import DeepFace
import cv2
import tkinter as tk
import sqlite3
import shutil
import os
from tkinter import messagebox
from pathlib import Path
from datetime import date
from PIL import Image,ImageTk

userName = ""
userPath = ""
createdPath = ""


def captureImage(): 
    camera = cv2.VideoCapture(0) 
    cv2.namedWindow("Camera Capture")
    capturedPath = ""
    messagebox.showinfo("Notice", "Please press space to checkin")
    while True:
        ret, frame = camera.read()
        if not ret:
            messagebox.showerror("Error", "Please press space to capture again")
            break
        cv2.imshow("Camera Capture", frame)

        key = cv2.waitKey(1)
        capturedPath = "captured_image.jpg"
        if key == 32:  # Space key
            cv2.imwrite("captured_image.jpg", frame)
            readImg ("captured_image.jpg")
        elif key == 27:
            camera.release()
            cv2.destroyAllWindows()  # Esc key
            return




def readImg(capture_path) :
    # TODO: image_path = [captured_path, img[i]] when traverse all folder & images
    captured_image = capture_path
    if (len(captured_image) == 0):
        return
    image_path = process_folder_images("sourceImages",captured_image)
    if (len(image_path) == 1):
        regLoop()
        # TODO: save the captured image to the folder with the username
        new_name = userName +".jpg"
        os.rename(captured_image, new_name)
        shutil.move(new_name, createdPath)

## FOLDER TRAVERSAL ##

def process_folder_images(folder_path, capturedImagePath):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_path = []
    image_path.append(capturedImagePath)
    for root_dir, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_file_path = os.path.join(root_dir, file_name)
                if compare_images(capturedImagePath, image_file_path):
                    image_path.append(image_file_path)
                    return image_path
    return image_path


def compare_images(image1_path, image2_path):
    global userPath
    userPath = image2_path
    try:
        result = DeepFace.verify(image1_path, image2_path,distance_metric="euclidean_l2")
        if result["verified"]:
            logLoop()
            return True
    except Exception as e:
         messagebox.showinfo("Error", "Cannot find face, please try again")
         readImg()
    return False


##
def register(username,errorLabel):
    global userName,createdPath
    if username:
        userName = username;
        # Connect to the database
        connection = sqlite3.connect("face_recognition.db")
        cursor = connection.cursor()

        # Insert the user into the database
        current_date = date.today().strftime("%d/%m/%Y")
        visit_sequence = 1

        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        result = cursor.fetchall()
        if len(result) > 0:
            errorLabel.config(text="Username already exists. Please choose a different username.")
        else:
            path = Path("./sourceImages") / username
            if (not path.exists()):
                path.mkdir()

        path_str = str(path)
        createdPath = path_str
        cursor.execute("INSERT INTO user (username, created_date, img_source, visit_sequence,checkin_date) VALUES (?, ?, ?, ?,?)", (username, current_date, path_str, visit_sequence,current_date))
        connection.commit()

        # Close the database connection
        connection.close()
        messagebox.showinfo("Registration Successful", "Welcome "+ username)
        root.destroy()
    
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

    # Error Label
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    # Register Button
    register_button = tk.Button(root, text="Register", command=lambda: register(username_entry.get(),error_label))
    register_button.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

def logLoop():
    root = tk.Tk()
    root.title("Checkin success")

    username =  userPath.split('\\')[1]


    connection = sqlite3.connect("face_recognition.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    current_date = date.today().strftime("%d/%m/%Y")
    result= cursor.fetchall()
    currentUsername,join_date,imgSrc,visit_times,checkin_date=result[0] 

    cursor.execute("UPDATE user SET visit_sequence = ?, checkin_date = ? WHERE username = ?", (visit_times + 1,checkin_date ,username))

    connection.commit()
    
    image = Image.open(userPath)  # Replace with your image file path
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo)
    image_label.image = photo
    image_label.pack(pady=10)

    # Add labels below the image
    label1 = tk.Label(root, text="Username: "+ username)
    label1.pack()

    label2 = tk.Label(root, text="Checkin date: "+ checkin_date)
    label2.pack()
    
    label3 = tk.Label(root, text="Visit sequences: "+ str(visit_times))
    label3.pack()
    
    label4 = tk.Label(root, text="Join date: "+ join_date)
    label4.pack()

    messagebox.showinfo("Checkin Successful", "Welcome "+username)
    connection.close()
    root.destroy()
    root.mainloop()


captureImage()
