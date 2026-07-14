@description('The location used for all deployed resources')
param location string = resourceGroup().location

@description('Tags that will be applied to all resources')
param tags object = {}

param resName object = {}
param jsonServerExists bool
param pythonServerExists bool
param terraUpdateBatchExists bool
param sendEmailLogicAppUrl string
param jobNotificationsRecipients string

@description('Id of the user or app to assign application roles')
param principalId string

@description('Principal type of user or app')
param principalType string

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = uniqueString(subscription().id, resourceGroup().id, location)
var jobWorkloadProfile = 'worker-16GB'
var terraDbName = 'db-terra'
var sqlAdminUser = 'statlab'
var dbPasswordSecretName = 'db-password'
var storageAccountKeySecretName = 'cosmostoragekey'

// Monitor application with Azure Monitor
module monitoring 'br/public:avm/ptn/azd/monitoring:0.1.0' = {
  name: 'monitoring'
  params: {
    logAnalyticsName: resName.logAnalytics ?? '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: resName.applicationInsights ?? '${abbrs.insightsComponents}${resourceToken}'
    applicationInsightsDashboardName: resName.applicationInsightsDashboard ?? '${abbrs.portalDashboards}${resourceToken}'
    location: location
    tags: tags
  }
}
// Container registry
module containerRegistry 'br/public:avm/res/container-registry/registry:0.1.1' = {
  name: 'registry'
  params: {
    name: resName.acr ?? '${abbrs.containerRegistryRegistries}${resourceToken}'
    location: location
    tags: tags
    publicNetworkAccess: 'Enabled'
    roleAssignments:[
      {
        principalId: appsIdentity.outputs.principalId
        principalType: 'ServicePrincipal'
        roleDefinitionIdOrName: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
      }
    ]
  }
}

// Container apps environment
module containerAppsEnvironment 'br/public:avm/res/app/managed-environment:0.13.3' = {
  name: 'container-apps-environment'
  params: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsWorkspaceResourceId: monitoring.outputs.logAnalyticsWorkspaceResourceId
    }
    name: resName.containerAppsEnvironment ?? '${abbrs.appManagedEnvironments}${resourceToken}'
    location: location
    zoneRedundant: false
    workloadProfiles: [
      {
        minimumCount: 1
        maximumCount: 1
        workloadProfileType: 'D4'
        name: jobWorkloadProfile
      }
    ]
    storages: [
      {
        kind: 'SMB'
        name: 'tmp-data'
        accessMode: 'ReadWrite'
        storageAccountName: storageAccount.outputs.name
      }
    ]
  }
}

module appsIdentity 'br/public:avm/res/managed-identity/user-assigned-identity:0.2.1' = {
  name: 'appsidentity'
  params: {
    name: resName.userAssignedManagedIdentity ?? '${abbrs.managedIdentityUserAssignedIdentities}-${resourceToken}'
    location: location
  }
}

module jsonServerFetchLatestImage './modules/fetch-container-image.bicep' = {
  name: 'jsonServer-fetch-image'
  params: {
    exists: jsonServerExists
    name: 'ca-terra-jsonserver'
  }
}

module jsonServer 'br/public:avm/res/app/container-app:0.8.0' = {
  name: 'jsonServer'
  params: {
    name: 'ca-terra-jsonserver'
    ingressTargetPort: 5300
    scaleMinReplicas: 1
    scaleMaxReplicas: 10
    secrets: {
      secureList:  [
      ]
    }
    containers: [
      {
        image: jsonServerFetchLatestImage.outputs.?containers[?0].?image ?? 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
        name: 'main'
        resources: {
          cpu: json('0.5')
          memory: '1.0Gi'
        }
        env: [
          {
            name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
            value: monitoring.outputs.applicationInsightsConnectionString
          }
          {
            name: 'AZURE_CLIENT_ID'
            value: appsIdentity.outputs.clientId
          }
          {
            name: 'PORT'
            value: '5300'
          }
        ]
      }
    ]
    managedIdentities:{
      systemAssigned: false
      userAssignedResourceIds: [appsIdentity.outputs.resourceId]
    }
    registries:[
      {
        server: containerRegistry.outputs.loginServer
        identity: appsIdentity.outputs.resourceId
      }
    ]
    environmentResourceId: containerAppsEnvironment.outputs.resourceId
    location: location
    tags: union(tags, { 'azd-service-name': 'json-server' })
  }
}

