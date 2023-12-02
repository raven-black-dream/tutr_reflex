import reflex as rx
from tutr_reflex.templates import template
from tutr_reflex.components.class_form import class_form


@template(route="/class/create", title="Create Class")
def create_class():
    return class_form()
