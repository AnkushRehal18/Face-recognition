import face_recognition
import cv2
import numpy as np
import os
import csv
from datetime import datetime
import tkinter as tk #helps use to create gui  of our application  
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from email.message import EmailMessage
import smtplib
import imghdr

# Initialize the video capture from the default camera (0)
video_capture = cv2.VideoCapture(1)

# Load known face encodings and names
jobs_image = face_recognition.load_image_file("photos/steve_jobs.png")
jobs_encoding = face_recognition.face_encodings(jobs_image)[0] #0 is used here to access the first file

ratan_tata_image = face_recognition.load_image_file("photos/ratantata.png")
ratan_tata_encoding = face_recognition.face_encodings(ratan_tata_image)[0]

sadmona_image = face_recognition.load_image_file("photos/monalisa.png")
sadmona_encoding = face_recognition.face_encodings(sadmona_image)[0]

tesla_image = face_recognition.load_image_file("photos/elonmusk.png")
tesla_encoding = face_recognition.face_encodings(tesla_image)[0]


known_face_encodings = [jobs_encoding, ratan_tata_encoding, sadmona_encoding, tesla_encoding]
known_face_names = ["jobs", "ratan_tata", "sadmona", "tesla" , "ankush","Gurjot Singh","Neha"]


students = known_face_names.copy()

# Initialize variables for face detection and recognition
face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now() 
current_date = now.strftime("%Y-%m-%d") #create a varibale to save the file aacroidng to current date 
current_time_csvv = datetime.now() #created a variable to store the current time 
# Open a CSV file for writing attendance data
with open(current_date + '.csv', 'w', newline='') as csvfile:
    lnwriter = csv.writer(csvfile)

    while True: #created an infinite wile loop 
        _, frame = video_capture.read() #reading video from the frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #resized the frame 
        rgb_small_frame = small_frame[:, :, ::-1]

        if s:
            face_locations = face_recognition.face_locations(rgb_small_frame) #if there is face in camra or not
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=1)
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"  # Default to "Unknown" if the face is not recognized
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances) #argmin method is used to return the smallest value

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

                if name in students:
                    students.remove(name)
                    current_time = current_time_csvv
                    lnwriter.writerow([name, current_time])

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle and label the recognized face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.imshow("Attendance System", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

# Release video capture and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()

# GUI Section of the email app

chekc = False  #used to check if user have attacehd any file 

#created an attachment funtion to attach an file 
def attachment():
    global name_of_file, file_type, file, chekc #global vairable 

    chekc = True #if true then user have attached an file

    file = filedialog.askopenfilename(initialdir='c:/', title="Select file") #open a dialog box from dir
    file_type = file.split('.')  # Split the file name into two parts: name and file type
    file_type = file_type[1]  # Store the type of file in this variable
    name_of_file = os.path.basename(file) #will return the name of the file by passing the address
    Email_text_area.insert(tk.END, f"\n{name_of_file}\n")  # Insert the file name into the text area of the email

def sendemail(toaddress, body): #used in submit button to send mail 
    # Open the email credentials file and read it

    with open('credential.txt', 'r') as f: #opened the  credential file in read mode 
        for i in f:
            email_credentials = i.split(',') #used a for loop to read file and split it into two parts from, 

    message = EmailMessage()  #created an object of EmailMessage class 
    message['to'] = toaddress  #where to send 
    message['from'] = email_credentials[0] #used to get the email credentials from the email credential file
    message.set_content(body) #the body 

    if chekc:
        if file_type == 'png' or file_type == 'jpg' or file_type == 'jpeg': #checking file type 
            f = open(file, 'rb')    #opened in binary read format
            file_data = f.read()    #stored file data 
            subtype = imghdr.what(file)    #calculate subtype of file using imghdr 
            message.add_attachment(file_data, maintype='image', subtype=subtype, filename=name_of_file)
        else:
            f = open(file, 'rb')  #this is for an document file
            file_data = f.read()
            message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=name_of_file)
    

    
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587) #create object of smtp class passed gmail and its port no
    
    smtpobj.starttls()  #used to secure connection between client and server 
    
    smtpobj.login(email_credentials[0], email_credentials[1]) #login using credital file 
    
    smtpobj.send_message(message) #used to send message method and pass the object of sendemail class
    
    messagebox.showinfo("Information", 'Email Sent Successfully') #message is used to shwo the message 
    #box that email is sent 

def sendmail():
    if toEntryField.get() == '':
        messagebox.showerror("Error", "Fill all fields")
    else:
        sendemail(toEntryField.get(), Email_text_area.get(1.0, tk.END)) #passed parameters here 
        #the entryfield data the text area data 

