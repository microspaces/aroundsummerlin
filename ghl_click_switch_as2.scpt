tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on the "Switch to Sub-Account" link for Around Summerlin
        -- Based on screenshot, the link is at the bottom right of the Around Summerlin card
        -- The card is around y=500-650, link is around y=620, x=1050
        click at {1050, 620}
        delay 5
    end tell
end tell
