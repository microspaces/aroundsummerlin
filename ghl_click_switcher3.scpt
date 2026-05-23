tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Try different coordinates in the upper-left sidebar area
        -- The "Click here to switch" element is below the logo
        click at {100, 85}
        delay 3
    end tell
end tell
