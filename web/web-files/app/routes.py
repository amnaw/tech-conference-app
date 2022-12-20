from app import app, db
from datetime import datetime
from app.models import Attendee, Conference, Notification
from flask import render_template, session, request, redirect, url_for, flash, make_response, session
from azure.servicebus import ServiceBusMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import logging

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        attendee = Attendee()
        attendee.first_name = request.form['first_name']
        attendee.last_name = request.form['last_name']
        attendee.email = request.form['email']
        attendee.job_position = request.form['job_position']
        attendee.company = request.form['company']
        attendee.city = request.form['city']
        attendee.state = request.form['state']
        attendee.interests = request.form['interest']
        attendee.comments = request.form['message']
        attendee.conference_id = app.config.get('CONFERENCE_ID')

        logging.error('------------1--------------')

        try:
            db.session.add(attendee)
            db.session.commit()
            logging.error('------------2--------------')
            session['message'] = 'Thank you, {} {}, for registering!'.format(attendee.first_name, attendee.last_name)
            logging.error('------------3--------------')
            return redirect('/Registration')
        except:
            logging.error('------------4--------------')
            logging.error('Error occured while saving your information')

    else:
        if 'message' in session:
            message = session['message']
            session.pop('message', None)
            return render_template('registration.html', message=message)
        else:
             return render_template('registration.html')

@app.route('/Attendees')
def attendees():
    attendees = Attendee.query.order_by(Attendee.submitted_date).all()
    return render_template('attendees.html', attendees=attendees)


@app.route('/Notifications')
def notifications():
    notifications = Notification.query.order_by(Notification.id).all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/Notification', methods=['POST', 'GET'])
def notification():
    if request.method == 'POST':
        notification = Notification()
        notification.message = request.form['message']
        notification.subject = request.form['subject']
        notification.status = 'Notifications submitted'
        notification.submitted_date = datetime.utcnow()

        try:
            ## save the notification object
            db.session.add(notification)
            db.session.commit()
            logging.error('************** commit to db *****************')

            ##################################################
            ## Queue the notification id,  for the Azure function to pick it up
            ## Call servicebus queue_client to enqueue notification ID
            #################################################
            logging.error('************** enqueue_notification(notification.id) *****************')
            logging.error('************** (notification.id) *****************')
            logging.error(notification.id)
            enqueue_notification(notification.id)
            #################################################

            return redirect('/Notifications')
        except :
            logging.error('log unable to save notification')

    else:
        return render_template('notification.html')


@app.route('/NotificationWithSENDGRID', methods=['POST', 'GET'])
def notificationSENDGRID():
    if request.method == 'POST':
        notification = Notification()
        notification.message = request.form['message']
        notification.subject = request.form['subject']
        notification.status = 'Notifications submitted'
        notification.submitted_date = datetime.utcnow()

        try:
            db.session.add(notification)
            db.session.commit()

            attendees = Attendee.query.all()

            for attendee in attendees:
                subject = '{}: {}'.format(attendee.first_name, notification.subject)
                send_email(attendee.email, subject, notification.message)

            notification.completed_date = datetime.utcnow()
            notification.status = 'Notified {} attendees'.format(len(attendees))
            db.session.commit()

            return redirect('/Notifications')
        except :
            logging.error('log unable to save notification')

    else:
        return render_template('notification.html')



def send_email(email, subject, body):
    if not app.config.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email=app.config.get('ADMIN_EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
        sg.send(message)


def enqueue_notification(message):
    logging.error('************** Start enqueue_notification *****************')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=app.config.get('SERVICE_BUS_CONNECTION_STRING'), logging_enable=True)
    with servicebus_client:
    # get a Queue Sender object to send messages to the queue
        sender = servicebus_client.get_queue_sender(queue_name=app.config.get('SERVICE_BUS_QUEUE_NAME'))
        with sender:                            
                # send one message        
                send_single_message(sender, message)
                logging.error('************** WOW *****************')




def send_single_message(sender, message):
    # create a Service Bus message
    message = ServiceBusMessage(str(message))
    # send the message to the queue
    sender.send_messages(message)
    logging.error('************** message sent **************')
  




