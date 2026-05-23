tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Press F12 to toggle DevTools off
        key code 111
        delay 2
    end tell
end tell
