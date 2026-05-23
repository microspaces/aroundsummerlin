tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        set win to window 1
        set winElements to entire contents of win
        repeat with anElement in winElements
            try
                set elemName to name of anElement
                if elemName contains "Switch to Sub-Account" then
                    click anElement
                    delay 5
                    return "Clicked Switch to Sub-Account"
                end if
            on error
                -- skip
            end try
        end repeat
        return "Switch to Sub-Account not found by name, trying coordinates"
    end tell
end tell
