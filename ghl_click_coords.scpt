tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 1
        -- Click at coordinates where Sub-Accounts appears in sidebar (left side, around y=200-250)
        -- Based on screenshot, sidebar is on left, Sub-Accounts is about 1/3 down
        click at {150, 300}
        delay 3
    end tell
end tell
