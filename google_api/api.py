
import os
from google.auth.transport.requests import Request
from google.oauth2.challenges import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]

class FormFieldDoesntExistError(Exception):
    pass

class GoogleAPI:
    # Classe que obtém as credenciais para que seja realizada a conexão
    # com as APIs disponibilizadas pelo Google.

    def __init__(self):
        creds = None

        if os.path.exists("google_api/token.json"):
            creds = Credentials.from_authorized_user_file("google_api/token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "google_api/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=8081)

            with open("google_api/token.json", "w") as token:
                token.write(creds.to_json())

        if creds:
            self.creds = creds
        else:
            self.creds = None

    def get_formularios_inscricao(self):
        try:
            service = build("drive", "v3", credentials=self.creds)
            forms = []
            page_token = None
            while True:
                response = (service.files().list(
                    q="mimeType='application/vnd.google-apps.form'",
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                ).execute())

                for formulario in response.get('files', []):
                    if 'inscrição' in formulario['name'].lower(): 
                        forms.append(formulario)
                # forms.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            return forms

        except HttpError as error:
            print('error', error)

    def get_formulario_email_question_id(self, form_id):
        try:
            service = build("forms", "v1", credentials=self.creds)
            form = service.forms().get(formId=form_id).execute()

            email_question_id = None

            for item in form.get('items'):
                if 'e-mail' in item.get('title').lower():
                    email_question_id = item['questionItem']['question']['questionId']

            if not email_question_id:
                raise FormFieldDoesntExistError(
                    "Este formulário não possui dados de e-mail dos participantes."
                )

            return form, email_question_id
        except HttpError as error:
            print(f'{error}')

    def get_lista_email_alunos(self, form_id, email_qid):
        try:
            service = build("forms", "v1", credentials=self.creds)
            responses = service.forms().responses().list(formId=form_id).execute()
            responses = responses.get('responses')

            email_alunos = []
            for response in responses:
                answer = response['answers'][email_qid]
                email = answer['textAnswers']['answers'][0]['value']
                email = email.strip()

                email_alunos.append(email) 

            return email_alunos
        except HttpError as error:
            print('error', error)
