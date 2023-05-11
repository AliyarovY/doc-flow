import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import (
    Depends,
    HTTPException,
    BackgroundTasks,
)
from sqlalchemy.orm import Session
from starlette import status

from doc_flow import models
from doc_flow import tables

from doc_flow.database import get_session
from doc_flow.settings import settings


class DocService:
    @classmethod
    def send_email(cls,
                   to: str,
                   title: str,
                   message: str,
                   ) -> None:
        msg = MIMEMultipart()
        msg['Subject'] = title
        msg['From'] = settings.smtp_login
        msg['To'] = to

        text = MIMEText(message)
        msg.attach(text)

        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(settings.smtp_login, settings.smtp_password)
            smtp.send_message(msg)

    @classmethod
    def send_email_for_admin(cls, to: str, doc: tables.Document):
        title = 'Document to be checked'
        message = f'{doc.name}\n{doc.content}'
        cls.send_email(to, title, message)

    @classmethod
    def send_email_for_sender(cls, to: str, doc_data: models.AdminCheckedDoc):
        title = f'Response to "{doc_data.name}" document verification'
        if doc_data.is_verified:
            message = 'Congratulations! Your document has passed inspection.'
        else:
            message = "I'm sorry, but your document didn't pass."
        cls.send_email(to, title, message)

    @classmethod
    def is_admin(cls, user: tables.User) -> bool:
        return user.is_superuser

    def __init__(
            self,
            background_tasks: BackgroundTasks,
            session: Session = Depends(get_session),
    ):
        self.session = session
        self.background_tasks = background_tasks

    def create_document(
            self,
            doc_data: models.CreateDoc,
            user: tables.User,
    ):
        doc = tables.Document(
            name=doc_data.name,
            content=doc_data.content,
            user_id=user.id,
            admin_id=doc_data.admin_id,
        )
        self.session.add(doc)
        self.session.commit()

        # validate
        admin = (
            self.session
            .query(tables.User)
            .filter(
                tables.User.id == doc_data.admin_id,
            )
            .first()
        )
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Not valid admin id',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        # send email
        self.background_tasks.add_task(
            self.send_email_for_admin,
            admin.email,
            doc,
        )

    def verify_document(
            self,
            doc_data: models.AdminCheckedDoc,
            user: tables.User,
    ):
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient rights to perform this action',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        if not self.is_admin(user):
            raise exception from None

        # send email
        self.background_tasks.add_task(
            self.send_email_for_admin,
            user.email,
            doc_data,
        )
