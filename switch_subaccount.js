// JavaScript to find and click "Switch to Sub-Account" for Around Summerlin
const elements = document.querySelectorAll('*');
let found = false;
for (let el of elements) {
    if (el.textContent && el.textContent.includes('Around Summerlin')) {
        console.log('Found Around Summerlin element:', el);
        // Look for the parent container and find the switch button
        let parent = el.closest('.subaccount-card, .location-item, [class*="card"], [class*="item"]');
        if (parent) {
            const switchBtn = parent.querySelector('a, button');
            if (switchBtn) {
                switchBtn.click();
                found = true;
                break;
            }
        }
    }
}
found ? 'Clicked switch button' : 'Around Summerlin not found';
