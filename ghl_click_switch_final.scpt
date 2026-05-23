tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on the "Switch to Sub-Account" link for Around Summerlin
        -- Based on screenshot, it's on the right side of the Around Summerlin card
        click at {1050, 500}
        delay 5
    end tell
end tell
