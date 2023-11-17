import reflex as rx
from tutr_reflex.state import State
from tutr_reflex.templates.template import template
from typing import List


class PersonListState(State):

    @rx.var()
    def people() -> List:
        return []


class PersonDetailState(State):
    
    @rx.var()
    def person():
        return {}


class PersonUpdateState(State):
    pass


@template(route="/members", title="Members", image="/github.svg")
def person_list():
    return rx.container(
        rx.foreach(
            PersonListState.people,
            lambda x: rx.hstack(
                rx.text(),
                rx.text(),
                rx.text(),
                rx.link(rx.button("View"), href='', button=True),
                rx.link(rx.button("Delete"), href='', button=True)
            )

        )
    )

@template(route="/members/[pid]", title="Member Detail", image="/github.svg")
def person_detail():
    return rx.container(
        rx.vstack(
            rx.heading(),
            rx.hstack(rx.text("FirstName"), rx.text("LastName")),
            rx.divider(),
            rx.heading("Degrees"),
            rx.data_table(),
            rx.divider(),
            rx.heading("Class History"),
            rx.data_table()
        )
    )
    pass

@template(route="/members/[pid]/update", title="Update Member", image="/github.svg")
def person_update():
    pass