from datetime import datetime
import reflex as rx
from tutr_reflex.state import ClassUpdateState

def event_form(
        event_name: str = '',
        start_date: datetime = datetime.now(),
        end_date: datetime = datetime.now(),
        tutr_surcharge: float = 0.0,
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
                    rx.text(),
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
                                rx.text("Street Number:"),
                                rx.input(
                                    id='street_number',
                                    default_value=apt_num
                                )
                            ),
                            
                        )
                    )
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