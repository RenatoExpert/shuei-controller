class fakegpio:
    HIGH = True
    LOW = False
    IN = True
    OUT = False
    pins = {} 
    def setup (pin, mode):
        pins[pin] = {mode:mode, state:false}
    def output (pin, state):
        if pins[pin][mode]: raise f'Pin {pin} is not set as output!'
        else: pins[pin][state] = state
    def input (pin):
        return pins[pin][state]

