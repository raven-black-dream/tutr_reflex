import reflex as rx
from tutr_reflex.templates.template import template
from tutr_reflex.db import Attendance, db_Session, Person
from tutr_reflex.state import State, Option
from typing import List


class AttendanceObject(rx.Base):
    id: int = 0
    attended: bool = False
    passed: bool = False
    name: str = ""


class AttendanceState(State):

    session: db_Session | None = None
    class_name: str = ""
    attendance_list: List[AttendanceObject] = []

    @rx.var
    def session_id(self):
        return self.router.page.params.get('pid', 'no pid')

    def get_session(self):
        with rx.session() as session:
            self.session = session.exec(db_Session.select.where(db_Session.id == self.session_id)).first()
            self.class_name = self.session.class_info.class_name

            self.attendance_list = [
                AttendanceObject(
                    id=item.id,
                    name=item.person.sca_name,
                    attended=item.attended,
                    passed=item.passed)
                for item in self.session.roll_list
            ]

    def update_attendance(self, id:int, value:bool):
        with rx.session() as session:
            row = session.exec(Attendance.select.where(Attendance.id == id)).first()
            row.attended = value
            session.commit()

    def update_pass_fail(self, id:int, value:bool):
        with rx.session() as session:
            row = session.exec(Attendance.select.where(Attendance.id == id)).first()
            row.passed = value
            session.commit()

    def remove_person(self, id:int):
        with rx.session() as session:
            row = session.exec(Attendance.select.where(Attendance.id == id)).first()
            session.delete(row)
            session.commit()
            self.get_session()


class AttModalState(AttendanceState):
    show: bool = False

    @rx.var
    def person_list(self) -> List[Option]:
        with rx.session() as session:
            people = session.exec(Person.select.where()).all()
            return [Option(value=prsn.id, label=prsn.sca_name) for prsn in people]
    def handle_submit(self, form_data: dict):
        with rx.session() as session:
            session.add(
                Attendance(
                    person_id=form_data['person_id'],
                    session_id=AttendanceState.session.id,
                    attended=False,
                    passed=False
                )
            )
            session.commit()
            self.show = not self.show

    def toggle_modal(self):
        self.show = not self.show



@template(route='/sessions/[pid]', title='Attendance', on_load=AttendanceState.get_session())
def attendance():
    return rx.box(
        rx.vstack(
            rx.heading(
                AttendanceState.class_name,
            ),
            rx.hstack(
                rx.text('Start Time: '),
                rx.text(AttendanceState.session.start_time),
            ),
            rx.hstack(
                rx.text('End Time: '),
                rx.text(AttendanceState.session.end_time),
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Attendance"),
                    rx.divider(),
                    rx.table_container(
                        rx.table(
                            rx.thead(
                                rx.tr(
                                    rx.th('Name'),
                                    rx.th('Attended'),
                                    rx.th('Passed'),
                                    rx.th('Actions')
                                )
                            ),
                            rx.tbody(
                                rx.foreach(
                                    AttendanceState.attendance_list,
                                    lambda item:
                                    rx.tr(
                                        rx.td(
                                            rx.text(item.name)
                                        ),
                                        rx.td(
                                            rx.checkbox(
                                                is_checked=item.attended,
                                                on_change=lambda value, id=item.id: AttendanceState.update_attendance(
                                                    id, value)
                                            )
                                        ),
                                        rx.td(
                                            rx.checkbox(
                                                is_checked=item.passed,
                                                on_change=lambda value, id=item.id: AttendanceState.update_pass_fail(id,
                                                                                                                     value)
                                            )
                                        ),
                                        rx.td(
                                            rx.hstack(
                                                rx.cond(
                                                    item.attended,
                                                    rx.button(
                                                        "Mark Absent",
                                                        on_click=lambda id=item.id: AttendanceState.update_attendance(
                                                            id, False)
                                                    ),
                                                    rx.button(
                                                        "Mark Present",
                                                        on_click=lambda id=item.id: AttendanceState.update_attendance(
                                                            id, True)
                                                    )
                                                ),
                                                rx.cond(
                                                    item.attended,
                                                    rx.cond(
                                                        item.passed,
                                                        rx.button(
                                                            "Mark Failed",
                                                            on_click=lambda id=item.id: AttendanceState.update_pass_fail(
                                                                id, False)
                                                        ),
                                                        rx.button(
                                                            "Mark Passed",
                                                            on_click=lambda id=item.id: AttendanceState.update_pass_fail(
                                                                id, True)
                                                        ),

                                                    ),
                                                ),
                                                rx.button(
                                                    "Remove Person",
                                                    on_click=lambda id=item.id: AttendanceState.remove_person(id)

                                                ),

                                            )
                                        )
                                    )

                                )
                            )
                        )
                    ),
                    rx.button("Add Person", on_click=AttModalState.toggle_modal),
                    rx.modal(
                        rx.modal_overlay(
                            rx.modal_content(
                                rx.modal_header("Add Person"),
                                rx.modal_body(
                                    rx.modal_content(
                                        rx.form(
                                            rx.vstack(
                                                rx.vstack(
                                                    rx.text("Person"),
                                                    rx.select(
                                                        rx.foreach(
                                                            AttModalState.person_list,
                                                            lambda option: rx.option(option.label, value=option.value)
                                                        ),
                                                        id='person_id'
                                                    )
                                                ),
                                                rx.button("Submit", type_='submit')
                                            ),
                                            on_submit=AttModalState.handle_submit,
                                        )

                                    )
                                ),
                            )
                        ),
                        is_open=AttModalState.show,
                        on_overlay_click=AttModalState.toggle_modal,
                        on_esc=AttModalState.toggle_modal,
                    ),
                ),
                width='100%',
            )
        )
    )