// Debug helper for multi-account
window.debugMultiAccount = function() {
    console.log('=== Multi-Account Debug Info ===');
    console.log('currentAccountId:', window.currentAccountId);
    console.log('configData:', window.configData);
    console.log('charts:', window.charts);
    console.log('================================');
};

// Log when account changes
const originalSwitchAccount = window.switchAccount;
if (originalSwitchAccount) {
    window.switchAccount = function(accountId) {
        console.log('Switching to account:', accountId);
        originalSwitchAccount(accountId);
        console.log('After switch, currentAccountId:', window.currentAccountId);
    };
}
