tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on the search box
        click at {350, 260}
        delay 1
    end tell
end tell
