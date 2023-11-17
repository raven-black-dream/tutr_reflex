import reflex as rx
from tutr_reflex.state import State
from tutr_reflex.templates.template import template
from tutr_reflex.db import Person
from typing import List


class PersonListState(State):
    people: List[Person]

    def get_people(self):
        with rx.session() as session:
            self.people = session.exec(
                Person.select([Person.id, Person.first_name, Person.last_name, Person.sca_name, Person.branch.branch_name])
                ).all()



class PersonDetailState(State):
    person: Person

    @rx.var
    def person_id(self) -> str:
        return self.router.page.params.get('pid', 'no pid')

    def get_person(self):
        with rx.session() as session:
            self.person = session.exec(Person.select.where(Person.id.equals(PersonDetailState.person_id))).one()


class PersonUpdateState(PersonDetailState):

    def handle_submit(self, form_data:dict):
        pass


@template(route="/members", title="Members")
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

@template(route="/members/[pid]", title="Member Detail")
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

@template(route="/members/[pid]/update", title="Update Member")
def person_update():
    pass