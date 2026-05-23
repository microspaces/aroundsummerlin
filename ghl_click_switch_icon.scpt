tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on the icon next to "Switch to Sub-Account" for Around Summerlin
        -- The icon is to the left of the text, around x=1000, y=620
        click at {1000, 620}
        delay 5
    end tell
end tell
