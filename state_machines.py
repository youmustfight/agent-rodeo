import enum
import logging
from transitions import Machine, State

# LOGGING
logging.basicConfig(level=logging.INFO) # DEBUG

# ==========================================================
# State Machine without tracking internal data/context
# ==========================================================

# MACHINE
# --- states
class States(enum.Enum):
    CLOSED = 'CLOSED'
    OPENED = 'OPENED'
    BROKEN = 'BROKEN'
# --- actions
def knock_and_say_something(phrase: str = ""):
    print('*knock* *knock* *knock*')
    if len(phrase) > 0: print(phrase)
# --- init
OpenCloseMachine = Machine(
    states=[
        State(name=States.CLOSED),
        State(name=States.OPENED),
        State(name=States.BROKEN),
    ],
    transitions=[
        # CLOSED
        { 'trigger': 'open', 'source': States.CLOSED, 'dest': States.OPENED },
        { 'trigger': 'knock', 'source': States.CLOSED, 'dest': None, 'after': knock_and_say_something }, # 'dest' is required, but None means its internal transition
        # OPEN
        { 'trigger': 'close', 'source': States.OPENED, 'dest': States.CLOSED },
        { 'trigger': 'knock', 'source': States.OPENED, 'dest': None, 'after': knock_and_say_something },
    ],
    initial=States.CLOSED,
)

# TEST PRINTS
print('======= v1 =======')
OpenCloseMachine.knock()
OpenCloseMachine.knock(phrase='hello anyone around?')
OpenCloseMachine.open()
OpenCloseMachine.close()
try:
    OpenCloseMachine.open()
except Exception as err:
    # this will throw an err because we have no transition back
    print(err)



# ==========================================================
# State Machine with tracking internal data/context (re-using above w/ model)
# ==========================================================

class Door(object):
    # MACHINE DEFS
    # --- states
    machine_states = [
        State(name=States.CLOSED),
        State(name=States.OPENED),
        State(name=States.BROKEN),
    ]
    # --- actions
    def cond_can_open(self):
        return self.broken == False and self.locked == False
    def action_lock(self):
        print('*click*')
        self.locked = True
    def action_unlock(self):
        print('*clack*')
        self.locked = False
    def action_break_it(self):
        self.broken = True
    def action_fix_it(self):
        self.broken = False
    # --- transitions
    machine_transitions = [
        # CLOSED
        { 'trigger': 'open', 'source': States.CLOSED, 'dest': States.OPENED, 'conditions': ['cond_can_open'] },
        { 'trigger': 'break_it', 'source': States.CLOSED, 'dest': States.BROKEN },
        { 'trigger': 'knock', 'source': States.CLOSED, 'dest': None, 'after': [knock_and_say_something] },
        { 'trigger': 'lock', 'source': States.CLOSED, 'dest': None, 'after': ['action_lock'] },
        { 'trigger': 'unlock', 'source': States.CLOSED, 'dest': None, 'after': ['action_unlock'] },
        # OPEN
        { 'trigger': 'close', 'source': States.OPENED, 'dest': States.CLOSED },
        { 'trigger': 'break_it', 'source': States.OPENED, 'dest': States.BROKEN },
        { 'trigger': 'knock', 'source': States.OPENED, 'dest': None, 'after': [knock_and_say_something] },
        { 'trigger': 'lock', 'source': States.OPENED, 'dest': None, 'after': ['action_lock'] },
        { 'trigger': 'unlock', 'source': States.OPENED, 'dest': None, 'after': ['action_unlock'] },
        # BROKEN
        # ... no state changes allowed
        { 'trigger': 'fix', 'source': States.BROKEN, 'dest': States.OPENED },
    ]
    # INIT
    def __init__(self):
        self.machine = Machine(
            model=self,
            states=self.machine_states,
            transitions=self.machine_transitions,
            initial=States.CLOSED,
            ignore_invalid_triggers=True # if a state tries to occur that's not allowed, don't raise err for now
        )
        # --- context/vars we're going to do conditioning on
        self.broken = False
        self.locked = False


# TEST PRINTS
print('======= v2 =======')
new_door = Door()
new_door.knock()
print('-')
print(new_door.state)
new_door.open()
print(new_door.state)
print('-')
new_door.close()
print('-')
new_door.open()
new_door.open() # trigger err
new_door.open() # trigger err
print('-')
print(new_door.state)
new_door.lock()
print(new_door.state)
print('-')
new_door.close()
print('-')
new_door.open()
new_door.open()
new_door.open()
print('-')
print(new_door.state)
new_door.unlock()
new_door.open()
print('-')
print(new_door.state)
