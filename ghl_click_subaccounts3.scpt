tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 1
        -- Get the structure of window 1
        set win to window 1
        set winElements to entire contents of win
        -- Find and click "Sub-Accounts" text
        repeat with anElement in winElements
            try
                if name of anElement is "Sub-Accounts" then
                    set elemPos to position of anElement
                    set elemSize to size of anElement
                    return "Found Sub-Accounts at position " & (item 1 of elemPos) & "," & (item 2 of elemPos) & " size " & (item 1 of elemSize) & "x" & (item 2 of elemSize)
                end if
            on error
                -- skip
            end try
        end repeat
        return "Sub-Accounts not found"
    end tell
end tell
