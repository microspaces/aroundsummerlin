tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 1
        -- Press F12 or Cmd+Option+I to close DevTools
        key code 111 using {command down, option down}
        delay 2
    end tell
end tell
