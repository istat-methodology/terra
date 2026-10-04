param(
    [string] $SqlServerHostName,
    [string] $SqlDbName,
    [string] $ManagedIdentityName,
    [string] $DbRole
)

[AppContext]::SetSwitch(
    'Switch.Microsoft.Data.SqlClient.UseManagedNetworkingOnWindows',
    $true
)

if (-not (Get-Module -ListAvailable -Name SqlServer)) {
    Install-Module SqlServer -Force
}


$token = azd auth token --scope https://database.windows.net/.default

$maxAttempts = 5
$retryDelaySeconds = 20

for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
        $query = @"
IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = N'$ManagedIdentityName'
)
BEGIN
    CREATE USER [$ManagedIdentityName] FROM EXTERNAL PROVIDER;
END;

IF NOT EXISTS (
    SELECT 1
    FROM sys.database_role_members AS drm
    INNER JOIN sys.database_principals AS role
        ON role.principal_id = drm.role_principal_id
    INNER JOIN sys.database_principals AS member
        ON member.principal_id = drm.member_principal_id
    WHERE role.name = N'$DbRole'
      AND member.name = N'$ManagedIdentityName'
)
BEGIN
    ALTER ROLE [$DbRole] ADD MEMBER [$ManagedIdentityName];
END;
"@

        Invoke-SqlCmd -ServerInstance $SqlServerHostName -AccessToken $token -Database $SqlDbName -Query $query -ErrorAction Stop
        Write-Host "Successfully added user [$ManagedIdentityName] to role [$DbRole]."
        break
    }
    catch {
        if ($attempt -eq $maxAttempts) {
            throw
        }

        Write-Warning "Invoke-SqlCmd failed on attempt $attempt of $maxAttempts. Retrying in $retryDelaySeconds seconds."
        Start-Sleep -Seconds $retryDelaySeconds
    }
}
