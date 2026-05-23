tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- The "Switch to Sub-Account" button for Around Summerlin
        -- It's on the right side of the card, try different y positions
        click at {1150, 400}
        delay 5
    end tell
end tell
