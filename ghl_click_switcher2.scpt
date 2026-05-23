tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Try clicking directly on the "Click here to switch" text
        -- Get all elements and find the one with that text
        set win to window 1
        set winElements to entire contents of win
        repeat with anElement in winElements
            try
                set elemName to name of anElement
                if elemName contains "Click here to switch" or elemName contains "switch" then
                    click anElement
                    delay 3
                    return "Clicked element: " & elemName
                end if
            on error
                -- skip
            end try
        end repeat
        return "Switch element not found by name, trying coordinates"
    end tell
end tell
