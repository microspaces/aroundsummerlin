tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Scroll down to make sure Around Summerlin is fully visible
        -- Then try clicking the "Switch to Sub-Account" link
        -- First scroll the main content area
        scroll down 3
        delay 1
        -- Try clicking at the right side of the Around Summerlin row
        -- The row appears to be lower now, around y=350-400
        click at {1200, 380}
        delay 5
    end tell
end tell
