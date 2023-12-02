import reflex as rx
from tutr_reflex.templates.template import template
from tutr_reflex.state import EventListState, EventListObject


@template(route="/events", title="Event List")
def event_list() -> rx.Component:
    return rx.box(
        rx.box(
            rx.heading(
                "Filter by Event Name:",
                size="sm",
            ),
            rx.input(
                on_change=EventListState.input_filter_on_change,
                value=EventListState.filter_expr,
                debounce_timeout=1000,
            ),
        ),
        rx.box(
            render_table(),
        ),
    )


def render_row(row: EventListObject):
    return rx.tr(rx.td(row.event_name), rx.td(row.start_date), rx.td(row.end_date),
                 rx.td(row.branch), rx.td(rx.switch(is_checked=row.approved, is_disabled=True)),
                 rx.td(rx.link(rx.button('View'), href=f'/events/{row.id}', button=True))
                 )


def render_rows():
    return [
        rx.foreach(
            # use data filtered by `filter_expr` as update by rx.input
            EventListState.filtered_data,
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
                        for column in ["Event Name", "Start Date", "End Date", "Branch", "Approved", "Buttons"]
                    ]
                )
            ),
            rx.tbody(*render_rows()),
        )
    )