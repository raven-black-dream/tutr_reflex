import reflex as rx
from tutr_reflex.templates.template import template
from tutr_reflex.state import EventDetailState

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
                width='50%'
            )

        )
    )