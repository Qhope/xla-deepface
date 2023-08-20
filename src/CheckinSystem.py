from deepface import DeepFace
import cv2

class CheckinSystem :
    def __init__(self, db_path, model_name = "VGG-Face"):
        self.db_path = db_path
        self.model_name = model_name
        self.model = DeepFace.build_model(self.model_name)
        self.DeepFace = DeepFace
    
    def checkin(self, image):
        result = self.DeepFace.find(img_path = image, db_path = self.db_path, model_name = self.model_name, distance_metric="euclidean")
        print(result)
        if(len(result[0]) == 0):
            return None
        n_result = result[0].to_numpy()[0]
        return n_result
    
    def visualize(self, query_image_path, db_image_path):
        query_image = cv2.imread(query_image_path)
        db_image = cv2.imread(db_image_path)

        # resize image to 400x400
        query_image = cv2.resize(query_image, (400, 400))
        db_image = cv2.resize(db_image, (400, 400))
        # concat image
        image = cv2.hconcat([query_image, db_image])

        cv2.imshow("Image", image)
        cv2.waitKey(0)
