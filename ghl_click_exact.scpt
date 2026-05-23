tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Based on the screenshot, the "Switch to Sub-Account" link is a blue button
        -- Try clicking more precisely on the button text area
        -- The Around Summerlin card is around y=400, button is on the right
        click at {1100, 420}
        delay 5
    end tell
end tell
