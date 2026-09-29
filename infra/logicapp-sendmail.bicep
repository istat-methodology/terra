param logicAppName string

resource la 'Microsoft.Logic/workflows@2019-05-01' existing = {
  name: logicAppName
}

var triggerName = first(items(la.properties!.definition!.triggers!))!.key

module triggerCallback 'logicapp-trigger-callback.bicep' = {
  name: 'logicapp-trigger-callback-${uniqueString(logicAppName)}'
  params: {
    logicAppName: logicAppName
    triggerName: triggerName
  }
}

@secure()
output triggerUrl string = triggerCallback.outputs.triggerUrl
