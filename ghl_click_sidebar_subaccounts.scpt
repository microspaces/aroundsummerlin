tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on "Sub-Accounts" in the left sidebar
        -- It's around y=200 in the sidebar
        click at {80, 200}
        delay 3
    end tell
end tell
