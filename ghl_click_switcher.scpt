tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on "Click here to switch" in the sidebar (upper-left area, below logo)
        -- Based on screenshot analysis, this is around x=100, y=80-100
        click at {120, 90}
        delay 3
    end tell
end tell
