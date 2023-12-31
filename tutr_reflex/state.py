"""Base state for the app."""

import reflex as rx
from tutr_reflex.db import Attendance, Branch, Class, ClassDesignation, db_Session, Event, PersonDegree, Person
from tutr_reflex.auth.auth_session import AuthSession, User
from datetime import datetime, timedelta, timezone
from sqlmodel import select
from typing import List
import pandas as pd

AUTH_TOKEN_LOCAL_STORAGE_KEY = "_auth_tokens"
DEFAULT_AUTH_SESSION_EXPIRATION_DELTA = timedelta(days=7)


class State(rx.State):
    """Base state for the app.

    The base state is used to store general vars used throughout the app.
    """

    # The auth_token is stored in local storage to persist across tab and browser sessions.
    auth_token: str = rx.LocalStorage(name=AUTH_TOKEN_LOCAL_STORAGE_KEY)

    @rx.cached_var
    def authenticated_user(self) -> User:
        """The currently authenticated user, or a dummy user if not authenticated.

        Returns:
            A User instance with id=-1 if not authenticated, or the User instance
            corresponding to the currently authenticated user.
        """
        with rx.session() as session:
            result = session.exec(
                select(User, AuthSession).where(
                    AuthSession.session_id == self.auth_token,
                    AuthSession.expiration
                    >= datetime.now(timezone.utc),
                    User.id == AuthSession.user_id,
                ),
            ).first()
            if result:
                user, session = result
                return user
        return User(id=-1)  # type: ignore

    @rx.cached_var
    def is_authenticated(self) -> bool:
        """Whether the current user is authenticated.

        Returns:
            True if the authenticated user has a positive user ID, False otherwise.
        """
        return self.authenticated_user.id >= 0

    def do_logout(self) -> None:
        """Destroy AuthSessions associated with the auth_token."""
        with rx.session() as session:
            for auth_session in session.exec(
                    AuthSession.select.where(AuthSession.session_id == self.auth_token)
            ).all():
                session.delete(auth_session)
            session.commit()
        self.auth_token = self.auth_token

    def _login(
            self,
            user_id: int,
            expiration_delta: timedelta = DEFAULT_AUTH_SESSION_EXPIRATION_DELTA,
    ) -> None:
        """Create an AuthSession for the given user_id.

        If the auth_token is already associated with an AuthSession, it will be
        logged out first.

        Args:
            user_id: The user ID to associate with the AuthSession.
            expiration_delta: The amount of time before the AuthSession expires.
        """
        if self.is_authenticated:
            self.do_logout()
        if user_id < 0:
            return
        self.auth_token = self.auth_token or self.get_token()
        with rx.session() as session:
            session.add(
                AuthSession(  # type: ignore
                    user_id=user_id,
                    session_id=self.auth_token,
                    expiration=datetime.now(timezone.utc)
                               + expiration_delta,
                )
            )
            session.commit()


class PersonListState(State):
    """State for the member list page."""

    filter_expr: str = ""

    @rx.var
    def people(self) -> List[Person]:
        with rx.session() as session:
            result = session.exec(Person.select.where()).all()
            return result

    @rx.cached_var
    def filtered_data(self) -> List[Person]:
        sca_name = self.filter_expr
        first_name = sca_name.split(' ')[0]

        with rx.session() as session:
            result = session.exec(Person.select.where(Person.sca_name.contains(self.filter_expr))).all()
            if not result:
                result = session.exec(Person.select.where(Person.first_name.contains(first_name))).all()
            return result

    def input_filter_on_change(self, value):
        self.filter_expr = value
        # for DEBUGGING
        yield rx.console_log(
            f"Filter set to: {self.filter_expr}"
        )


