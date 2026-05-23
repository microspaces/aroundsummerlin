tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on the "Switch to Sub-Account" link for Around Summerlin
        -- Based on screenshot, the link is at the bottom right of the Around Summerlin card
        -- The card starts around y=500, link is around y=600, x=1050
        click at {1050, 600}
        delay 5
    end tell
end tell
