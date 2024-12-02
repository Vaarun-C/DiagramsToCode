from ultralytics import YOLO
from PIL import Image
from states import detection_object
from ultralytics.engine.results import Results

class yolomodel:
    def __init__(self) -> None:       
        self.model = YOLO("/Users/varunchandrashekar/base/Projects/DiagramsToCode/Website/services/Group_Recognition/3_categories_best.pt")
        self.conf_thresh = 0.8
        self.CLS_NAME_TO_TYPE = {
            "Private-subnet_32": "Private_Subnet",
            "Public-subnet_32": "Public_Subnet",
            "Virtual-private-cloud-VPC_32": "VPC"
        }
        self.model_names = self.model.names

    def predict(self, architectureDiagram: Image) -> list[detection_object]:
        all_classes = list(range(3))

        results = self.model.predict(architectureDiagram, save=False, classes=all_classes, conf=self.conf_thresh)
        detections = results[0].boxes
        detection_objects = []
        
        for det in detections:
            x_min, y_min, x_max, y_max = det.xyxy[0].tolist()
            class_name = self.model_names[int(det.cls)]

            try:
                class_type = self.CLS_NAME_TO_TYPE[class_name]
            except KeyError:
                print(class_name, "Woah, Doesn't seem to be in list")

            detection_objects.append(detection_object([x_max, y_max, x_min, y_min], class_type, float(det.conf)))
        return detection_objects
if __name__ == "__main__":
    y = yolomodel()
    d = Image.open("/Users/varunchandrashekar/base/Projects/DiagramsToCode/test/test10.png")
    y.predict(d)