class PersonDetailState(State):
    """State for the member detail page."""
    person: Person | None = None
    branch: str = ""
    attendance_history: pd.DataFrame = pd.DataFrame()
    classes_taught: pd.DataFrame = pd.DataFrame()
    degrees_earned: pd.DataFrame = pd.DataFrame()

    @rx.var
    def person_id(self) -> str:
        return self.router.page.params.get('pid', 'no pid')

    def get_person(self):
        with rx.session() as session:
            self.person = session.exec(Person.select.where(Person.id == self.person_id)).one()
            self.branch = self.person.branch.branch_name
            attendance = [{
                'class_name': str(attendance.session.class_info.class_name),
                'date': attendance.session.class_info.events[0].start_date,
                'attended': str(attendance.attended),
                'passed': str(attendance.passed)
            } for attendance in self.person.attendance_history]
            self.attendance_history = pd.DataFrame(attendance, columns=['class_name', 'date', 'attended', 'passed'])
            classes = [{
                'class_name': str(class_taught.class_name),
                'times_taught': str(len(class_taught.events))
            } for class_taught in self.person.classes_taught]
            self.classes_taught = pd.DataFrame(classes, columns=['class_name', 'times_taught'])
            degrees = [
                {
                    'degree': person_degree.degree.degree_name,
                    'date': person_degree.date_achieved
                } for person_degree in self.person.degrees
            ]
            self.degrees_earned = pd.DataFrame(degrees, columns=['degree', 'date'])


class Option(rx.Base):
    label: str
    value: int


class PersonUpdate(rx.Base):
    sca_name: str
    first_name: str
    last_name: str
    joined_date: str
    active: bool
    position: str
    teacher: bool
    minor: bool
    branch: str
    guardian: str


class PersonUpdateState(PersonDetailState):
    """State for the member update page."""

    guardian: str = ''
    person_dict: PersonUpdate = PersonUpdate(
        sca_name='',
        first_name='',
        last_name='',
        joined_date=datetime.strftime(datetime.now(), '%m/%d/%Y'),
        active=True,
        position='Student',
        teacher=False,
        minor=False,
        branch='',
        guardian=''
    )

    def initialize(self):
        self.get_guardian()
        self.get_person_dict()

    def get_guardian(self):
        if self.person is None or not self.person.minor:
            return ''
        with rx.session() as session:
            guardian = session.exec(Person.select.where(Person.id == self.person.guardian_id)).all()[0]
            self.guardian = guardian.sca_name if guardian.sca_name else guardian.first_name + ' ' + guardian.last_name

    @rx.var
    def branch_options(self) -> List[Option]:
        with rx.session() as session:
            branches = session.exec(Branch.select.where()).all()
            return [Option(label=branch.branch_name, value=branch.id) for branch in branches]

    @rx.var
    def position_options(self) -> List[str]:
        with rx.session() as session:
            persons = session.exec(Person.select).all()
            return list(set([person.position for person in persons]))

    @rx.var
    def guardian_options(self) -> List[Option]:
        with rx.session() as session:
            guardians = session.exec(Person.select.where(Person.minor == False)).all()
            if not guardians:
                return [Option(label='None', value=None)]
            guardian_options = []
            for guardian in guardians:
                sca_name = guardian.sca_name
                first_name = guardian.first_name
                last_name = guardian.last_name
                if sca_name:
                    guardian_options.append(Option(label=sca_name, value=guardian.id))
                elif first_name and last_name:
                    guardian_options.append(Option(label=first_name + ' ' + last_name, value=guardian.id))
                else:
                    if first_name:
                        guardian_options.append(Option(label=first_name, value=guardian.id))
                    if last_name:
                        guardian_options.append(Option(label=last_name, value=guardian.id))
                    else:
                        guardian_options.append(Option(label='Unknown', value=guardian.id))
            return guardian_options

    def get_person_dict(self):
        if self.person is None:
            self.person_dict = PersonUpdate(
                sca_name='',
                first_name='',
                last_name='',
                joined_date=datetime.strftime(datetime.now(), '%m/%d/%Y'),
                active=True,
                position='Student',
                teacher=False,
                minor=False,
                branch='',
                guardian=''
            )
            return None
        self.person_dict = PersonUpdate(
            sca_name=self.person.sca_name if self.person.sca_name else '',
            first_name=self.person.first_name if self.person.first_name else '',
            last_name=self.person.last_name if self.person.last_name else '',
            joined_date=datetime.strftime(self.person.joined_date, '%m/%d/#Y') if
            self.person.joined_date else datetime.strftime(datetime.now(), '%m/%d/%Y'),
            active=self.person.active,
            position=self.person.position,
            teacher=self.person.teacher,
            minor=self.person.minor,
            branch=self.person.branch_id if self.person.branch_id else '',
            guardian=self.person.guardian_id if self.person.guardian_id else ''
        )

    def active_on_change(self, checked: bool):
        self.person_dict.active = checked
        print('pause')

    def teacher_on_change(self, checked: bool):
        self.person_dict.teacher = checked

    def minor_on_change(self, checked: bool):
        self.person_dict.minor = checked

    def handle_submit(self, form_data: dict):
        with rx.session() as session:
            self.person.sca_name = form_data['sca_name']
            self.person.first_name = form_data['first_name']
            self.person.last_name = form_data['last_name']
            self.person.joined_date = None
            self.person.active = form_data['active']
            self.person.position = form_data['position']
            self.person.teacher = form_data['teacher']
            self.person.branch_id = form_data['branch']
            if self.person.minor and not form_data['minor']:
                self.person.minor = form_data['minor']
                self.person.guardian_id = None
            else:
                self.person.minor = form_data['minor']
                self.person.guardian_id = form_data['guardian']
            session.commit()
            rx.redirect(f'/member/{self.person_id}')


