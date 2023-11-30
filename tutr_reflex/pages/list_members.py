import reflex as rx
from tutr_reflex.state import PersonListState
from tutr_reflex.templates.template import template
from tutr_reflex.db import Person
from typing import List


@template(route="/members", title="Members")
def person_list() -> rx.Component:
    return rx.box(
        rx.box(
            rx.heading(
                "Filter by tags:",
                size="sm",
            ),
            rx.input(
                on_change=PersonListState.input_filter_on_change,
                value=PersonListState.filter_expr,
                debounce_timeout=1000,
            ),
        ),
        rx.box(
            render_table(),
        ),
    )


def render_row(row: Person):
    return rx.tr(rx.td(row.sca_name), rx.td(row.first_name), rx.td(row.last_name), rx.td(
        rx.hstack(
            rx.link(rx.button('View'), href=f'/members/{row.id}', button=True),
        )
    ))


def render_rows():
    return [
        rx.foreach(
            # use data filtered by `filter_expr` as update by rx.input
            PersonListState.filtered_data,
            render_row,
        )
    ]


def render_table():
    return rx.table_container(
        rx.table(
            rx.thead(
                rx.tr(
                    *[
                        rx.th(column)
                        for column in ["SCA Name", "First Name", "Last Name", "Buttons"]
                    ]
                )
            ),
            rx.tbody(*render_rows()),
        )
    )