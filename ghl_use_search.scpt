tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on search box and type "Around Summerlin"
        click at {400, 220}
        delay 1
        keystroke "Around Summerlin"
        delay 2
    end tell
end tell
