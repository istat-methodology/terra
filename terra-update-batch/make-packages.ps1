$Version = ((Get-Content .\prepare-node.sh | ?{ $_ -match '^# Version [0-9\.]+$' }) -split ' ')[2]
Compress-Archive -Update -Path .\prepare-node.sh -DestinationPath .\prepare-node_$Version.zip

$Version = ((Get-Content main.py | ?{ $_ -match '^# Version [0-9\.]+$' }) -split ' ')[2]
Compress-Archive -Update -Path *.py, modules, resources, execute, run.sh, requirements.txt -DestinationPath .\terraDataUpdate_$Version.zip

Write-Host "Operation completed."
