param (
    [string]$SessionToken,
    [int]$DayNumber
)

# Create the input directory if it doesn't exist
if (-not (Test-Path -Path "input")) {
    New-Item -ItemType Directory -Path "input" | Out-Null
}

Invoke-WebRequest `
    -Uri "https://adventofcode.com/2025/day/$DayNumber/input" `
    -Headers @{ "Cookie" = "session=$SessionToken" } `
    -OutFile "input/$('{0:D2}' -f $DayNumber).txt"