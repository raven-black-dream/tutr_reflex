import reflex as rx

from tutr_reflex.state import State
from typing import List
from tutr_reflex.auth.auth_session import User
from tutr_reflex.templates.template import template

"""

Give the administrators the ability to approve and reject users,
as well as to change their roles.

"""

class UserManagementState(State):

    options: List[rx.option] = ['event_steward', 'dean', 'governor', 'registrar', 'user']
    role: str = ''

    @rx.var
    def users():
        with rx.session() as session:
            result = session.exec(User.select.where()).all()
        return result
    
    def toggle_access(user_id:int):
        with rx.session() as session:
            user = session.exec(User.select.where(User.id == user_id)).all()
            user.enabled = not user.enabled
            session.commit()

    def save_role(user_id:int, value:str):
        with rx.session() as session:
            user = session.exec(User.select.where(User.id == user_id)).all()
            user.role = not user.enabled
            session.commit()

    
@template(route='/user_management', title="User Management")
def user_management_page() -> rx.Component:
    return rx.box(
        rx.table_container(
            rx.table(
                rx.thead(
                    rx.tr(
                        [
                         rx.th(column)
                         for column in ['Username' , 'role', 'enabled', 'actions']
                        ]
                    )
                ),
                rx.tbody(
                    rx.foreach(
                        UserManagementState.users,
                        lambda user: rx.tr(
                            rx.td(user.username),
                            rx.td(rx.select(
                                UserManagementState.options,
                                default_value=user.role,
                                on_change=lambda c: UserManagementState.save_role(user.id, c)
                            )),
                            rx.td(user.enabled),
                            rx.td(rx.cond(
                                user.enabled,
                                rx.button("Revoke Access", on_click=lambda c: UserManagementState.toggle_access(user.id)),
                                rx.button("Grant Access", on_click=lambda c: UserManagementState.toggle_access(user.id))
                            ))
                        )
                    )
                )
            )
        )
    )