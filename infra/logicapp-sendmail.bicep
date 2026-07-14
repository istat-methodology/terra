param logicAppName string

resource la 'Microsoft.Logic/workflows@2019-05-01' existing = {
  name: logicAppName
}

@secure()
output triggerUrl string = listCallbackURL('${la.id}/triggers/manual','2019-05-01').value
