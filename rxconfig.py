import reflex as rx

config = rx.Config(
    app_name="tutr_reflex",
    frontend_port=3030,
    db_url='postgresql://postgres:postgres@localhost:5432/tutr-dev',
)