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
                    click anElement
                    delay 3
                    exit repeat
                end if
            on error
                -- skip
            end try
        end repeat
    end tell
end tell
