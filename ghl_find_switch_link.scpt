tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        set win to window 1
        set winElements to entire contents of win
        set foundList to {}
        repeat with anElement in winElements
            try
                set elemName to name of anElement
                set elemRole to role description of anElement
                if elemName is not missing value and (elemName contains "Switch" or elemName contains "Around Summerlin") then
                    set elemPos to position of anElement
                    set end of foundList to "[" & elemRole & "] " & elemName & " at " & (item 1 of elemPos) & "," & (item 2 of elemPos)
                end if
            on error
                -- skip
            end try
        end repeat
        return foundList
    end tell
end tell
