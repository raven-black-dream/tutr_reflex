from datetime import date, time, datetime
import reflex as rx
from sqlmodel import Field,  Relationship
from sqlalchemy import Column, DateTime, Date, Time, func
from typing import Optional, List


class db_Session(rx.Model, table=True):
    __tablename__ = 'sessions'

    id: int = Field(primary_key=True)
    class_id: int = Field(foreign_key='classes.id')
    event_id: int = Field(foreign_key='events.id')
    start_time: Optional[time] = Field(
        sa_column=Column(
            'start_time',
            Time(timezone=True),
            server_default=func.now(),

        )
    )
    end_time: Optional[time] = Field(
        sa_column=Column(
            'end_time',
            Time(timezone=True),
            server_default=func.now(),

        )
    )
    roll_list: List['Attendance'] = Relationship(back_populates='session')
    class_info: 'Class' = Relationship(back_populates='sessions', sa_relationship_kwargs={'viewonly': True})



class Attendance(rx.Model, table=True):

    __tablename__ = 'attendance'

    id: int = Field(default=None, primary_key=True)
    attended: Optional[bool]
    passed: Optional[bool]
    person_id: int = Field(foreign_key='person.id')
    session_id: int = Field(foreign_key='sessions.id')

    person: "Person" = Relationship(back_populates='attendance_history')
    session: db_Session = Relationship(back_populates='roll_list', sa_relationship_kwargs={'viewonly': True})



class Branch(rx.Model, table=True):
    __tablename__ = 'branches'

    id: int = Field(primary_key=True)
    branch_name: str
    principality_id: int = Field(foreign_key='principalities.id')
    
    people: List['Person'] = Relationship(back_populates='branch')
    principality: "Principality" = Relationship(back_populates='branches')


class Class(rx.Model, table=True):
    __tablename__ = 'classes'

    id: int = Field(primary_key=True)
    class_name: str
    length: Optional[float]
    cost: float
    min_participants: int
    max_participants: int
    travel: bool
    # handouts: Optional[bytes}
    student_requirements: Optional[str]
    location_requirements: Optional[str]
    description: Optional[str]
    prerequisites: Optional[str]
    approved: bool
    designation_id: int = Field(foreign_key='class_designations.id')
    person_id: int = Field(foreign_key='person.id')

    events: List['Event'] = Relationship(back_populates='classes', link_model=db_Session)
    designation: 'ClassDesignation' = Relationship(back_populates='classes')
    sessions: db_Session = Relationship(back_populates='class_info', sa_relationship_kwargs={'viewonly': True})
    teacher: 'Person' = Relationship(back_populates='classes_taught')


class ClassDesignation(rx.Model, table=True):
    __tablename__ = 'class_designations'

    id: int = Field(primary_key=True)
    designation_name: str
    hours: float
    credits: int
    approved: bool
    major_id: int = Field(foreign_key='majors.id')

    classes: List['Class'] = Relationship(back_populates='designation')
    major: 'Major' = Relationship(back_populates='designations')


class Degree(rx.Model, table=True):
    __tablename__ = 'degrees'

    id: int = Field(primary_key=True)
    degree_name: str
    title: Optional[str]
    degree_type_id: int = Field(foreign_key='degree_types.id')

    degree_type: 'DegreeType' = Relationship(back_populates='degrees')
    majors: List['Major'] = Relationship(back_populates='degree')
    achievers: List['PersonDegree'] = Relationship(back_populates='degree')


class DegreeType(rx.Model, table=True):
    __tablename__ = 'degree_types'

    id: int = Field(primary_key=True)
    type_name: str
    core_credits: int
    extra_credits: int

    degrees: List['Degree'] = Relationship(back_populates='degree_type')


class Event(rx.Model, table=True):
    __tablename__ = 'events'

    id: int = Field(primary_key=True)
    event_name: str
    start_date: date = Field(
        sa_column=Column(
            'start_date',
            Date(),
            server_default=func.now(),

        )
    )
    end_date: date = Field(
        sa_column=Column(
            'end_date',
            Date(),
            server_default=func.now(),

        )
    )
    tutr_surcharge: float
    location_name: Optional[str]
    apt_num: Optional[str]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    closed: bool = Field(default=False)
    approved: bool = Field(default=False)
    branch_id: int = Field(foreign_key='branches.id')
    tutr_coordinator: Optional[int] = Field(foreign_key='person.id')

    coordinator: 'Person' = Relationship(back_populates='events_run')
    classes: List[Class] = Relationship(back_populates='events', link_model=db_Session)



class Major(rx.Model, table=True):
    __tablename__ = 'majors'
    id: int = Field(primary_key=True)
    major_name: str
    degree_id: int = Field(foreign_key='degrees.id')

    degree: Degree = Relationship(back_populates='majors')
    designations: List[ClassDesignation] = Relationship(back_populates='major')


class Person(rx.Model, table=True):
    __tablename__ = 'person'

    id: int = Field(primary_key=True)
    sca_name: Optional[str] = Field(default='')
    first_name: Optional[str] = Field(default='')
    last_name: Optional[str] = Field(default='')
    password: Optional[str] = Field(default=None)
    joined_date: Optional[datetime] = Field(
        sa_column=Column(
            'joined_date',
            DateTime(timezone=True),
            server_default=func.now(),

        )
    )
    active: bool
    position: Optional[str] = Field(default='Student')
    teacher: bool
    minor: bool
    branch_id: int = Field(foreign_key='branches.id')
    guardian_id: Optional[int] = Field(foreign_key='person.id')

    attendance_history: List['Attendance'] = Relationship(back_populates='person')
    classes_taught: List['Class'] = Relationship(back_populates='teacher')
    branch: Branch = Relationship(back_populates='people')
    degrees: List['PersonDegree'] = Relationship(back_populates='person')
    events_run: List['Event'] = Relationship(back_populates='coordinator')
    

class PersonDegree(rx.Model, table=True):
    __tablename__ = 'person_degrees'

    id: int = Field(primary_key=True)
    person_id: int = Field(foreign_key='person.id')
    degree_id: int = Field(foreign_key='degrees.id')
    date_achieved: date = Field(
        sa_column=Column(
            'date_achieved',
            Date(),
            server_default=func.now(),

        )
    )

    person: Person = Relationship(back_populates='degrees')
    degree: Degree = Relationship(back_populates='achievers')


class Principality(rx.Model, table=True):
    __tablename__ = 'principalities'

    id: int = Field(primary_key=True)
    principality_name: str

    branches: List['Branch'] = Relationship(back_populates='principality')

