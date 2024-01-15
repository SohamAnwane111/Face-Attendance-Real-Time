import cv2
import face_recognition
import pickle
import os

folderName = 'Students'
FileList = os.listdir(folderName)
StudentImg = []
StudentId = []

for file in FileList:
    StudentImg.append(cv2.imread(os.path.join(folderName, file)))
    StudentId.append(file[:5:])


# openCV uses BGR, face-recognition uses RGB.
def encoder(student_img):
    encode_list = []
    for img in student_img:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


StudentKnown = encoder(StudentImg)
CombinedList = [StudentKnown, StudentId]

with open('data.pkl', 'wb') as file:
    pickle.dump(CombinedList, file)
