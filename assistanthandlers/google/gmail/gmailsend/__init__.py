"""
Send an email with Gmail

You must set 4 parameters:
 - "email" - the email address you want to send the email to
 - "subject"
 - "text"
 - "confirmation" - should be "yes" or else the email won't be sent
"""
from gmail import AssistantHandlerGmail

from utils import current_milli_time
import json
import base64
from email.mime.text import MIMEText

class AssistantHandlerGmailSend(AssistantHandlerGmail):
	def __init__(self):
		AssistantHandlerGmail.__init__(self,"gmailsend")    

	def	getEndpoint(self,parameters):
		return "users/me/messages/send"
	
	def getBaseUrl(self,parameters):
		return "https://content.googleapis.com/gmail/v1/"

	def getEndpointParameters(self,parameters):
		return None

	def getSpeech(self, parameters, data):	
		confirm = parameters.get("confirm")
		if confirm != "yes":
			return "Email not sent."	
		email = parameters.get("email")
		subject = parameters.get("subject")
		return "Email with subject \"" + subject + "\" sent to " + email

	def create_message(self, to, subject, message_text):
		message = MIMEText(message_text)
		message['to'] = to
		message['from'] = "me"
		message['subject'] = subject
		return {'raw': base64.urlsafe_b64encode(message.as_string())}
	
	def shouldCallUrl(self, parameters):
		confirm = parameters.get("confirm")
		if confirm != "yes":
			return False
		return True

	def getPostData(self,parameters):
		email = parameters.get("email")
		subject = parameters.get("subject")
		text = parameters.get("text")
		return self.create_message(email,subject,text)