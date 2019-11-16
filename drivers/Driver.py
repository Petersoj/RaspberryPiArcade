class Driver:

    def __init__(self):
        self.isOpen: bool = False

    def open(self, *args):
        self.isOpen = True
        print("opened driver")

    def write(self, x: int, y: int, value: int):
        print(f"wrote ({x}, {y}) to {value}")

    def flush(self):
        print("flushed")