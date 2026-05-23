tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 1
        set win to window 1
        set winElements to entire contents of win
        set foundList to {}
        repeat with anElement in winElements
            try
                set elemName to name of anElement
                set elemRole to role description of anElement
                set end of foundList to "[" & elemRole & "] " & (elemName as string)
            on error
                -- skip
            end try
        end repeat
        return foundList
    end tell
end tell
