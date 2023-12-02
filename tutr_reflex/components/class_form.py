import reflex as rx
from tutr_reflex.state import ClassUpdateState


def class_form(
        class_name: str = '',
        length: str = "0.0",
        cost: str = "0.0",
        min_participants: str = "1",
        max_participants: str = "1",
        travel:bool = False,
        student_requirements: str = '',
        location_requirements: str = '',
        description: str = '',
        prerequisites: str = '',
        approved: bool = False,
        designation: str = '',
        person: str = ''

):
    return rx.container(
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.text('Class Name: '),
                    rx.input(
                        id='class_name',
                        default_value=class_name
                    ),
                ),
                rx.hstack(
                    rx.text("Class Designation"),
                    rx.select(
                        rx.foreach(
                            ClassUpdateState.class_designation_options,
                            lambda option: rx.option(
                                option.label,
                                value=option.value,
                            ),
                        ),
                        id='class_designation',
                        default_value=designation
                    )
                ),
                rx.hstack(
                    rx.text(),
                    rx.select(
                        rx.foreach(
                            ClassUpdateState.teacher_options,
                            lambda option: rx.option(
                                option.label,
                                value=option.value,
                            ),
                        ),
                        id='teacher',
                        default_value=person
                    )
                ),
                rx.hstack(
                    rx.text('Class Length: '),
                    rx.input(
                        id='length',
                        default_value=length
                    ),
                ),
                rx.hstack(
                    rx.text('Cost: '),
                    rx.input(
                        id='cost',
                        default_value=cost
                    ),
                ),
                rx.hstack(
                    rx.text('Minimum Participants: '),
                    rx.input(
                        id='min_participants',
                        default_value=min_participants
                    )
                ),
                rx.hstack(
                    rx.text('Maximum Participants: '),
                    rx.input(
                        id='max_participants',
                        default_value=max_participants
                    )
                ),
                rx.vstack(
                    rx.text('Prerequisites: '),
                    rx.text_area(
                        id='prerequisites',
                        default_value=prerequisites
                    )
                ),
                rx.vstack(
                    rx.text("Description: "),
                    rx.text_area(
                        id='description',
                        default_value=description
                    )
                ),
                rx.vstack(
                    rx.text('Student Requirements: '),
                    rx.text_area(
                        id='student_requirements',
                        default_value=student_requirements
                    )
                ),
                rx.vstack(
                    rx.text('Location Requirements: '),
                    rx.text_area(
                        id='location_requirements',
                        default_value=location_requirements
                    )
                ),                
                rx.checkbox_group(
                    rx.switch(
                        'Willing to Travel',
                        on_change=ClassUpdateState.travel_on_change,
                        is_checked=travel,
                        id='travel',
                    ),
                    rx.switch(
                        'Class Approved',
                        on_change=ClassUpdateState.approved_on_change,
                        is_checked=approved,
                        id='approved',
                    ),
                ),
                rx.button(
                    "Submit",
                    type_='submit',
                    color_scheme='blue'
                )
            ),
            on_submit=ClassUpdateState.handle_submit,
        )
    )