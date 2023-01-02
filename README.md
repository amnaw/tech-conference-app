# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Cost-effective architecture for web app and function
## _Architecture Explanation_

#### Azure Web App
For this particular project Azure web app is considered to be an easier approach to facilitate the migration process. 
Since there no special deployment, networking, governance and compliance requirements PaaS solution like web app is the first option.
Another good point to consider, Azure web app can easily integrate with other azure solutions like Azure Service Bus to queue the notifications, 
and Azure Postgres server.
In terms of costs, there are many payment options, the most common is consumption based.
The pricing tier of an App Service plan determines the App Service specifications and price.

#### Azure Function
Server less solution like Azure Function is the optimal choice in this scenario, since the application needs to run a background job to 
process asynchronous long-running workloads like sending emails.
Azure Functions allows you to focus only on the job logic, and maintain less infrastructure, you only need to integrate the function with needed Azure recourse
like Azure service bus and Postgres server.
with Azure Functions only pay for the used resources, there is no charges when the function is idle.
also the pricing models are flexible as you can use consumption plan or App Service plan.


## _Monthly Cost Analysis_
Note: the following price is estimated by [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/?&ef_id=CjwKCAiA-8SdBhBGEiwAWdgtcHI09_68WBYFrhGV_8MXt2zrbY_eGNgMinY6ozJSrn_8upQ08l4OQBoCYjIQAvD_BwE:G:s&OCID=AIDcmmk62dhxg3_SEM_CjwKCAiA-8SdBhBGEiwAWdgtcHI09_68WBYFrhGV_8MXt2zrbY_eGNgMinY6ozJSrn_8upQ08l4OQBoCYjIQAvD_BwE:G:s&gclid=CjwKCAiA-8SdBhBGEiwAWdgtcHI09_68WBYFrhGV_8MXt2zrbY_eGNgMinY6ozJSrn_8upQ08l4OQBoCYjIQAvD_BwE) based on many variables like region and execution times.  
| Azure Resource | Service Tier | Monthly Cost |
| ------ | ------ |------ |
| Azure Postgres Server | Basic 2 vCore | $49.64
| Azure Service Bus | Basic | $0.05 per million operations 
| Azure Web App | Basic | $12.41
| Azure Function | Consumption tier, Pay as you go, 128 MB memory | $0.20
| Azure Storage Account | Block Blob Storage, General Purpose V2, Hot Access Tier, Pay as you go | $20.80
|  |  | **Total**
|  |  | $83.10



