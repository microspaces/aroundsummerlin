tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Scroll down in the main content area to find Around Summerlin
        click at {800, 600}
        delay 0.5
        key code 125
        delay 0.5
        key code 125
        delay 0.5
        key code 125
        delay 1
    end tell
end tell
