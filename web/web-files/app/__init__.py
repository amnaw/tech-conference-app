import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from azure.servicebus import ServiceBusClient, ServiceBusMessage
# from azure.servicebus import QueueClient



app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.secret_key = app.config.get('SECRET_KEY')

# # create a Service Bus client using the connection string
# servicebus_client = ServiceBusClient.from_connection_string(app.config.get('SERVICE_BUS_CONNECTION_STRING'), logging_enable=True)
# with servicebus_client:
#     # get a Queue Sender object to send messages to the queue
#     queue_client = servicebus_client.get_queue_sender(queue_name=app.config.get('SERVICE_BUS_QUEUE_NAME'))


db = SQLAlchemy(app)

from . import routes