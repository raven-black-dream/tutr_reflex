import reflex as rx
from tutr_reflex.state import PersonUpdateState
from tutr_reflex.templates.template import template
from tutr_reflex.components.member_form import member_form


@template(route="/members/[pid]/update", title="Update Member", on_load=PersonUpdateState.initialize)
def person_update() -> rx.Component:
    return member_form(
        sca_name=PersonUpdateState.person_dict.sca_name,
        first_name=PersonUpdateState.person_dict.first_name,
        last_name=PersonUpdateState.person_dict.last_name,
        branch=PersonUpdateState.branch,
        position=PersonUpdateState.person_dict.position,
        teacher=PersonUpdateState.person_dict.teacher,
        active=PersonUpdateState.person_dict.active,
        minor=PersonUpdateState.person_dict.minor,
        guardian=PersonUpdateState.guardian,
    )
