#! /bin/sh
resourceGroup=TechConf-proj
########################################
# Variables for the Function App
# Must be unique worldwide
functionApp=amnafunctionapp1133
# Must be unique worldwide
storageAccount=TechConfStorageAccount1122
region=eastus
######################################## 
serverVersion='4.0'
########################################
# General purpose variables
# uniqueId=$RANDOM
########################################
# Must be unique worldwide
webApp='TechConfApp1122'
########################################
containerRegistry='amnacontainer112'
AKSCluster='amnaakscluster112'
imageName='amnaimage112'
imageTag='v1'
########################################
# Azure Postgres Database single server
PostgresServer='TechConfServer112'
login='amnaadmin'
password='myP@ssw0r89*'
sku="GP_Gen5_2"
PostgresDBName="techconfdb"
########################################
# Create a Service Bus resource
BusName='TechConfBus112'
QueueName='notificationqueue'
########################################
# Create an App Service Plan
appServicePlan='TechConfServicePlan112'
########################################
# Create a Storage Account 
storageAccountName='storageaccountaechconf'
########################################
# Print and verify
echo "=======Local Environment Variables======"
echo "functionApp = "$functionApp
echo "resourceGroup = "$resourceGroup
echo "storageAccount = "$storageAccount
echo "region = "$region
echo "cosmosDBAccountName = "$cosmosDBAccountName
echo "serverVersion = "$serverVersion
echo "databaseName = "$databaseName
echo "collectionName = "$collectionName
echo "webApp = "$webApp
echo "containerRegistry = "$containerRegistry
echo "AKSCluster = "$AKSCluster
echo "imageName = "$imageName
echo "imageTag = "$imageTag

echo "PostgresServer = "$PostgresServer
echo "PostgresDBName = "$PostgresDBName
echo "PostgresServerLogin = "$login
echo "PostgresServerPassword= "$password
echo "PostgresSKU= "$sku
echo "ServiceBusNameSpace  = "$BusName
echo "ServiceBusQueueName = "$QueueName
echo "AppServicePlanName = "$appServicePlan
echo "storageAccountName = "$storageAccountName
echo "=======End of Result======"