#created a settings functions to use in configure button 
def settings():
    def clear(): #defined a clear function to clear the fields of email and password 
        email_Entry_field.delete(0, tk.END) #clear the entry field of the email 
        password_field.delete(0, tk.END) #clear the password field 

    def save():  #created a function to save the senders email and password 
        #used an if condition to check if the email and password field are empty 
        if email_Entry_field.get() == '' or password_field.get() == '': 
            
            messagebox.showerror("Error", "All fields must be filled", parent=obj1) #if empty show error
        else:
            f = open('credential.txt', 'a') #else save them in a credential file 
            f.write(email_Entry_field.get() + ',' + password_field.get()) #writing the email and password
            #in the file 
            f.close()
            messagebox.showinfo("Information", "Credentials Saved Successfully", parent=obj1)
            #message box is used to show info that the info is saved successfully

    # Create a Toplevel object is used to show a pop on the origianl main window
    obj1 = tk.Toplevel() #created an object of toplevel class
    obj1.title("Settings") #title is settings 
    obj1.geometry('400x300+350+100') #created the size of the window
    obj1.config(bg='skyblue2') #provide the background color

    tk.Label(obj1, text="Email Configuration", font=('times new roman', '25', 'bold'), bg='white', fg='skyblue2').grid(
        padx=52) #created a lable for email configureation 

    #created a lable frame class to add email address field 
    email_address = tk.LabelFrame(obj1, text="Email Address", font=('times new roman', '15', 'bold'),
                               bd=5, fg='white', bg="skyblue2") 
    email_address.grid(row=2, column=0, pady=20) #added using grid method
    
    #created an entry field to enter the sender's email 
    email_Entry_field = tk.Entry(email_address, font=('times new roman', '13', 'bold'), width=30)
    email_Entry_field.grid(row=0, column=0) #used grid method to placed it on screen

    #created a lable and frame class for password field 
    password_field = tk.LabelFrame(obj1, text="Password", font=('times new roman', '15', 'bold'),
                               bd=5, fg='white', bg="skyblue2")
    password_field.grid(row=3, column=0, pady=20) #grid method to show it on main window 
     
     #created and password entry field to enter password
    password_field = tk.Entry(password_field, font=('times new roman', '13', 'bold'), width=30, show='*')
    password_field.grid(row=0, column=0)  #placed it using grid method
    
    #created a lable frame class for submit and clear button 
    submit_and_Clear_button = tk.LabelFrame(obj1, font=("times new roman", "10", "bold"), bd=5, fg='white', bg='skyblue2')
    submit_and_Clear_button.grid(row=4, column=0) #placed them using grid 
     
    #created a submit button with command save 
    tk.Button(submit_and_Clear_button, text="Submit", font=("text new roman", "10", "bold"),
              cursor="hand2", bd="0", bg="dodger blue2", activebackground="skyblue2", border=3, command=save).grid(row=0, column=0)
    
    #created a clear button with command clear 
    tk.Button(submit_and_Clear_button, text="Clear", font=("text new roman", "10", "bold"),
              cursor="hand2", bd="0", bg="dodger blue2", activebackground="skyblue2", border=3, command=clear).grid(row=0, column=5, padx=10)

    obj1.mainloop() #main loop of the toplevel class

# Create the main GUI window
obj = tk.Tk() #object of the tk class
obj.title("Attendance App") #gives the title to the gui window
obj.geometry('500x500+350+100') #height and width  of the window 
obj.config(bg='skyblue2') #gives the background color

titleframe = tk.Frame(obj, bg='white') #creating a frame  and passed the object of the main gui window

titleframe.grid(row=0, column=0) #grid to add on the window on row 0 and column 0

logo_image = Image.open('logo.jpg') #opened the image using pillow library
logo_image = logo_image.resize((100, 100)) #resized the image to 100 by 100 pixles 
logo_image = ImageTk.PhotoImage(logo_image) #changed the image to photoimage imagetk module

titlelabel_image = tk.Label(titleframe, image=logo_image, bg="white", padx=30) #used to display boxes and 
#the object of the titleframe class is passed in it 

titlelabel_image.grid(row=0, column=0, padx=15) #use grid method to put on the title frame on row and column 0 

titlelabel_text = tk.Label(titleframe, text="Govt P.G. College Una \n MCA Department", font=('times new roman', '25', 'bold'),
                           bg='white', fg='skyblue2') #used another lable to write the text

titlelabel_text.grid(row=0, column=1, padx=21) #placed it in column 1 to 

email_address_space = tk.LabelFrame(obj, text="Email Address", font=('times new roman', '15', 'bold'), bd=5,
                                    fg='white', bg="skyblue2") #created another lable on the main gui 
#window for the email space 


email_address_space.grid(row=2, column=0, pady=20) #placed it in the main frame using grid method

#created and entry field to write email
toEntryField = tk.Entry(email_address_space, font=('times new roman', '12', 'bold'), width=30)

toEntryField.grid(row=0, column=0) #placed it in the lable

email_written = tk.LabelFrame(obj, text="Compose Email", font=('times new roman', '15', 'bold'), bd=5,
                              fg='white', bg='skyblue2')  #created a lable to compose mail

email_written.grid(row=5, column=0) #placed it on the main gui window using grid method

#created an button on the lable email written to attach the file and added a command 
tk.Button(email_written, text="Attachment", font=("text new roman", "10", "bold"), cursor="hand2",
          bd="0", bg="skyblue2", activebackground="skyblue2", border=3, command=attachment).grid(row=0, column=0)

#email text area is used to write email
Email_text_area = tk.Text(email_written, font=("times new roman", "10", "bold"), height=8, width=55)
Email_text_area.grid(row=1, column=0) #placed using grid method

#created a lableframe to submit button and settings 
submit_button_and_Settings = tk.LabelFrame(obj, font=("times new roman", "10", "bold"), bd=5, fg='white', bg='skyblue2')
submit_button_and_Settings.grid(row=6, column=0) #placed it using grid method

#create da button for submit or send mail and used a command 
tk.Button(submit_button_and_Settings, text="Submit", font=("text new roman", "10", "bold"), cursor="hand2",
          bd="0", bg="skyblue2", activebackground="skyblue2", border=3, command=sendmail).grid(row=0, column=0)
#created a button to configure email and used command 
tk.Button(submit_button_and_Settings, text="Configure email", font=("text new roman", "10", "bold"),
          cursor="hand2", bd="0", bg="skyblue2", command=settings, activebackground="skyblue2", border=3).grid(row=0, column=3, padx=30)

obj.mainloop() #use to show window continously
