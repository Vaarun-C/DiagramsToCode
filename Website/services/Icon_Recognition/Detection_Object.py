class detection_object:
    def __init__(self, detection_box=[], class_type: str = None, confidence: float = 0.00) -> None:
        self.box = detection_box
        self.classType = class_type
        self.confidenceValue = confidence

    def to_dict(self):
        return {"pos": self.box, "classType": self.classType, "confidence": self.confidenceValue}