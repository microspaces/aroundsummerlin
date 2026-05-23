tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Try clicking at various positions where the switcher might be
        -- Position 1: Directly on the globe icon area
        click at {60, 85}
        delay 2
    end tell
end tell
