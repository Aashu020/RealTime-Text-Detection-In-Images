import tkinter as tk
from tkinter import filedialog
import pytesseract
import cv2
from PIL import Image, ImageTk
import ctypes

# Setting up Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def clear_text1():
    mytext2.delete("1.0", "end")
    
def clear_text2():
    mytext.delete("1.0", "end")
    
def uploadvideo():
    filepath = filedialog.askopenfilename()
    img1 = cv2.imread(filepath)
    img2char1 = pytesseract.image_to_string(img1)
    imgbox1 = pytesseract.image_to_boxes(img1)
    imgH1, imgW1, _ = img1.shape
    for boxes1 in imgbox1.splitlines():
        boxes1 = boxes1.split(' ')
        x1, y1, w1, h1 = int(boxes1[1]), int(boxes1[2]), int(boxes1[3]), int(boxes1[4])
        cv2.rectangle(img1, (x1, imgH1 - y1), (w1, imgH1 - h1), (0, 150, 200), 3)
    print(img2char1)
    mytext.insert(tk.END, img2char1)

def opencam():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Couldn't open video file.")
        return
    
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        
        if not ret:
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        extracted_text = pytesseract.image_to_string(gray_frame)
        
        print(extracted_text)
        mytext2.insert(tk.END, extracted_text)
        
        cv2.imshow('Text Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

root = tk.Tk()
root.title('TEXT DETECTOR')
root.geometry("1050x553")
root.resizable(False, False)

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Calculate desired width and height for the video
desired_width = int(screen_width * 0.8)
desired_height = int(screen_height * 0.8)

root.geometry(f"{desired_width}x{desired_height}")
root.resizable(False, False)

# Load background video
video_path = 'C:/Users/acer/Downloads/asif project1/asif project/textdectector/textdectector/vid01.mp4'
cap = cv2.VideoCapture(video_path)

# Define a function to update the background video
def update_background():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame.resize((desired_width, desired_height)))
        bg_label.configure(image=frame)
        bg_label.image = frame
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Set frame position to beginning for looping
    root.after(10, update_background)

# Label for background video
bg_label = tk.Label(root)
bg_label.place(x=0, y=0)
update_background()

# Transparent Title
title_label = tk.Label(root, text="Text Detector", font=("Helvetica", 32, "bold"), fg="black")
title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
title_label.config(highlightthickness=0, bd=0)

""" # Label for upload video or photo
label1 = tk.Label(root, text="Upload Video or Photo", padx=40, font="Arial 12", bg="ivory")
label1.place(x=105, y=80)
label1.config(highlightthickness=0, bd=0) """

# Button to upload video
upload_img = Image.open("C:/Users/acer/Downloads/asif project1/asif project/textdectector/textdectector/upload_icon.png")
upload_img = upload_img.resize((100, 100))
upload_photo = ImageTk.PhotoImage(upload_img)
btn1 =tk.Button(root, image=upload_photo, bd=0, command=uploadvideo)
btn1.place(x=735, y=105)

""" # Label for open camera
label2 = tk.Label(root, text="Open Camera", padx=40, font="Arial 12", bg="ivory")
label2.place(x=700, y=75)
label2.config(highlightthickness=0, bd=0 """

# Button to open camera (cam icon)
cam_img = Image.open("C:/Users/acer/Downloads/asif project1/asif project/textdectector/textdectector/cam_icon.png")
cam_img = cam_img.resize((100, 100))
cam_photo = ImageTk.PhotoImage(cam_img)
btn = tk.Button(root, image=cam_photo, bd=0, command=opencam)
btn.place(x=160, y=105)

# Text box for display
mytext = tk.Text(root, width=55, height=20, font="Arial 10 bold")
mytext.place(x=596, y=190)

# Button to clear text box 1
clear_icon = Image.open("C:/Users/acer/Downloads/asif project1/asif project/textdectector/textdectector/clear_icon.png")
clear_icon = clear_icon.resize((30, 30))
clear_photo = ImageTk.PhotoImage(clear_icon)
btn2 = tk.Button(root, image=clear_photo, bd=0, command=clear_text1)
btn2.place(x=40, y=190)

# Text box 2 for display
mytext2 = tk.Text(root, width=55, height=20, font="Arial 10 bold")
mytext2.place(x=70, y=190)

# Button to clear text box 2
btn3 = tk.Button(root, image=clear_photo, bd=0,  command=clear_text2)
btn3.place(x=982, y=190)

root.mainloop()
