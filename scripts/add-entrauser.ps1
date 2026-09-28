param(
    [string] $SqlServerHostName,
    [string] $SqlDbName,
    [string] $ManagedIdentityName,
    [string] $DbRole
)

$token = azd auth token --scope https://database.windows.net/.default
Install-Module SqlServer -Force
Invoke-SqlCmd -HostName $SqlServerHostName -AccessToken $token -Database $SqlDbName -Query "CREATE USER [$ManagedIdentityName] FROM EXTERNAL PROVIDER; ALTER ROLE $DbRole ADD MEMBER [$ManagedIdentityName]"