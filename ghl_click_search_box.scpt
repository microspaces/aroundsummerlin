tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click directly in the search input field
        click at {350, 260}
        delay 1
        -- Select all and type
        key code 126 using {command down}
        delay 0.5
        keystroke "Around Summerlin"
        delay 2
    end tell
end tell
