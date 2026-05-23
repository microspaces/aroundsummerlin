tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- The "Switch to Sub-Account" link for Around Summerlin is on the right side of the row
        -- Around Summerlin is the second row in the table
        -- Try clicking further to the right where the link should be
        click at {1200, 280}
        delay 5
    end tell
end tell
