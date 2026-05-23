tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 2
        -- Try to get UI elements recursively
        set winElements to entire contents of window 1
        set elementList to {}
        repeat with anElement in winElements
            try
                set elemName to name of anElement
                set elemRole to role description of anElement
                set elemValue to value of anElement
                if elemName is not missing value and elemName is not "" then
                    set end of elementList to "Role: " & elemRole & " | Name: " & elemName
                end if
            on error
                -- skip
            end try
        end repeat
        return elementList as string
    end tell
end tell
