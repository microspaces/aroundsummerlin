tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 2
        return "HighLevel is now frontmost"
    end tell
end tell
