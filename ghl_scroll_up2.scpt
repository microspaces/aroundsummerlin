tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Scroll up to find Around Summerlin
        key code 126
        delay 0.5
        key code 126
        delay 0.5
        key code 126
        delay 1
    end tell
end tell
