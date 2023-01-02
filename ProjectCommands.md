Application Workflow after the migration to Azure:
1- Web app send Notification to Service Bus queue
2- Function gets triggered when Bus recieve new message
3- Function processes the message which is the notification id
4- Function query the database using psycopg2 library for the given notification to retrieve the subject and message
5- Query the database to retrieve a list of attendees (email and first name)![image](https://user-images.githubusercontent.com/48104560/210189335-df06b88a-9554-4bc2-9f3c-fe0bc5120f39.png)
6- Send email by SendGrid to all attendees
