param (
    [string]$SessionToken,
    [int]$DayNumber
)

Invoke-WebRequest `
    -Uri "https://adventofcode.com/2025/day/$DayNumber/input" `
    -Headers @{ "Cookie" = "session=$SessionToken" } `
    -OutFile "input/$('{0:D2}' -f $DayNumber).txt"