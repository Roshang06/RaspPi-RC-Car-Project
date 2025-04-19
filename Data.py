class ControlData:
    def __init__(self):
        self.shift = False
        self.forward = False
        self.backward = False
        self.right = False
        self.left = False
    def __str__(self):
        return f"ControlData(shift={self.shift}, forward={self.forward}, backward={self.backward}, Right={self.right}, Left={self.left})"
    