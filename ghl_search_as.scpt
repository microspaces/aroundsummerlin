tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on the search box and type "Around Summerlin"
        -- Search box is near top of main content, around y=150
        click at {600, 150}
        delay 1
        keystroke "Around Summerlin"
        delay 2
    end tell
end tell
