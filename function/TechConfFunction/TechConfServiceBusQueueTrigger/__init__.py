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
        logging.info('********* Connection successfully done!')  


        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        cursor.execute("""SELECT message, subject FROM notification WHERE id = %s""",
          [notification_id])
        
        logging.info('********* notification :: Executing a SQL query')
       

        # TODO: Get notification message and subject from database using the notification_id
        # Fetch result
        record = cursor.fetchone()

        notification_message = ""
        notification_subject = ""

        notification_message = record[0]
        notification_subject = record[1]    

        logging.info('********* notification :: ')
        logging.info('notification_message: %s', notification_message)  
        logging.info('notification_subject: %s', notification_subject)  

        # TODO: Get attendees email and name
        cursor.execute("""
          SELECT * 
          FROM attendee;
          """)

        records = cursor.fetchall()
        logging.info('********* attendee :: Executing a SQL query')

        # TODO: Loop through each attendee and send an email with a personalized subject
        for record in records:
            notification_subject = 'Hi ' + record[1] + ' ' + record[2] + ', ' + notification_subject
            # TODO: sendGrid logic
            logging.info('********* send_email Started !')
            logging.info(notification_subject) 
            logging.info('********* email :: ') 
            logging.info(record[5])  
            send_email(record[5], notification_subject, notification_message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cursor.execute("""SELECT COUNT(*) FROM attendee""")
        count = cursor.fetchone()
        status = 'Notified ' + str(count[0]) + ' attendees'
        cursor.execute("""UPDATE notification SET completed_date = %s, status = %s WHERE id = %s""",
          (datetime.utcnow(), status, notification_id))
        connection.commit()
        
        logging.info('********* count :: ') 
        logging.info(status) 

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
        logging.info('********* sendgrid send started') 
        sg.send(message)
        logging.info('********* Message has been sent !') 

        