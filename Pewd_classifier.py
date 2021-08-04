from Scrapper.insta import Hashtag
from Recognizer.recognize import ClassifyPweds

#Download test set
hash_tag = Hashtag("Pewdiepie")
hash_tag.get_links()
hash_tag.download_images('/home/maskedman/Pewdiepie/test')
print ("Total image downloaded for classification: ", hash_tag.total_post)

#Classify test set
classes = ClassifyPweds('cnn')
classes.encode_train()
classes.classify_pewds('/home/maskedman/Pewdiepie/test')
print("Classification Done")

