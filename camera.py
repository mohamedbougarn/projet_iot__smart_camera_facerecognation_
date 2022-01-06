from mail import sendEmail, sendEmail1
import face_recognition
import cv2
import numpy as np
import os
import time
import sys


face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6


email_update_interval = 10 #Interval de temps d'envoie d'un mail
#video_camera = VideoCamera(flip=True) #Crée un objet caméra, retournez verticalement

#Store objects in array
known_person=[] #Name of person string
known_image=[] #Image object
known_face_encodings=[] #Encoding object

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

#Loop to add images in friends folder
for file in os.listdir("profiles"):
    try:
        #Extracting person name from the image filename eg: david.jpg
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("profiles/", file)
        known_image = face_recognition.load_image_file(file)
        #print("test")
        #print(face_recognition.face_encodings(known_image)[0])
        known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
        #print(known_face_encodings)

    except Exception as e:
        pass
    
#print(len(known_face_encodings))
#print(known_person)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        
        process_this_frame = True
        
            # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
       # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            global name_gui;
            #face_names = []
            #+'.DS_Store'
            for face_encoding in face_encodings :
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                #print(face_encoding)
                print(matches)

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_person[best_match_index]

                print(name)
                #print(face_locations)
                face_names.append(name)
        
                name_gui = name
                if(name=="Unknown"):
                    #while True:
                    try:
                        #print("limage = ".image)
                        #cv2.imwrite("templates/photo.jpg", image)
                        cv2.imwrite("photo.jpg", image)
                        #frame,found_obj = video_camera.get_object(image)  # appelation la fonction de videm_camera.get_object qui est dans le fichier camera.py
                        #if found_obj and (time.time() - last_epoch) > email_update_interval:  # Test si objet trouvé et si le temps actuel - temps de la dernière > interval mail
                        # last_epoch = time.time()  # Changement de la valeur last_epoch par le temps du dernier mouvement
                        print("Envoie mail")  # Affichage du texte dans le terminal
                        sendEmail()  # Utilisation de la fonction sendEmail du fichier mail.py avec récupération de frame et du found_obj pour intégration dans le mail
                        #sendEmail(image)  # Utilisation de la fonction sendEmail du fichier mail.py avec récupération de frame et du found_obj pour intégration dans le mail
                        #sendEmail1()  # Utilisation de la fonction sendEmail du fichier mail.py avec récupération de frame et du found_obj pour intégration dans le mail
                        #print("limage = ".image)
                        print("Fait")  # Affichage du texte dans le terminal
                    except:
                        print("PB envoie mail",sys.exc_info()[0])  # Affiche des erreurs dans le terminal lors du non envoie du mail

                    #cv2.imwrite("photo.jpg", image)
                    #print("face scan compleet .")
                    #cap.release()
                    #print("face scan compleet .")
                    #sendEmail("photo.jpg")
                ##test if name unknown then send email
        process_this_frame = not process_this_frame
            
# Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (255, 255, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name_gui, (left + 10, bottom - 10), font, 1.0, (0, 0, 0), 1)

        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
