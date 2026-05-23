tell application "HighLevel"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "HighLevel"
        -- Click on the "Around Summerlin" search result
        -- It's in the dropdown under "ALL ACCOUNTS"
        click at {350, 220}
        delay 5
    end tell
end tell
