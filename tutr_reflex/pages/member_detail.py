import reflex as rx
from tutr_reflex.state import PersonDetailState
from tutr_reflex.templates.template import template


@template(route="/members/[pid]", title="Member Detail", on_load=PersonDetailState.get_person)
def person_detail() -> rx.Component:

    return rx.cond(
        PersonDetailState.person is not None,
        rx.container(
            rx.vstack(
                rx.heading(PersonDetailState.person.sca_name),
                rx.divider(),
                rx.vstack(
                    rx.box(
                        rx.hstack(
                            rx.text('First Name: '),
                            rx.text(PersonDetailState.person.first_name)
                        )
                    ),
                    rx.box(
                        rx.hstack(
                            rx.text('Last Name: '),
                            rx.text(PersonDetailState.person.last_name)
                        )
                    ),
                    rx.box(
                        rx.hstack(
                            rx.text('Joined: '),
                            rx.text(PersonDetailState.person.joined_date)
                        )
                    ),
                    rx.box(
                        rx.hstack(
                            rx.text('Branch: '),
                            rx.text(PersonDetailState.branch)
                        )
                    ),
                    align_items='flex-start',

                ),
                rx.divider(),
                rx.divider(),
                rx.heading("Degrees"),
                rx.flex(
                    rx.data_table(
                        data=PersonDetailState.degrees_earned,
                        width='100%',

                    ), width='100%'
                ),
                rx.heading("Classes Taught"),
                rx.flex(
                    rx.data_table(
                        data=PersonDetailState.classes_taught,
                        width='100%',

                    ), width='100%'
                ),
                rx.divider(),
                rx.heading("Attendance History"),
                rx.flex(
                    rx.data_table(
                        data=PersonDetailState.attendance_history,
                        pagination=True,
                        width='100%',

                    ), width='100%'
                ),
                rx.link(rx.button('Edit Member', color_scheme='blue'),
                        href=f'/members/{PersonDetailState.person_id}/update')

            ),
            width='90%'

        ),
        rx.text("No person selected")
    )
