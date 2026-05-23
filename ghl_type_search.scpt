tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Type "Around Summerlin" in the search box
        keystroke "Around Summerlin"
        delay 2
    end tell
end tell