module pythonServerFetchLatestImage './modules/fetch-container-image.bicep' = {
  name: 'pythonServer-fetch-image'
  params: {
    exists: pythonServerExists
    name: 'ca-terra-pythonserver'
  }
}

module pythonServer 'br/public:avm/res/app/container-app:0.8.0' = {
  name: 'pythonServer'
  params: {
    name: 'ca-terra-pythonserver'
    ingressTargetPort: 5500
    scaleMinReplicas: 1
    scaleMaxReplicas: 10
    secrets: {
      secureList:  [
      ]
    }
    containers: [
      {
        image: pythonServerFetchLatestImage.outputs.?containers[?0].?image ?? 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
        name: 'main'
        resources: {
          cpu: json('0.5')
          memory: '1.0Gi'
        }
        env: [
          {
            name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
            value: monitoring.outputs.applicationInsightsConnectionString
          }
          {
            name: 'AZURE_CLIENT_ID'
            value: appsIdentity.outputs.clientId
          }
          {
            name: 'PORT'
            value: '5500'
          }
        ]
      }
    ]
    managedIdentities:{
      systemAssigned: false
      userAssignedResourceIds: [appsIdentity.outputs.resourceId]
    }
    registries:[
      {
        server: containerRegistry.outputs.loginServer
        identity: appsIdentity.outputs.resourceId
      }
    ]
    environmentResourceId: containerAppsEnvironment.outputs.resourceId
    location: location
    tags: union(tags, { 'azd-service-name': 'python-server' })
  }
}

module storageAccount 'br/public:avm/res/storage/storage-account:0.32.0' = {
  name: 'terraJobStorage'
  params: {
    name: resName.storageAccount ?? '${abbrs.storageStorageAccounts}${resourceToken}'
    fileServices: {
      shares: [
        {
          name: 'tmp-data'
        }
      ]
    }
    secretsExportConfiguration: {
      keyVaultResourceId: keyVault.outputs.resourceId
      accessKey1Name: storageAccountKeySecretName
    }
  }

}

module sqlServer 'br/public:avm/res/sql/server:0.21.2' = {
  name: 'sqlServer'
  params: {
    name: resName.sqlServer ?? 'statlab'
    administratorLogin: sqlAdminUser
    databases: [
      {
        availabilityZone: -1
        name: terraDbName
        sku: {
          name: 'Standard'
          tier: 'Standard'
          capacity: 100
        }
      }
    ]
    secretsExportConfiguration: {
      keyVaultResourceId: keyVault.outputs.resourceId
      sqlAdminPasswordSecretName: dbPasswordSecretName
    }
  }
}

module keyVault 'br/public:avm/res/key-vault/vault:0.13.3' = {
  name: 'keyVault'
  params: {
    name: resName.keyVault ?? 'statlab-key-vault'
    roleAssignments: [
      {
        principalId: appsIdentity.outputs.principalId
        roleDefinitionIdOrName: 'Key Vault Secrets User'
      }
      {
        principalId: principalId
        principalType: principalType
        roleDefinitionIdOrName: 'Key Vault Administrator'
      }
    ]
  }
}

module terraUpdateBatchFetchLatestImage './modules/fetch-containerjob-image.bicep' = {
  name: 'terraUpdateBatch-fetch-image'
  params: {
    exists: terraUpdateBatchExists
    name: 'cj-terra-batch-data-update'
  }
}

