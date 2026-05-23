tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Try clicking directly on the "Around Summerlin" text in the table
        -- It's in the main content area, around the middle
        click at {400, 280}
        delay 5
    end tell
end tell
