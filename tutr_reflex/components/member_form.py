import reflex as rx
from tutr_reflex.state import PersonUpdateState


def member_form(
        sca_name: str = '',
        first_name: str = '',
        last_name: str = '',
        branch: str = '',
        position: str = '',
        teacher: bool = False,
        active: bool = True,
        minor: bool = False,
        guardian: str = '',

):
    return rx.container(
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.text('SCA Name: '),
                    rx.input(
                        id='sca_name',
                        default_value=sca_name
                    ),
                ),
                rx.hstack(
                    rx.text('First Name: '),
                    rx.input(
                        id='first_name',
                        default_value=first_name
                    ),
                ),
                rx.hstack(
                    rx.text('Last Name: '),
                    rx.input(
                        id='last_name',
                        default_value=last_name
                    ),
                ),
                rx.vstack(
                    rx.text('Branch: '),
                    rx.select(
                        rx.foreach(
                            PersonUpdateState.branch_options,
                            lambda option: rx.option(
                                option.label,
                                value=option.value,
                            ),

                        ),
                        id='branch',
                        default_value=branch
                    ),
                    width='100%'
                ),
                rx.vstack(
                    rx.text('Position: '),
                    rx.select(
                        rx.foreach(
                            PersonUpdateState.position_options,
                            lambda option: rx.option(
                                option,
                                value=option,
                            ),

                        ),
                        id='position',
                        default_value=position
                    ),
                    width='100%'
                ),
                rx.checkbox_group(
                    rx.switch(
                        'Teacher',
                        on_change=PersonUpdateState.teacher_on_change,
                        is_checked=teacher,
                        id='teacher',
                    ),
                    rx.switch(
                        'Active',
                        on_change=PersonUpdateState.active_on_change,
                        is_checked=active,
                        id='active',
                    ),
                ),
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.spacer(),
                            rx.checkbox(
                                'Minor',
                                is_checked=minor,
                                on_change=PersonUpdateState.minor_on_change,
                                id='minor',
                                size='lg'
                            )
                        ),
                        rx.vstack(
                            rx.text('Guardian: '),
                            rx.select(
                                rx.foreach(
                                    PersonUpdateState.guardian_options,
                                    lambda option: rx.option(
                                        option.label,
                                        value=option.value,
                                    ),

                                ),
                                defalut_value=guardian,
                                id='guardian'
                            ),
                        ),
                        align_items='end',
                        spacing='1em'
                    ),
                    padding='1em',
                    border_radius="15px",
                    border_color="blue",
                    border_width="thin",
                ),
                rx.button(
                    "Submit",
                    type_='submit',
                    color_scheme='blue'
                )
            ),
            on_submit=PersonUpdateState.handle_submit,
        )
    )