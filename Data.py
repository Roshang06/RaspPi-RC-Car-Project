class ControlData:
    def __init__(self):
        self.shift = False
        self.forward = False
        self.backward = False
        self.right = False
        self.left = False
    def __str__(self):
        return f"ControlData(shift={self.shift}, forward={self.forward}, backward={self.backward}, right={self.right}, left={self.left})"

    def to_string(self):
        return f"ControlData(shift={self.shift}, forward={self.forward}, backward={self.backward}, right={self.right}, left={self.left})"

    @classmethod
    def from_string(cls, s):
        # Remove 'ControlData(' and ')' then split key=value pairs
        s = s.strip()[len("ControlData("):-1]
        pairs = s.split(", ")
        obj = cls()
        for pair in pairs:
            key, value = pair.split("=")
            setattr(obj, key, value == "True")

        obj.Corrections()
        return obj
    def Corrections(self):
        if self.right and self.left:
            self.right = False
            self.left = False
    