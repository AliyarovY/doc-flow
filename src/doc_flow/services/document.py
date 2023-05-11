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
from doc_flow.services import utils


class DocService:
    @classmethod
    def send_email(cls,
                   to: str,
                   title: str,
                   message: str,
                   ) -> None:
        try:
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
        except:
            pass

    @classmethod
    def send_email_for_admin(cls, to: str, doc: tables.Document):
        title = 'Document to be checked'
        message = f'id={doc.id}\n\n{doc.name}\n{doc.content}'
        cls.send_email(to, title, message)

    @classmethod
    def send_email_for_sender(
            cls,
            to: str,
            comment: str,
            doc: tables.Document
    ):
        title = f'Response to "{doc.name}" document verification'

        if doc.is_verified:
            message = 'Congratulations! Your document has passed inspection.'
        else:
            message = "I'm sorry, but your document didn't pass."

        if comment:
            message += f'\n\nComment from the administrator:\n{comment}'

        message += f'\n\nDocument id is {doc.id}'

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

        # validate
        admin = (
            self.session
            .query(tables.User)
            .filter(
                tables.User.id == doc_data.admin_id,
            )
            .first()
        )
        if not self.is_admin(admin):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Not valid admin id',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        # doc create
        doc = tables.Document(
            name=doc_data.name,
            content=doc_data.content,
            user_id=user.id,
            admin_id=doc_data.admin_id,
            is_verified=False,
        )
        self.session.add(doc)
        self.session.commit()

        # send email
        self.background_tasks.add_task(
            self.send_email_for_admin,
            admin.email,
            doc,
        )

        return self.get_response_doc_dict(doc)

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

        doc = utils.get_document(doc_data.id)
        doc.is_verified = doc_data.is_verified
        self.session.add(doc)
        self.session.commit()

        sender = (
            self.session
            .query(tables.User)
            .filter(
                tables.User.id == doc.user_id,
            )
            .first()
        )

        # send email
        self.background_tasks.add_task(
            self.send_email_for_sender,
            sender.email,
            doc_data.comment,
            doc,
        )

    def get_response_doc_dict(self, doc: tables.Document) -> models.Doc:
        user = (
            self.session
            .query(tables.User)
            .filter(
                tables.User.id == doc.user_id,
            )
            .first()
        )
        admin = (
            self.session
            .query(tables.User)
            .filter(
                tables.User.id == doc.admin_id,
            )
            .first()
        )

        return models.Doc(
            id=doc.id,
            name=doc.name,
            content=doc.content,
            is_verified=doc.is_verified,
            user=models.User.from_orm(user),
            admin=models.User.from_orm(admin),
        ).dict()
