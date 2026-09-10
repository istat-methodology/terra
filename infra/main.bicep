targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

param jsonServerExists bool
param pythonServerExists bool
param terraUpdateBatchExists bool
param jobNotificationsRecipients string
param sendEmailLogicAppName string = 'LASendMailGmail'
param sendEmailLogicAppResourceGroup string = 'RG-Cosmo'
@secure()
param sqlAdminPassword string

@description('Id of the user or app to assign application roles')
param principalId string

@description('Principal type of user or app')
param principalType string

type resNamesType = {
  resourceGroup: string?
  logAnalytics: string?
  applicationInsights: string?
  applicationInsightsDashboard: string?
  acr: string?
  containerAppsEnvironment: string?
  userAssignedManagedIdentity: string?
  storageAccount: string?
  sqlServer: string?
  keyVault: string?
  staticWebApp: string?
}

// Tags that should be applied to all resources.
// 
// Note that 'azd-service-name' tags should be applied separately to service host resources.
// Example usage:
//   tags: union(tags, { 'azd-service-name': <service name in azure.yaml> })
var tags = {
  'azd-env-name': environmentName
}

param resName resNamesType = loadJsonContent('../.azure/.resnames.json')

module laUrl 'logicapp-sendmail.bicep' = {
  scope: resourceGroup(sendEmailLogicAppResourceGroup)
  params: {
    logicAppName: sendEmailLogicAppName
  }
}

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resName.?resourceGroup ?? 'rg-${environmentName}'
  location: location
  tags: tags
}

module resources 'resources.bicep' = {
  scope: rg
  name: 'resources'
  params: {
    location: location
    tags: tags
    principalId: principalId
    principalType: principalType
    jsonServerExists: jsonServerExists
    pythonServerExists: pythonServerExists
    terraUpdateBatchExists: terraUpdateBatchExists
    jobNotificationsRecipients: jobNotificationsRecipients
    sendEmailLogicAppUrl: laUrl.outputs.triggerUrl
    resName: resName
    sqlAdminPassword: sqlAdminPassword
  }
}
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = resources.outputs.AZURE_CONTAINER_REGISTRY_ENDPOINT
output AZURE_RESOURCE_JSON_SERVER_ID string = resources.outputs.AZURE_RESOURCE_JSON_SERVER_ID
output AZURE_RESOURCE_PYTHON_SERVER_ID string = resources.outputs.AZURE_RESOURCE_PYTHON_SERVER_ID
output AZURE_RESOURCE_TERRA_FRONTEND_ID string = resources.outputs.AZURE_RESOURCE_TERRA_FRONTEND_ID
output AZURE_RESOURCE_TERRA_UPDATE_BATCH_ID string = resources.outputs.AZURE_RESOURCE_TERRA_UPDATE_BATCH_ID
output AZURE_RESOURCE_GROUP string = rg.name
