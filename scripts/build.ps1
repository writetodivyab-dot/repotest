Write-Host "=== Starting Windows PowerShell Build ==="
Write-Host "Compiling module A..."
Start-Sleep -Seconds 1
Write-Host "Compiling module B..."
Start-Sleep -Seconds 1

# Write a build log
@"
Compiling module A...
Compiling module B...
ERROR: unresolved symbol 'doWork' at src\moduleB.c:123
"@ | Out-File -FilePath build.log -Encoding utf8

Write-Error "Build failed: unresolved symbol 'doWork' at src\moduleB.c:123"

# Exit with non-zero code so Jenkins marks build as failed
exit 1
