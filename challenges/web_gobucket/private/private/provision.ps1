$appDir = "C:\app"
$appExePath = "$appDir\server.exe"
$appZipPath = "c:\app.zip"

if (-not (Test-Path $appDir))
{
    $gwIP = (Get-NetRoute "0.0.0.0/0").NextHop

	# Download the app
	Invoke-WebRequest -OutFile $appZipPath -Uri "http://${gwIP}:8000/app.zip"
 
	# Unzip
	Expand-Archive -Path $appZipPath -DestinationPath $appDir
 
	# Cleanup
	Remove-Item $appZipPath
}
else
{
	Write-Host "App is already installed"
}