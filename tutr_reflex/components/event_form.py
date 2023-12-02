from datetime import datetime
import reflex as rx
from tutr_reflex.state import EventUpdateState

def event_form(
        event_name: str = '',
        start_date: str = datetime.now().strftime('%m/%d/%Y'),
        end_date: str = datetime.now().strftime('%m/%d/%Y'),
        tutr_surcharge: str = "0.0",
        location_name: str = '',
        apt_num: str = '',
        street: str = '',
        city: str = '',
        postal_code: str = '',
        closed: bool = False,
        approved: bool = False,
        branch: str = '',
        tutr_coordinator: str = ''
):
    return rx.container(
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.text("Event Name: "),
                    rx.input(
                        id='event_name',
                        default_value=event_name
                    )
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("Address Information: "),
                        rx.hstack(
                            rx.hstack(
                                rx.text("Location Name:"),
                                rx.input(
                                    id='location_name',
                                    default_value=location_name
                                ),
                            ),
                        ),
                        rx.hstack(
                            rx.hstack(
                                rx.text("Apt Number:"),
                                rx.input(
                                    id='apt_number',
                                    default_value=apt_num
                                ),
                            ),
                            rx.hstack(
                                rx.text("Street:"),
                                rx.input(
                                    id='street',
                                    default_value=street
                                ),
                            ),
                            
                        ),
                        rx.hstack(
                            rx.hstack(
                                rx.text("City:"),
                                rx.input(
                                    id='city',
                                    default_value=city
                                ),
                            ),
                            rx.hstack(
                                rx.text("Postal Code:"),
                                rx.input(
                                    id='postal_code',
                                    default_value=postal_code
                                ),
                            ),
                        ),
                        rx.hstack(
                            rx.text('Branch:'),
                            rx.select(
                                rx.foreach(
                                    EventUpdateState.branch_options,
                                    lambda branch: rx.option(
                                        branch.label,
                                        value=branch.value,
                                    ),
                                    id='branch',
                                    default_value=branch
                                )
                            )
                        )
                    )
                ),

                rx.hstack(
                    rx.hstack(
                    rx.text("Start Date:"),
                    rx.date_picker(
                        id='start_date',
                        default_value=start_date
                    )
                    ),
                    rx.hstack(
                        rx.text("End Date:"),
                        rx.date_picker(
                            id='end_date',
                            default_value=end_date
                        )
                    )
                ),
                rx.hstack(
                    rx.text("Tutr Surcharge:"),
                    rx.input(
                        id='tutr_surcharge',
                        default_value=tutr_surcharge
                    )
                ),
                rx.hstack(
                    rx.text("Tutr Coordinator:"),
                    rx.select(
                        rx.foreach(
                            EventUpdateState.coordinator_options,
                            lambda person: rx.option(
                                person.label,
                                value=person.value,
                            ),
                            id='tutr_coordinator',
                            default_value=tutr_coordinator
                        )
                    )
                ),
                rx.checkbox_group(

                    rx.hstack(
                        rx.text("Registration Closed: "),
                        rx.switch(
                            id='closed',
                            on_change=EventUpdateState.closed_on_change,
                            is_checked=closed
                        )
                    ),
                    rx.hstack(
                        rx.text("Event Approved: "),
                        rx.switch(
                            id='approved',
                            on_change=EventUpdateState.approved_on_change,
                            is_checked=approved
                        )
                    )
                ),


                rx.button(
                    "Submit",
                    type_='submit',
                    color_scheme='blue'
                )
            ),
            on_submit=EventUpdateState.handle_submit,
        )
    )