class ClassListState(State):

    pass


class ClassDetailState(State):
    class_data: Class | None = None
    teacher: str = ''
    credits: float = 0.0

    @rx.var
    def class_id(self) -> str:
        return self.router.page.params.get('pid', 'no pid')

    def get_class(self):
        with rx.session() as session:
            self.class_data = session.exec(Class.select.where(Class.id == self.class_id)).one()
            self.teacher = self.class_data.teacher.sca_name
            self.credits = self.class_data.designation.credits


class ClassUpdate(rx.Base):
    class_name: str = '',
    class_length: str = "0.0",
    cost: str = "0.0",
    min_participants: str = "1",
    max_participants: str = "1",
    travel: bool = False,
    student_requirements: str = '',
    location_requirements: str = '',
    description: str = '',
    prerequisites: str = '',
    approved: bool = False,
    designation: str = '',
    person: str = ''


class ClassUpdateState(ClassDetailState):
    class_obj: ClassUpdate = ClassUpdate()

    @rx.var
    def class_designation_options(self) -> List[Option]:
        with rx.session() as session:
            designations = session.exec(ClassDesignation.select.where()).all()
            return [Option(label=designation.designation_name, value=designation.id) for designation in designations]

    @rx.var
    def teacher_options(self) -> List[Option]:
        """
        :return: list of Reflex Options for the teacher select box.

        Process Note:
        Before a Teacher can be included in the list they need to have and SCA Name listed in their profile.

        """
        with rx.session() as session:
            teachers = session.exec(Person.select.where(Person.teacher == True)).all()
            return [Option(label=teacher.sca_name, value=teacher.id) for teacher in teachers
                    if teacher.sca_name is not None]

    def get_class_obj(self):
        if self.person is None:
            self.class_obj = ClassUpdate()
            return None
        self.class_obj = ClassUpdate(
            class_name=self.class_data.class_name,
            class_length=str(self.class_data.class_length),
            cost=str(self.class_data.cost),
            min_participants=str(self.class_data.min_participants),
            max_participants=str(self.class_data.max_participants),
            travel=self.class_data.travel,
            student_requirements=self.class_data.student_requirements,
            location_requirements=self.class_data.location_requirements,
            description=self.class_data.description,
            prerequisites=self.class_data.prerequisites,
            approved=self.class_data.approved,
            designation=self.class_data.designation_id,
            person=self.class_data.person_id
        )

    def approved_on_change(self, checked: bool):
        self.class_obj.approved = checked

    def travel_on_change(self, checked: bool):
        self.class_obj.travel = checked

    def handle_submit(self, form_data: dict):
        pass


class EventListObject(rx.Base):
    id: int = 0
    event_name: str = ''
    start_date: str = ''
    end_date: str = ''
    approved: bool = False
    branch: str = ''


