param(
    [string] $SqlServerHostName,
    [string] $SqlDbName,
    [string] $SqlFileName
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
        Invoke-SqlCmd -InputFile $SqlFileName -ServerInstance $SqlServerHostName -AccessToken $token -Database $SqlDbName -ErrorAction Stop
        Write-Host "Successfully executed DDL script [$SqlFileName]."
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
