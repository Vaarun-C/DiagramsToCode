from ultralytics import YOLO
from PIL import Image
from Detection_Object import detection_object
from ultralytics.engine.results import Results

class yolomodel:
    def __init__(self) -> None:       
        self.model = YOLO("298_icons_best.pt")
        self.conf_thresh = 0.6
        self.CLS_NAME_TO_TYPE = {
            "Arch_Amazon-Elastic-Container-Service_64": "AWS::ECS::Cluster",
            "Arch_Amazon-Simple-Storage-Service_64": "AWS::S3::Bucket",
            "Arch_AWS-Lambda_64": "AWS::Lambda::Function",
            "Arch_Amazon-RDS_64": "AWS::RDS::DBInstance",
            "Arch_AWS-Fargate_64": "AWS::ECS::Cluster",
            "Arch_Amazon-EC2_64": "AWS::EC2::Instance"
        }
        self.model_names = self.model.names

    def predict(self, architectureDiagram: Image) -> list[detection_object]:
        all_classes = set(range(298))
        removed_classes = set([57])
        allowed_classes = list(all_classes-removed_classes)

        results = self.model.predict(architectureDiagram, save=False, classes=allowed_classes, conf=self.conf_thresh)
        detections = results[0].boxes
        detection_objects = []
        
        for det in detections:
            print("DETE", det)
            x_min, y_min, x_max, y_max = det.xyxy[0].tolist()
            print(f"Class ID: {int(det.cls)}, Coordinates: ({x_min}, {y_min}, {x_max}, {y_max})")
            class_name = self.model_names[int(det.cls)]

            try:
                class_type = self.CLS_NAME_TO_TYPE[class_name]
            except KeyError:
                print(class_name, "not in Mongo yet !!!!")

            detection_objects.append(detection_object([x_max, y_max, x_min, y_min], class_type, float(det.conf)))
        return detection_objects