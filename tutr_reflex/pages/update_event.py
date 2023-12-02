import reflex as rx
from tutr_reflex.state import EventUpdateState
from tutr_reflex.templates.template import template
from tutr_reflex.components.event_form import event_form


@template(route="/events/[pid]/update", title="Update Event", on_load=EventUpdateState.get_event)
def update_event():
    return event_form(
        event_name=EventUpdateState.event_obj.event_name,
        start_date=EventUpdateState.event_obj.start_date,
        end_date=EventUpdateState.event_obj.end_date,
        tutr_surcharge=EventUpdateState.event_obj.tutr_surcharge,
        location_name=EventUpdateState.event_obj.location_name,
        apt_num=EventUpdateState.event_obj.apt_num,
        street=EventUpdateState.event_obj.street,
        city=EventUpdateState.event_obj.city,
        postal_code=EventUpdateState.event_obj.postal_code,
        closed=EventUpdateState.event_obj.closed,
        approved=EventUpdateState.event_obj.approved,
        branch=EventUpdateState.event_obj.branch,
        tutr_coordinator=EventUpdateState.event_obj.tutr_coordinator
    )

