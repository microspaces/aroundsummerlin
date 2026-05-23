tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Based on screenshot, "Around Summerlin" is in the sub-accounts list
        -- Try clicking at coordinates where it appears in the table
        -- The table is in the main content area, Around Summerlin is likely around y=250-300
        click at {500, 280}
        delay 5
    end tell
end tell
