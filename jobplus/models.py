from flask import url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

user_job = db.Table(
        'user_job',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE')),
        db.Column('job_id',db.Integer,db.ForeignKey('job.id',ondelete='CASCADE'))
        )

class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    real_name = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    work_years = db.Column(db.SmallInteger)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    resume = db.relationship('Resume',uselist=False)
    collect_jobs = db.relationship('Job',secondary=user_job)
    resume_url = db.Column(db.String(64))
    detail = db.relationship('CompanyDetail',uselist=False)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',uselist=False)
    job_experiences = db.relationship('JobExperience')
    edu_experiences = db.relationship('EduExperience')
    project_experiences = db.relationship('ProjectExperience')

    def profile(self):
        pass


class Experience(Base):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)

    description = db.Column(db.String(256))

class JobExperience(Experience):
    __tablename__ = 'job_experience'

    company = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32),nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

class EduExperience(Experience):
    __tablename__ = 'edu_experience'

    school = db.Column(db.String(32), nullable=False)
    specialty = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.String(32))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

class ProjectExperience(Experience):
    __tablename__ = 'project_experience'

    name = db.Column(db.String(32), nullable=False)
    role = db.Column(db.String(32))
    technologys = db.Column(db.String(64))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

