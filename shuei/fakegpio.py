class fakegpio:
    HIGH = True
    LOW = False
    IN = True
    OUT = False
    pins = {} 
    def setup (self, pin, mode):
        self.pins[pin] = {mode:mode, state:false}
    def output (self, pin, state):
        if self.pins[pin][mode]: raise f'Pin {pin} is not set as output!'
        else: self.pins[pin][state] = state
    def input (self, pin):
        return self.pins[pin][state]
GPIO = fakegpio()
