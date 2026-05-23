tell application "System Events"
    tell process "HighLevel"
        set frontmost to true
        delay 2
        -- Get all buttons in the main window
        set allButtons to every button of window 1
        set buttonList to {}
        repeat with aButton in allButtons
            try
                set btnName to name of aButton
                set btnTitle to title of aButton
                set end of buttonList to "Button: " & btnName & " | Title: " & btnTitle
            on error
                set end of buttonList to "Button: (unnamed)"
            end try
        end repeat
        return buttonList as string
    end tell
end tell
