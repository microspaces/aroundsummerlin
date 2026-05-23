tell application "Google Chrome"
    tell active tab of window 1
        execute javascript "
            var elements = document.querySelectorAll('*');
            var found = false;
            for (var i = 0; i < elements.length; i++) {
                var el = elements[i];
                if (el.textContent && el.textContent.indexOf('Around Summerlin') !== -1) {
                    console.log('Found element');
                    var parent = el.closest('.subaccount-card, .location-item, [class*=\"card\"], [class*=\"item\"]');
                    if (parent) {
                        var switchBtn = parent.querySelector('a, button');
                        if (switchBtn) {
                            switchBtn.click();
                            found = true;
                            break;
                        }
                    }
                }
            }
            found ? 'Clicked' : 'Not found';
        "
    end tell
end tell
