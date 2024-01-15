import cv2
import pickle
import face_recognition
import csv
from datetime import datetime

video = cv2.VideoCapture(1)
face_cap = cv2.CascadeClassifier("C:/Users/Lenovo/AppData/Local/Programs/Python/Python311/Lib/site-packages/cv2/data"
    "/haarcascade_frontalface_default.xml")
now = datetime.now()

f = open("Attendance.csv", 'w')
Wtr = csv.writer(f)
f.close()
f = open("Attendance.csv", 'a')
wtr = csv.writer(f)
wtr.writerow(["Sr. no", "Name", "ID", "Department", "Time"])

Modes = ['Active.png', 'Identity.png', 'Marked.png']
ImageModes = []
Marked = {}

for mode in Modes:
    ImageModes.append(cv2.imread(mode))
mode = 1
Time = 0
NoOfAttendees = 1

temp = cv2.imread('background.png')
HomePage = cv2.resize(temp, (1240, 775))

with open('data.pkl', 'rb') as file:
    CombinedList = pickle.load(file)
StudentKnown, StudentId = CombinedList

for Id in StudentId:
    Marked[Id] = False

Database = {'28600': ['Cristiano Ronaldo', 'CSE'],
            '28601': ['Elon Musk', 'ECE'],
            '28602': ['Narendra Modi', 'CIV'],
            '28603': ['Virat Kohli', 'MECH'],
            '28604': ['Bill Gates', 'CSE'],
            '28605': ['Soham Anwane', 'CSE']}


def find(is_same):
    for i in range(0, len(is_same)):
        if is_same[i]:
            return i
    return -1


while True:
    success, image = video.read()
    img = cv2.resize(image, (643, 614), None, 0.75, 0.75)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_location = face_recognition.face_locations(img)
    face_encoding = face_recognition.face_encodings(img, face_location)

    face = face_cap.detectMultiScale(img)
    for x, y, width, height in face:
        cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 3)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    HomePage[144: 758, 19: 662] = img
    HomePage[18: 761, 707: 1221] = ImageModes[mode]

    for face_encode, face_location in zip(face_encoding, face_location):
        AreTheySame = face_recognition.compare_faces(face_encode, StudentKnown)
        index = find(AreTheySame)

        if mode == 1:
            if index < len(AreTheySame):
                cv2.putText(HomePage, Database[StudentId[index]][0], (866, 550), cv2.FONT_HERSHEY_PLAIN, 1.6, (0, 0, 0),
                            2)
                cv2.putText(HomePage, StudentId[index], (866, 620), cv2.FONT_HERSHEY_PLAIN, 1.6, (0, 0, 0), 2)
                cv2.putText(HomePage, Database[StudentId[index]][1], (866, 692), cv2.FONT_HERSHEY_PLAIN, 1.6, (0, 0, 0),
                            2)
                CurrStudent = cv2.imread(f"{StudentId[index]}.png")
                HomePage[100: 480, 778: 1151] = cv2.resize(CurrStudent, (373, 380))
                Marked[StudentId[index]] = True
                if Time > 5:
                    wtr.writerow(
                        [NoOfAttendees, Database[StudentId[index]][0], StudentId[index], Database[StudentId[index]][1],
                         str(now)[:19]])
                    NoOfAttendees += 1
                    mode = 2
            Time += 1

    if len(face_location) == 0:
        Time = 0
        mode = 1

    cv2.imshow('Face Attendance', HomePage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

f.close()

with open('Attendance.csv', 'r') as file:
    wtr = csv.reader(file)
    List = []
    for row in wtr:
        if len(row) != 0:
            List.append(row)

for i in range(1, len(List) - 1):
    for j in range(i + 1, len(List)):
        if List[i][1:4] == List[j][1:4]:
            List.remove(List[j])

with open('Attendance.csv', 'w') as file:
    wtr = csv.writer(file)
    for row in List:
        wtr.writerow(row)
