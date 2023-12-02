import reflex as rx
from tutr_reflex.templates.template import template
from tutr_reflex.state import State

class AttendanceState(State):
    pass

@template(route='/sessions/[pid]', title='Attendance', on_load=AttendanceState.get_session())
def attendance():
    pass