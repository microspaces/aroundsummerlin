tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on "Sub-Accounts" in the left sidebar
        click at {100, 200}
        delay 3
    end tell
end tell
