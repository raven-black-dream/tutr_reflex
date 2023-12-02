import reflex as rx
from tutr_reflex.templates.template import template
from tutr_reflex.components.class_form import class_form
from tutr_reflex.state import ClassUpdateState

@template(route="/classes/[pid]/update", title="Update Class", on_load=ClassUpdateState.get_class)
def update_class() -> rx.Component:
    return class_form(
        class_name=ClassUpdateState.class_obj.class_name,
        length=ClassUpdateState.class_obj.class_length,
        cost=ClassUpdateState.class_obj.cost,
        min_participants=ClassUpdateState.class_obj.min_participants,
        max_participants=ClassUpdateState.class_obj.max_participants,
        travel=ClassUpdateState.class_obj.travel,
        student_requirements=ClassUpdateState.class_obj.student_requirements,
        location_requirements=ClassUpdateState.class_obj.location_requirements,
        description=ClassUpdateState.class_obj.description,
        prerequisites=ClassUpdateState.class_obj.prerequisites,
        approved=ClassUpdateState.class_obj.approved,
        designation=ClassUpdateState.class_obj.designation,
        person=ClassUpdateState.class_obj.person
    )
