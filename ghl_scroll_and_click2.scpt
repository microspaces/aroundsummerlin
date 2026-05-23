tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Scroll down in the main content area
        key code 125
        delay 0.5
        key code 125
        delay 0.5
        key code 125
        delay 1
        -- Try clicking at the right side where "Switch to Sub-Account" link should be
        click at {1200, 380}
        delay 5
    end tell
end tell
