import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from urllib.parse import urlparse

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)  

    try:
        # TODO: Get connection to database
        conStr = os.environ.get('CONNECTION_STRING') 
        p = urlparse(conStr)
        
        # pg_connection_dict = {
        #       'dbname': p.hostname, 
        #       'user': p.username,
        #       'password': p.password,
        #       'port': p.port,
        #       'host': p.scheme
        #          } 

        # connection = psycopg2.connect(**pg_connection_dict)
        connection = psycopg2.connect(conStr)
        logging.info('********* connection successfully done!')  


        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Executing a SQL query
        cursor.execute("""
          SELECT * 
          FROM notification n
          WHERE n.id = %s;
          """,
          [notification_id,])

        # TODO: Get notification message and subject from database using the notification_id
        # Fetch result
        record = cursor.fetchone()
        while record is not None:
            notification_message = record['message']
            notification_subject = record['subject']    

        logging.info('********* notification :: ')
        logging.info('notification_message: %s', notification_message)  
        logging.info('notification_subject: %s', notification_subject)  

        # TODO: Get attendees email and name
        cursor.execute("""
          SELECT * 
          FROM attendee;
          """)

        records = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for record in records:
            notification_subject = 'Hi ' + record['first_name'] + ' ' + record['last_name'] + ', ' + notification_subject
            # TODO: sendGrid logic
            logging.info('********* send_email Started !')  
            send_email(record['email'], notification_subject, notification_message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified

    except (Exception, psycopg2.DatabaseError) as error:  
        logging.info('********* ERROR : ')  
        logging.error(error)
    finally:
        # TODO: Close connection
        if connection:
            cursor.close()
            connection.close()
            logging.info('WOW finally ~') 



def send_email(email, subject, body):
    if not os.environ.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email=os.environ.get('ADMIN_EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
        logging.info('********* Message has been sent !')  
        