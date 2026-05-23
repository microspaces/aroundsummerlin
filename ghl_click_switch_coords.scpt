tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Based on screenshot, "Switch to Sub-Account" link is to the right of "Around Summerlin"
        -- Around Summerlin is in the table, the switch link is on the right side of that row
        -- Try clicking at the right side of the Around Summerlin row
        click at {1100, 280}
        delay 5
    end tell
end tell
