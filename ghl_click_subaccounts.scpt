tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 1
        -- Click on "Sub-Accounts" in the left sidebar
        click static text "Sub-Accounts" of group 1 of scroll area 1 of window 1
        delay 3
    end tell
end tell
