param logicAppName string
param triggerName string

resource logicApp 'Microsoft.Logic/workflows@2019-05-01' existing = {
  name: logicAppName
}

@secure()
output triggerUrl string = listCallbackURL('${logicApp.id}/triggers/${triggerName}', '2019-05-01').value
