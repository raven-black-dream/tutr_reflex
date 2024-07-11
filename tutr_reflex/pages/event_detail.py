import reflex as rx
from tutr_reflex.db import Class, db_Session
from tutr_reflex.templates.template import template
from tutr_reflex.state import EventDetailState, Option
from typing import List


class ModalState(EventDetailState):

    show: bool = False

    @rx.var
    def class_list(self) -> List[Option]:
        with rx.session() as session:
            classes = session.exec(Class.select.where()).all()
            return [Option(value=cls.id, label=cls.class_name) for cls in classes]

    def handle_submit(self, form_data: dict):
        with rx.session() as session:
            session.add(
                db_Session(
                    class_id=form_data['class_id'],
                    event_id=EventDetailState.event_data.id,
                    start_time=form_data['start_time'],
                    end_time=form_data['end_time']
                )
            )
            session.commit()
            self.show = not self.show

    def toggle_modal(self):
        self.show = not self.show


@template(route="/events/[pid]", title="Event Details", on_load=EventDetailState.get_event())
def event_detail() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                EventDetailState.event_data.event_name,
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Start Date: "),
                        rx.text(EventDetailState.event_data.start_date),
                    ),
                    rx.hstack(
                        rx.text("End Date: "),
                        rx.text(EventDetailState.event_data.end_date),
                    ),
                    rx.hstack(
                        rx.text("Tutr Surcharge: "),
                        rx.text(EventDetailState.event_data.tutr_surcharge),
                    ),
                    rx.hstack(
                        rx.text('TUTR Coordinator: '),
                        rx.text(EventDetailState.coordinator),
                    )

                ),
                border='1px solid black',
                border_radius='15px',
                bg='whitesmoke',
                padding='1em',
                margin='1em',
                width='50%'
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Branch: "),
                        rx.text(EventDetailState.branch),
                    ),
                    rx.hstack(
                        rx.text("Location Name: "),
                        rx.text(EventDetailState.event_data.location_name),
                    ),
                    rx.hstack(
                        rx.text("Apt Num: "),
                        rx.text(EventDetailState.event_data.apt_num),
                    ),
                    rx.hstack(
                        rx.text("Street: "),
                        rx.text(EventDetailState.event_data.street),
                    ),
                    rx.hstack(
                        rx.text("City: "),
                        rx.text(EventDetailState.event_data.city),
                    ),
                    rx.hstack(
                        rx.text("Postal Code: "),
                        rx.text(EventDetailState.event_data.postal_code),
                    ),
                ),
                border='1px solid black',
                border_radius='15px',
                bg='whitesmoke',
                padding='1em',
                margin='1em',
                width='50%'
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Classes", level=3),
                    rx.table_container(
                        rx.table(
                            rx.thead(
                                rx.tr(
                                  rx.th("Class Name"),
                                  rx.th("Length"),
                                  rx.th('Cost'),
                                  rx.th("Teacher"),
                                ),
                            ),
                            rx.tbody(
                                rx.foreach(
                                    EventDetailState.event_classes,
                                    lambda row: rx.tr(
                                        rx.td(
                                            rx.link(row.class_name, href=f'/sessions/{row.session_id}')
                                        ),
                                        rx.td(row.class_length),
                                        rx.td(row.cost),
                                        rx.td(
                                            rx.link(row.teacher, href=f'/members/{row.teacher_id}')
                                        ),
                                    ),
                                )
                            )
                        )
                    )

                ),
                border='1px solid black',
                border_radius='15px',
                bg='whitesmoke',
                padding='1em',
                margin='1em',
                width='75%'
            ),
            rx.button("Add Class", on_click=ModalState.toggle_modal),
            rx.modal(
                rx.modal_overlay(
                    rx.modal_content(
                        rx.modal_header("Add Class"),
                        rx.modal_body(
                            rx.modal_content(
                                rx.form(
                                    rx.vstack(
                                        rx.vstack(
                                            rx.text("Class"),
                                            rx.select(
                                                rx.foreach(
                                                    ModalState.class_list,
                                                    lambda option: rx.option(option.label, value=option.value)
                                                ),
                                                id='class_id'
                                            )
                                        ),
                                        rx.hstack(
                                            rx.text("Start Time"),
                                            rx.input(type='time', id='start_time')
                                        ),
                                        rx.hstack(
                                            rx.text("End Time"),
                                            rx.input(type='time', id='end_time')
                                        ),
                                        rx.button("Submit", type_='submit')
                                    ),
                                    on_submit=ModalState.handle_submit,
                                )

                            )
                        ),
                    )
                ),
                is_open=ModalState.show,
                on_overlay_click=ModalState.toggle_modal,
                on_esc=ModalState.toggle_modal,
            ),

        )
    )