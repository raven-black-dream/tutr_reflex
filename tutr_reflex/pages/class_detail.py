import reflex as rx
from tutr_reflex.templates import template
from tutr_reflex.state import ClassDetailState


@template(route="/classes/[pid]", title="Class Detail", on_load=ClassDetailState.get_class)
def class_detail():
    return rx.box(
        rx.vstack(
            rx.heading(ClassDetailState.class_data.class_name),
            rx.heading(ClassDetailState.teacher, level=2, color='blue'),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Length: "),
                        rx.text(ClassDetailState.class_data.class_length)
                    ),
                    rx.hstack(
                        rx.text("Credits: "),
                        rx.text(ClassDetailState.credits)
                    ),
                    rx.hstack(
                        rx.text("Cost: "),
                        rx.text(ClassDetailState.class_data.cost)
                    ),
                    rx.hstack(
                        rx.text('Minimum Number of Participants: '),
                        rx.text(ClassDetailState.class_data.min_participants)
                    ),
                    rx.hstack(
                        rx.text('Maximum Number of Participants: '),
                        rx.text(ClassDetailState.class_data.max_participants)
                    ),
                    rx.hstack(
                        rx.text('Willing to Travel: '),
                        rx.switch(
                            is_checked=ClassDetailState.class_data.travel,
                            is_disabled=True
                        )
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
                    rx.container(
                        rx.vstack(
                            rx.heading('Prerequisites', level=3),
                            rx.text(ClassDetailState.class_data.prerequisites),
                        ),
                    ),
                    rx.container(
                        rx.vstack(
                            rx.heading('Description', level=3),
                            rx.text(ClassDetailState.class_data.description, width='100%'),
                        ),

                    ),
                    rx.container(
                        rx.vstack(
                            rx.heading('Student Requirements', level=3),
                            rx.text(ClassDetailState.class_data.student_requirements),
                        ),
                    ),
                    rx.container(
                        rx.vstack(
                            rx.heading('Location Requirements', level=3),
                            rx.text(ClassDetailState.class_data.location_requirements)
                        ),
                    ),
                ),
                border='1px solid black',
                border_radius='15px',
                bg='whitesmoke',
                padding='1em',
                margin='1em',
                width='50%'
            ),

        ),
    )