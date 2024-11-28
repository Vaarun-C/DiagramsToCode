class detection_object:
    def __init__(self, detection_box=[], class_type: str = None, confidence: float = 0.00) -> None:
        self.box = detection_box
        self.classType = class_type
        self.confidenceValue = confidence

    def to_dict(self):
        return {"pos": self.box, "classType": self.classType, "confidence": self.confidenceValue}

class Group:
    def __init__(self, x,y,w,h,group_type=None) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.group_type = group_type
    
    def __repr__(self):
        if self.group_type is None:
            return f'Group[{(self.x,self.y)=}, {self.w=}, {self.h=}]'
        return f'Group[{self.group_type}][{(self.x,self.y)=}, {self.w=}, {self.h=}]'

    def to_dict(self):
        return {"pos": [ self.x, self.y, self.w, self.h], "group_type": self.group_type}
