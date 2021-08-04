import face_recognition
import pickle
import cv2
import os
import subprocess

from collections import Counter

class ClassifyPweds:

    def __init__(self, method):
        self.train_locs = subprocess.check_output("ls /home/maskedman/Pewdiepie/dataset/Pewdiepie", shell=True).decode("utf-8").splitlines()
        self.Encodings = []
        self.Method = method
        self.true_pewds = 0
        self.false_pewds = 0

    def encode_train(self):
        for images in self.train_locs:
            imagePath = f'/home/maskedman/Pewdiepie/dataset/Pewdiepie/{images}'
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model=self.Method)
            self.Encodings = face_recognition.face_encodings(rgb, boxes)
    
    def classify_pewds(self, test_images):
        test_locs = subprocess.check_output(f"ls {test_images}", shell=True).decode("utf-8").splitlines()
        pewds_loc, non_pewds_loc = f"{test_images}/pewds", f"{test_images}/not_pewds"
        os.system(f"mkdir -p {pewds_loc}")
        os.system(f"mkdir -p {non_pewds_loc}")
        for i, images in enumerate(test_locs):
            if images in ['pewds', 'not_pewds']:
                continue
            imagePath = test_images+'/'+images
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model=self.Method)
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []
            for encoding in encodings:
                matches = face_recognition.compare_faces(self.Encodings, encoding)
                name = "Unknown"
                if True in matches:
                    name = 'Pewdiepie'
                names.append(name)
            if 'Pewdiepie' in names:
                self.true_pewds += 1
                cv2.imwrite(f"{pewds_loc}/{str(i)}.jpg", image)
            else:
                self.false_pewds += 1
                cv2.imwrite(f"{non_pewds_loc}/{str(i)}.jpg", image)
