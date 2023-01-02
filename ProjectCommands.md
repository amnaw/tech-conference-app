##### Application Workflow after the migration to Azure:
1- Web app send Notification to Service Bus queue
2- Function gets triggered when Bus recieve new message
3- Function processes the message which is the notification id
4- Function query the database using psycopg2 library for the given notification to retrieve the subject and message
5- Query the database to retrieve a list of attendees (email and first name)
6- Send email by SendGrid to all attendees
***
##### Part 1 : Create Azure Resources and Deploy Web App
1- Create Virtual Env:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
```
deactivate
```
2-  Add Variables.sh
```
chmod +x variables.sh
source variables.sh
```
3- Create a Resource group
```
az group create --location $region --name $resourceGroup
```
4-  Create an Azure Postgres Database single server
```
az postgres server create \
-n $PostgresServer \
--resource-group $resourceGroup \
--location $region  \
--admin-user $login  \
--admin-password $password  \
--sku-name $sku
```
From <https://learn.microsoft.com/en-us/azure/postgresql/single-server/quickstart-create-server-database-azure-cli>

5- Add a new database techconfdb
From postgres admin UI/CLI:
```
CREATE DATABASE $PostgresDBName;
```
Or
```
az postgres db create -g $resourceGroup -s $PostgresServer -n $PostgresDBName
```

6- Allow all IPs to connect to database server
```
az postgres server firewall-rule create --end-ip-address 255.255.255.255 \
                                        --name allow-all \
                                        --resource-group $resourceGroup \
                                        --server-name $PostgresServer \
                                        --start-ip-address 0.0.0.0
```
7- Restore the database with the backup located in the data folder
use can use ***pg_restore*** command, or simply
GO TO DB SERVER IN AZURE, COPY HOST AND USER LOG IN IN PGADMIN UI AND DO THE RESTORE FROM UI.

8-  Create a Service Bus resource with a notificationqueue that will be used to communicate between the web and the function.
Run the following command to create a Service Bus messaging namespace:
```
az servicebus namespace create --resource-group $resourceGroup --name $BusName --location $region
```
Run the following command to create a queue in the namespace you created in the previous step:
```
az servicebus queue create --resource-group $resourceGroup --namespace-name $BusName --name $QueueName
```
Run the following command to get the primary connection string for the namespace:
```
az servicebus namespace authorization-rule keys list --resource-group $resourceGroup   --namespace-name  $BusName --name RootManageSharedAccessKey --query primaryConnectionString --output tsv
```

9-  Open the web folder and update the following in the config.py file
• POSTGRES_URL 
• POSTGRES_USER
• POSTGRES_PW
• POSTGRES_DB
• SERVICE_BUS_CONNECTION_STRING

10- Create App Service plan
```
az appservice plan create \
--name $appServicePlan \
--resource-group $resourceGroup \               
--is-linux \
--location $region \
--sku F1
```
11- Create a storage account
```
az storage account create -n $storageAccountName -g  $resourceGroup -l $region --sku Standard_LRS
```

###### PLEASE, Before deploy TO AZURE, RUN THE WEB APP LOCALLY, HERE ARE SOME TIPS:
- MAKE SURE ALL PACKAGES IN REQUIREMENTS TXT 
- DO VIRTUAL ENV
- RUN :
``` 
pip install -r requirements.txt
```
- FIX DEPENDECIS AND CODE ISSUES
- ONCE CODE IS FINE ON LOCALHOST GO TO CLOUD


12- Deploy the web app:
- Go to vs code
- Update the configs config.py
- Create and deploy the app from azure
***
##### Part 2 : Create and Publish an Azure Function
Create Azure function of type service bus trigger, add the bus connection to the function settings, the database connection, then write the function logic.

***
##### Part 3 : Refactor routes.py and Update README
Refactor the post logic in web/app/routes.py -> notification() using servicebus queue_client:
The notification method on POST should save the notification object and queue the notification id for the function to pick it up
Re-deploy the web app to publish changes
https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
Very useful like to how send to Service Bus :
https://github.com/epomatti/azure-python-api-servicebus/blob/main/src/servicebus.py
***