class EventListState(State):
    filter_expr: str = ""

    @rx.cached_var
    def filtered_data(self) -> List[EventListObject]:
        event_name = self.filter_expr

        with rx.session() as session:
            results: List[Event] = session.exec(Event.select.where(Event.event_name.contains(event_name)).order_by(Event.start_date)).all()
            result = [
                EventListObject(
                    id=event.id,
                    event_name=event.event_name,
                    start_date=event.start_date.strftime('%m/%d/%Y'),
                    end_date=event.end_date.strftime('%m/%d/%Y'),
                    approved=event.approved,
                    branch=event.branch.branch_name,
                ) for event in results
            ]
            return result

    def input_filter_on_change(self, value):
        self.filter_expr = value
        # for DEBUGGING
        yield rx.console_log(
            f"Filter set to: {self.filter_expr}"
        )

class EventClass(rx.Base):
    session_id: int = 0
    class_name: str = ''
    class_length: str = "0.0"
    cost: str = "0.0"
    teacher_id: int = 0
    teacher: str = ''


class EventDetailState(State):
    event_data: Event | None = None
    coordinator: str = ''
    branch: str = ''

    event_classes: List[db_Session] | None = None

    @rx.var
    def event_id(self) -> str:
        return self.router.page.params.get('pid', 'no pid')

    def get_event(self):
        with rx.session() as session:
            self.event_data = session.exec(Event.select.where(Event.id == self.event_id)).one()
            self.coordinator = self.event_data.coordinator.sca_name
            self.branch = self.event_data.branch.branch_name

    @rx.var
    def event_classes(self) -> List[EventClass]:
        if self.event_id == 'no pid':
            return []
        with rx.session() as session:
            event_classes = session.exec(db_Session.select.where(db_Session.event_id == self.event_id)).all()
            return [EventClass(
                session_id=event_class.id,
                class_name=event_class.class_info.class_name,
                class_length=str(event_class.class_info.class_length),
                cost=str(event_class.class_info.cost),
                teacher_id=event_class.class_info.person_id,
                teacher=event_class.class_info.teacher.sca_name if event_class.class_info.teacher.sca_name else
                event_class.class_info.teacher.first_name + ' ' + event_class.class_info.teacher.last_name
            ) for event_class in event_classes]



class EventUpdate(rx.Base):
    event_name: str = ''
    start_date: str = datetime.now().strftime('%m/%d/%Y')
    end_date: str = datetime.now().strftime('%m/%d/%Y')
    tutr_surcharge: str = "0.0"
    location_name: str = ''
    apt_num: str = ''
    street: str = ''
    city: str = ''
    postal_code: str = ''
    closed: bool = False
    approved: bool = False
    branch: str = ''
    tutr_coordinator: str = ''


class EventUpdateState(EventDetailState):
    event_obj: EventUpdate = EventUpdate()

    @rx.var
    def branch_options(self) -> List[Option]:
        with rx.session() as session:
            branches = session.exec(Branch.select.where()).all()
            return [Option(label=branch.branch_name, value=branch.id) for branch in branches]

    @rx.var
    def coordinator_options(self) -> List[Option]:
        with rx.session() as session:
            people = session.exec(Person.select.where(Person.sca_name is not None)).all()
            return [Option(label=person.sca_name, value=person.id) for person in people if person.sca_name is not None]

    def get_event_obj(self):
        if self.event is None:
            self.event_obj = EventUpdate()
            return None
        self.event_obj = EventUpdate(
            event_name=self.event_data.event_name,
            start_date=self.event_data.start_date,
            end_date=self.event_data.end_date,
            tutr_surcharge=self.event_data.tutr_surcharge,
            location_name=self.event_data.location_name,
            apt_num=self.event_data.apt_num,
            street=self.event_data.street,
            city=self.event_data.city,
            postal_code=self.event_data.postal_code,
            closed=self.event_data.closed,
            approved=self.event_data.approved,
            branch=self.event_data.branch_id,
            tutr_coordinator=self.event_data.tutr_coordinator_id
        )

    def approved_on_change(self, checked: bool):
        self.event_obj.approved = checked

    def closed_on_change(self, checked: bool):
        self.event_obj.closed = checked

    def handle_submit(self, form_data: dict):
        pass