module terraUpdateBatch 'br/public:avm/res/app/job:0.7.1' = {
  name: 'terraUpdateBatch'
  params: {
    replicaTimeout: 14400
    triggerType: 'Schedule'
    scheduleTriggerConfig: {
      cronExpression: '0 3 1 * *'
    }
    name: 'cj-terra-batch-data-update'
    workloadProfileName: jobWorkloadProfile
    volumes: [
      {
        name: 'tmp-storageaccount'
        storageType: 'AzureFile'
        storageName: 'tmp-data'
      }
    ]
    secrets: [
      {
        name: 'sa-key'
        keyVaultUrl: '${keyVault.outputs.uri}/secrets/${storageAccountKeySecretName}'
      }
      {
        name: 'db-password'
        keyVaultUrl: '${keyVault.outputs.uri}/secrets/${dbPasswordSecretName}'
      }
    ]
    containers: [
      {
        image: terraUpdateBatchFetchLatestImage.outputs.?containers[?0].?image ?? 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
        name: 'main'
        resources: {
          cpu: json('4.0')
          memory: '16.0Gi'
        }
        volumeMounts: [
          {
            volumeName: 'tmp-storageaccount'
            mountPath: '/tmpvolume'
          }
        ] 
        env: [
          {
            name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
            value: monitoring.outputs.applicationInsightsConnectionString
          }
          {
            name: 'AZURE_CLIENT_ID'
            value: appsIdentity.outputs.clientId
          }
          {
            name: 'WORKING_FOLDER'
            value: '/tmpvolume'
          }
          {
            name: 'STORAGE_ACCOUNT_NAME'
            value: storageAccount.outputs.name
          }
          {
            name: 'STORAGE_ACCOUNT_KEY'
            secretRef: 'sa-key'
          }
          {
            name: 'SIMULATE_ONLY'
            value: '0'
          }
          {
            name: 'LOGICAPP_URL'
            value: sendEmailLogicAppUrl
          }
          {
            name: 'MAIL_RECIPIENTS'
            value: jobNotificationsRecipients
          }
          {
            name: 'DOWNLOAD_TIME_INTERVAL_PRODUCT_M'
            value: '65'
          }
          {
            name: 'DOWNLOAD_TIME_INTERVAL_TRANSPORT_M'
            value: '60'
          }
          {
            name: 'RUN_DOWNLOAD'
            value: '1'
          }
          {
            name: 'RUN_ANNUAL_PROCESSING'
            value: '1'
          }
          {
            name: 'RUN_MONTHLY_PROCESSING'
            value: '1'
          }
          {
            name: 'SHARENAME_PREFIX'
            value: 'istat-cosmo-data-'
          }
          {
            name: 'RUN_OUTPUT'
            value: '1'
          }          
          {
            name: 'RUN_UTILS'
            value: '1'
          }
          {
            name: 'DUCKDB_LOCATION'
            value: '/tmpvolume/duckdb'
          }
          {
            name: 'DB_PROVIDER'
            value: 'mssql+pyodbc'
          } 
          {
            name: 'DB_SERVER'
            value: sqlServer.outputs.fullyQualifiedDomainName
          }
          {
            name: 'DB_NAME'
            value: terraDbName
          }
          {
            name: 'DB_DRIVER'
            value: 'ODBC Driver 18 for SQL Server'
          }
          {
            name: 'DB_USER'
            value: sqlAdminUser
          }
          {
            name: 'DB_PASS'
            secretRef: 'db-password'
          }
        ]
      }
    ]
    managedIdentities:{
      systemAssigned: false
      userAssignedResourceIds: [appsIdentity.outputs.resourceId]
    }
    registries:[
      {
        server: containerRegistry.outputs.loginServer
        identity: appsIdentity.outputs.resourceId
      }
    ]
    environmentResourceId: containerAppsEnvironment.outputs.resourceId
    location: location
    tags: union(tags, { 'azd-service-name': 'terra-update-batch' })
  }
}

module terraFrontend 'br/public:avm/res/web/static-site:0.9.5' = {
  name: 'terraFrontend'
  params: {
    name: resName.staticWebApp ?? 'xxxxxxxxxxxxxxxxxx'
    sku: 'Standard'
  }
}

output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.outputs.loginServer
output AZURE_RESOURCE_JSON_SERVER_ID string = jsonServer.outputs.resourceId
output AZURE_RESOURCE_PYTHON_SERVER_ID string = pythonServer.outputs.resourceId
output AZURE_RESOURCE_TERRA_FRONTEND_ID string = terraFrontend.outputs.resourceId
output AZURE_RESOURCE_TERRA_UPDATE_BATCH_ID string = terraUpdateBatch.outputs.resourceId
