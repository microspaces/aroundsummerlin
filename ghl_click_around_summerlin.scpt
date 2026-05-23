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
                if elemName contains "Around Summerlin" then
                    click anElement
                    delay 5
                    return "Clicked Around Summerlin"
                end if
            on error
                -- skip
            end try
        end repeat
        return "Around Summerlin not found by name"
    end tell
end tell
