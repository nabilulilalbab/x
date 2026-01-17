// Multi-Account Support Patch for Dashboard
// This file adds account_id parameter to all API calls

(function() {
    'use strict';
    
    // Store original functions
    const originalLoadDashboard = window.loadDashboard;
    const originalLoadStats = window.loadStats;
    const originalLoadGrowthChart = window.loadGrowthChart;
    const originalLoadActivityChart = window.loadActivityChart;
    const originalLoadRecentTweets = window.loadRecentTweets;
    const originalLoadKeywordPerformance = window.loadKeywordPerformance;
    const originalLoadActivityLog = window.loadActivityLog;
    const originalLoadConfigData = window.loadConfigData;
    const originalRunSlot = window.runSlot;
    const originalSaveSettings = window.saveSettings;
    const originalSaveTemplates = window.saveTemplates;
    
    // Helper function to add account_id to URL
    function addAccountId(url) {
        const accountId = window.currentAccountId || '';
        if (!accountId) return url;
        
        const separator = url.includes('?') ? '&' : '?';
        return `${url}${separator}account_id=${accountId}`;
    }
    
    // Patch loadDashboard
    window.loadDashboard = async function() {
        try {
            // Load functions that don't depend on charts first
            await Promise.all([
                window.loadStats(),
                window.loadBotStatus ? window.loadBotStatus() : Promise.resolve(),
                window.loadRecentTweets(),
                window.loadKeywordPerformance(),
                window.loadActivityLog()
            ]);
            
            // Load charts separately (they might not be initialized yet)
            if (window.charts) {
                await Promise.all([
                    window.loadGrowthChart(),
                    window.loadActivityChart()
                ]);
            }
            
            const lastUpdate = document.getElementById('last-update');
            if (lastUpdate) {
                lastUpdate.textContent = new Date().toLocaleString();
            }
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    };
    
    // Patch loadStats
    window.loadStats = async function() {
        const url = addAccountId('/api/stats');
        console.log('📊 Loading stats from:', url);
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            const stats = data.data;
            console.log('✅ Stats loaded. Account:', data.data.account_id || 'global');
            
            document.getElementById('stat-followers').textContent = stats.followers.current || 0;
            document.getElementById('stat-tweets').textContent = stats.today.tweets_posted || 0;
            
            const engagementRate = (stats.tweets.avg_engagement * 100).toFixed(2);
            document.getElementById('stat-engagement').textContent = engagementRate + '%';
            
            document.getElementById('stat-orders').textContent = stats.conversions.week.total_orders || 0;
        } else {
            console.error('❌ Failed to load stats');
        }
    };
    
    // Patch loadGrowthChart
    window.loadGrowthChart = async function() {
        const response = await fetch(addAccountId('/api/growth?days=30'));
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            const labels = data.data.map(d => new Date(d.date).toLocaleDateString());
            const followers = data.data.map(d => d.followers_count);
            
            // Check if charts exist
            if (window.charts && window.charts.growth) {
                window.charts.growth.data.labels = labels;
                window.charts.growth.data.datasets[0].data = followers;
                window.charts.growth.update();
            }
        }
    };
    
    // Patch loadActivityChart
    window.loadActivityChart = async function() {
        const response = await fetch(addAccountId('/api/activity/today'));
        const data = await response.json();
        
        if (data.success) {
            const activity = data.data;
            
            // Check if charts exist
            if (window.charts && window.charts.activity) {
                window.charts.activity.data.datasets[0].data = [
                    activity.tweets_posted || 0,
                    activity.likes_given || 0,
                    activity.replies_made || 0,
                    activity.follows_made || 0,
                    activity.retweets_made || 0
                ];
                window.charts.activity.update();
            }
        }
    };
    
    // Patch loadRecentTweets
    window.loadRecentTweets = async function() {
        const response = await fetch(addAccountId('/api/tweets/recent?limit=10'));
        const data = await response.json();
        
        if (data.success) {
            const container = document.getElementById('recent-tweets');
            
            if (data.data.length === 0) {
                container.innerHTML = '<p class="loading">No tweets yet</p>';
                return;
            }
            
            let html = '<table><thead><tr><th>Tweet</th><th>Type</th><th>Views</th><th>Likes</th><th>Engagement</th></tr></thead><tbody>';
            
            data.data.forEach(tweet => {
                const engagementRate = (tweet.engagement_rate * 100).toFixed(2);
                html += `
                    <tr>
                        <td>${tweet.tweet_text.substring(0, 50)}...</td>
                        <td>${tweet.tweet_type}</td>
                        <td>${tweet.views || 0}</td>
                        <td>${tweet.likes || 0}</td>
                        <td>${engagementRate}%</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            container.innerHTML = html;
        }
    };
    
    // Patch loadKeywordPerformance
    window.loadKeywordPerformance = async function() {
        const response = await fetch(addAccountId('/api/keywords?days=7'));
        const data = await response.json();
        
        if (data.success) {
            const container = document.getElementById('keyword-performance');
            
            if (data.data.length === 0) {
                container.innerHTML = '<p class="loading">No keyword data yet</p>';
                return;
            }
            
            let html = '<table><thead><tr><th>Keyword</th><th>Found</th><th>Engaged</th><th>Rate</th></tr></thead><tbody>';
            
            data.data.forEach(kw => {
                html += `
                    <tr>
                        <td>${kw.keyword}</td>
                        <td>${kw.total_found}</td>
                        <td>${kw.total_engaged}</td>
                        <td>${kw.engagement_rate || 0}%</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            container.innerHTML = html;
        }
    };
    
    // Patch loadActivityLog
    window.loadActivityLog = async function() {
        const response = await fetch(addAccountId('/api/logs?limit=20'));
        const data = await response.json();
        
        if (data.success) {
            const container = document.getElementById('activity-log');
            
            if (data.data.length === 0) {
                container.innerHTML = '<p class="loading">No activity logs yet</p>';
                return;
            }
            
            let html = '';
            
            data.data.forEach(log => {
                const className = log.success ? 'success' : 'error';
                const time = new Date(log.timestamp).toLocaleTimeString();
                const message = log.details || log.activity_type;
                
                html += `
                    <div class="log-entry ${className}">
                        <div class="log-time">${time}</div>
                        <div class="log-message">${message}</div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }
    };
    
    // Patch loadConfigData
    window.loadConfigData = async function() {
        try {
            const url = addAccountId('/api/config');
            console.log('📥 Loading config from:', url);
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.success) {
                window.configData = data.data;
                console.log('✅ Config loaded for account:', window.currentAccountId || 'global');
                console.log('   - Settings:', !!window.configData.settings);
                console.log('   - Templates:', !!window.configData.templates);
                console.log('   - Keywords:', !!window.configData.keywords);
                
                if (window.renderConfigSettings) window.renderConfigSettings();
                if (window.renderConfigTemplates) window.renderConfigTemplates();
                if (window.renderConfigKeywords) window.renderConfigKeywords();
            } else {
                console.error('❌ Failed to load config:', data.error);
            }
        } catch (error) {
            console.error('❌ Error loading config:', error);
        }
    };
    
    // Patch runSlot
    window.runSlot = async function(slot) {
        if (!confirm(`Run ${slot} slot now?`)) return;
        
        try {
            const accountId = window.currentAccountId || '';
            
            const response = await fetch('/api/bot/run-once', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    slot: slot,
                    account_id: accountId 
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert(`${slot} slot started! Check activity log.`);
                setTimeout(window.loadDashboard, 3000);
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error: ' + error);
        }
    };
    
    // Patch saveSettings
    const originalSaveSettingsFunc = window.saveSettings;
    window.saveSettings = async function() {
        try {
            const accountId = window.currentAccountId || '';
            
            // Call original logic to collect data
            window.configData.settings.business.product = document.getElementById('input-product-name').value;
            window.configData.settings.business.wa_number = document.getElementById('input-wa-number').value;
            window.configData.settings.business.wa_link = document.getElementById('input-wa-link').value;
            window.configData.settings.business.check_kuota_url = document.getElementById('input-check-url').value;
            
            const priceItems = document.querySelectorAll('.price-item');
            window.configData.settings.business.prices = [];
            
            priceItems.forEach((item, index) => {
                const priceData = {};
                
                const commonInputs = item.querySelectorAll('.price-field');
                commonInputs.forEach(input => {
                    const field = input.dataset.field;
                    let value = input.value;
                    
                    if (field === 'diskon') {
                        value = parseInt(value) || 0;
                    }
                    
                    priceData[field] = value;
                });
                
                priceData.harga = priceData.harga_display.replace(/[^0-9]/g, '');
                
                const extraContainer = item.querySelector('.extra-fields');
                if (extraContainer) {
                    const extraInputs = extraContainer.querySelectorAll('input[data-extra="value"]');
                    extraInputs.forEach(input => {
                        const field = input.dataset.field;
                        priceData[field] = input.value;
                    });
                }
                
                window.configData.settings.business.prices.push(priceData);
            });
            
            const url = addAccountId('/api/config/settings');
            
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(window.configData.settings)
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert('✅ Settings saved successfully!');
                await window.loadConfigData();
            } else {
                alert('❌ Error: ' + result.error);
            }
        } catch (error) {
            alert('❌ Error saving settings: ' + error);
        }
    };
    
    // Patch saveTemplates
    window.saveTemplates = async function() {
        try {
            const templateInputs = document.querySelectorAll('.template-item input[data-key]');
            
            templateInputs.forEach(input => {
                const key = input.dataset.key;
                const index = parseInt(input.dataset.index);
                
                if (key === 'promo_templates') {
                    const currentTemplate = window.configData.templates[key][index];
                    
                    if (typeof currentTemplate === 'object') {
                        const existingMedia = currentTemplate.media;
                        window.configData.templates[key][index] = {
                            text: input.value,
                            media: existingMedia || null
                        };
                    } else {
                        window.configData.templates[key][index] = {
                            text: input.value,
                            media: null
                        };
                    }
                } else {
                    window.configData.templates[key][index] = input.value;
                }
            });
            
            const url = addAccountId('/api/config/templates');
            
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(window.configData.templates)
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert('✅ Templates saved successfully!');
            } else {
                alert('❌ Error: ' + result.error);
            }
        } catch (error) {
            alert('❌ Error saving templates: ' + error);
        }
    };
    
    // Patch addTemplate
    const originalAddTemplate = window.addTemplate;
    window.addTemplate = function(type) {
        // Ensure configData exists and is loaded
        if (!window.configData || !window.configData.templates) {
            alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
            return;
        }
        
        const key = type === 'promo' ? 'promo_templates' : 'value_templates';
        
        if (!window.configData.templates[key]) {
            window.configData.templates[key] = [];
        }
        
        // Promo templates use object format, value templates use string format
        if (type === 'promo') {
            const defaultTemplate = {
                text: '🔥 KUOTA XL MURAH! 10GB cuma Rp25.000! Order: {wa_number}',
                media: null
            };
            window.configData.templates[key].push(defaultTemplate);
        } else {
            const defaultTemplate = '💡 Tips hemat kuota baru...';
            window.configData.templates[key].push(defaultTemplate);
        }
        
        if (window.renderConfigTemplates) {
            window.renderConfigTemplates();
        }
    };
    
    // Patch addTip
    const originalAddTip = window.addTip;
    window.addTip = function() {
        // Ensure configData exists and is loaded
        if (!window.configData || !window.configData.templates) {
            alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
            return;
        }
        
        if (!window.configData.templates.tips) {
            window.configData.templates.tips = [];
        }
        
        window.configData.templates.tips.push('Your tip here...');
        
        if (window.renderConfigTemplates) {
            window.renderConfigTemplates();
        }
    };
    
    // Patch addKeyword
    const originalAddKeyword = window.addKeyword;
    window.addKeyword = function(intent) {
        // Ensure configData exists and is loaded
        if (!window.configData || !window.configData.keywords) {
            alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
            return;
        }
        
        const key = intent + '_intent';
        
        if (!window.configData.keywords[key]) {
            window.configData.keywords[key] = [];
        }
        
        window.configData.keywords[key].push('new keyword');
        
        if (window.renderConfigKeywords) {
            window.renderConfigKeywords();
        }
    };
    
    // Patch addPrice
    const originalAddPrice = window.addPrice;
    window.addPrice = function() {
        // Ensure configData exists and is loaded
        if (!window.configData || !window.configData.settings || !window.configData.settings.business) {
            alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
            return;
        }
        
        if (!window.configData.settings.business.prices) {
            window.configData.settings.business.prices = [];
        }
        
        window.configData.settings.business.prices.push({
            paket: '10GB',
            harga: '25000',
            harga_display: 'Rp25.000',
            harga_normal: 'Rp45.000',
            diskon: 44
        });
        
        if (window.renderConfigSettings) {
            window.renderConfigSettings();
        }
    };
    
    console.log('✅ Multi-account patch loaded successfully!');
    console.log('   - window.currentAccountId:', window.currentAccountId);
    console.log('   - Patched functions: loadDashboard, loadStats, loadConfig, etc.');
    console.log('   - Helper: window.debugMultiAccount() for debug info');
})();
