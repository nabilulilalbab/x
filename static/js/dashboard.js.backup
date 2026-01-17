// Twitter Bot Dashboard JavaScript

let charts = {};
let refreshInterval;

// Global config data
let configData = {
    settings: null,
    templates: null,
    keywords: null
};

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    loadDashboard();
    setupEventListeners();
    loadConfigData();
    
    // Auto-refresh every 30 seconds
    refreshInterval = setInterval(loadDashboard, 30000);
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('btn-start').addEventListener('click', startBot);
    document.getElementById('btn-stop').addEventListener('click', stopBot);
    document.getElementById('btn-refresh').addEventListener('click', loadDashboard);
    document.getElementById('conversion-form').addEventListener('submit', submitConversion);
}

// Load all dashboard data
async function loadDashboard() {
    try {
        await Promise.all([
            loadStats(),
            loadBotStatus(),
            loadGrowthChart(),
            loadActivityChart(),
            loadRecentTweets(),
            loadKeywordPerformance(),
            loadActivityLog()
        ]);
        
        document.getElementById('last-update').textContent = new Date().toLocaleString();
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Load statistics
async function loadStats() {
    const response = await fetch('/api/stats');
    const data = await response.json();
    
    if (data.success) {
        const stats = data.data;
        
        document.getElementById('stat-followers').textContent = stats.followers.current || 0;
        document.getElementById('stat-tweets').textContent = stats.today.tweets_posted || 0;
        
        const engagementRate = (stats.tweets.avg_engagement * 100).toFixed(2);
        document.getElementById('stat-engagement').textContent = engagementRate + '%';
        
        document.getElementById('stat-orders').textContent = stats.conversions.week.total_orders || 0;
    }
}

// Load bot status
async function loadBotStatus() {
    const response = await fetch('/api/bot/status');
    const data = await response.json();
    
    if (data.success) {
        const isRunning = data.data.is_running;
        const statusDot = document.getElementById('bot-status');
        const statusText = document.getElementById('bot-status-text');
        
        if (isRunning) {
            statusDot.className = 'running';
            statusText.textContent = 'Bot Running';
            document.getElementById('btn-start').disabled = true;
            document.getElementById('btn-stop').disabled = false;
        } else {
            statusDot.className = 'stopped';
            statusText.textContent = 'Bot Stopped';
            document.getElementById('btn-start').disabled = false;
            document.getElementById('btn-stop').disabled = true;
        }
    }
}

// Initialize charts
function initializeCharts() {
    // Growth chart
    const growthCtx = document.getElementById('chart-growth').getContext('2d');
    charts.growth = new Chart(growthCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Followers',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
    
    // Activity chart
    const activityCtx = document.getElementById('chart-activity').getContext('2d');
    charts.activity = new Chart(activityCtx, {
        type: 'bar',
        data: {
            labels: ['Tweets', 'Likes', 'Replies', 'Follows', 'Retweets'],
            datasets: [{
                label: 'Count',
                data: [0, 0, 0, 0, 0],
                backgroundColor: [
                    '#667eea',
                    '#10b981',
                    '#3b82f6',
                    '#f59e0b',
                    '#ef4444'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Load growth chart
async function loadGrowthChart() {
    const response = await fetch('/api/growth?days=30');
    const data = await response.json();
    
    if (data.success && data.data.length > 0) {
        const labels = data.data.map(d => new Date(d.date).toLocaleDateString());
        const followers = data.data.map(d => d.followers_count);
        
        charts.growth.data.labels = labels;
        charts.growth.data.datasets[0].data = followers;
        charts.growth.update();
    }
}

// Load activity chart
async function loadActivityChart() {
    const response = await fetch('/api/activity/today');
    const data = await response.json();
    
    if (data.success) {
        const activity = data.data;
        charts.activity.data.datasets[0].data = [
            activity.tweets_posted || 0,
            activity.likes_given || 0,
            activity.replies_made || 0,
            activity.follows_made || 0,
            activity.retweets_made || 0
        ];
        charts.activity.update();
    }
}

// Load recent tweets
async function loadRecentTweets() {
    const response = await fetch('/api/tweets/recent?limit=10');
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
}

// Load keyword performance
async function loadKeywordPerformance() {
    const response = await fetch('/api/keywords?days=7');
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
}

// Load activity log
async function loadActivityLog() {
    const response = await fetch('/api/logs?limit=20');
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
}

// Bot control functions
async function startBot() {
    if (!confirm('Start bot in scheduled mode?')) return;
    
    try {
        const response = await fetch('/api/bot/start', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            alert('Bot started!');
            await loadBotStatus();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error starting bot: ' + error);
    }
}

async function stopBot() {
    if (!confirm('Stop bot?')) return;
    
    try {
        const response = await fetch('/api/bot/stop', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            alert('Bot stopped!');
            await loadBotStatus();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error stopping bot: ' + error);
    }
}

async function runSlot(slot) {
    if (!confirm(`Run ${slot} slot now?`)) return;
    
    try {
        const response = await fetch('/api/bot/run-once', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ slot: slot })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`${slot} slot started! Check activity log.`);
            setTimeout(loadDashboard, 3000);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error);
    }
}

// Conversion modal
function showConversionModal() {
    document.getElementById('conversion-modal').style.display = 'block';
}

function closeConversionModal() {
    document.getElementById('conversion-modal').style.display = 'none';
}

async function submitConversion(e) {
    e.preventDefault();
    
    const data = {
        wa_messages: parseInt(document.getElementById('input-messages').value),
        orders: parseInt(document.getElementById('input-orders').value),
        revenue: parseInt(document.getElementById('input-revenue').value),
        notes: document.getElementById('input-notes').value
    };
    
    try {
        const response = await fetch('/api/conversion/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Conversion data saved!');
            closeConversionModal();
            document.getElementById('conversion-form').reset();
            await loadDashboard();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error);
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('conversion-modal');
    if (event.target == modal) {
        closeConversionModal();
    }
}

// ============= CONFIG EDITOR FUNCTIONS =============

async function loadConfigData() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        
        if (data.success) {
            configData = data.data;
            renderConfigSettings();
            renderConfigTemplates();
            renderConfigKeywords();
            // Media gallery will be loaded when user clicks Templates tab
        }
    } catch (error) {
        console.error('Error loading config:', error);
    }
}

function showConfigTab(tab) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.config-tab').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById('config-' + tab).classList.add('active');
}

// ===== Settings Tab =====

function renderConfigSettings() {
    if (!configData.settings) return;
    
    const business = configData.settings.business;
    
    // Fill inputs
    document.getElementById('input-product-name').value = business.product || '';
    document.getElementById('input-wa-number').value = business.wa_number || '';
    document.getElementById('input-wa-link').value = business.wa_link || '';
    document.getElementById('input-check-url').value = business.check_kuota_url || '';
    
    // Render prices with ALL fields (dynamic!)
    const pricesList = document.getElementById('prices-list');
    pricesList.innerHTML = '';
    
    (business.prices || []).forEach((price, index) => {
        const div = document.createElement('div');
        div.className = 'price-item';
        
        // Get all fields from price object (fully dynamic!)
        let fields = '';
        const commonFields = ['paket', 'harga_display', 'harga_normal', 'diskon'];
        
        // Render common fields first
        commonFields.forEach(field => {
            const value = price[field] || '';
            const placeholder = field.replace('_', ' ');
            fields += `<input type="text" placeholder="${placeholder}" value="${value}" data-index="${index}" data-field="${field}" class="price-field">`;
        });
        
        // Add extra fields button
        div.innerHTML = `
            <div style="display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap;">
                ${fields}
                <button class="btn-delete" onclick="deletePrice(${index})">❌</button>
            </div>
            <div class="extra-fields" id="extra-fields-${index}"></div>
            <button class="btn btn-secondary btn-sm" onclick="showExtraFields(${index})">+ Add Extra Field (kuota_area1, dll)</button>
        `;
        pricesList.appendChild(div);
        
        // Render extra fields if exist
        const extraFields = Object.keys(price).filter(k => !commonFields.includes(k) && k !== 'harga');
        if (extraFields.length > 0) {
            renderExtraFields(index, price, extraFields);
        }
    });
}

function renderExtraFields(priceIndex, priceData, fields) {
    const container = document.getElementById(`extra-fields-${priceIndex}`);
    if (!container) return;
    
    let html = '<div style="padding: 10px; background: #f9fafb; border-radius: 5px; margin-top: 5px;">';
    html += '<small><strong>Extra Fields:</strong></small><br>';
    
    fields.forEach(field => {
        const value = priceData[field] || '';
        html += `
            <div style="margin: 5px 0;">
                <input type="text" placeholder="Field name" value="${field}" data-index="${priceIndex}" data-extra="name" style="width: 150px;">
                <input type="text" placeholder="Value" value="${value}" data-index="${priceIndex}" data-extra="value" data-field="${field}" style="width: 200px;">
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function showExtraFields(index) {
    const fieldName = prompt('Field name (e.g., kuota_area1, kuota_area2):');
    if (!fieldName) return;
    
    const fieldValue = prompt('Field value (e.g., 65 GB, 123 GB):');
    if (!fieldValue) return;
    
    // Add to configData
    if (!configData.settings.business.prices[index]) return;
    configData.settings.business.prices[index][fieldName] = fieldValue;
    
    // Re-render
    renderConfigSettings();
}

function addPrice() {
    if (!configData.settings.business.prices) {
        configData.settings.business.prices = [];
    }
    
    configData.settings.business.prices.push({
        paket: '10GB',
        harga: '25000',
        harga_display: 'Rp25.000',
        harga_normal: 'Rp45.000',
        diskon: 44
    });
    
    renderConfigSettings();
}

function deletePrice(index) {
    if (confirm('Delete this price?')) {
        configData.settings.business.prices.splice(index, 1);
        renderConfigSettings();
    }
}

async function saveSettings() {
    try {
        // Collect ALL data from inputs (FULLY DYNAMIC!)
        configData.settings.business.product = document.getElementById('input-product-name').value;
        configData.settings.business.wa_number = document.getElementById('input-wa-number').value;
        configData.settings.business.wa_link = document.getElementById('input-wa-link').value;
        configData.settings.business.check_kuota_url = document.getElementById('input-check-url').value;
        
        // Collect prices with ALL fields (FULLY DYNAMIC!)
        const priceItems = document.querySelectorAll('.price-item');
        configData.settings.business.prices = [];
        
        priceItems.forEach((item, index) => {
            const priceData = {};
            
            // Get common fields
            const commonInputs = item.querySelectorAll('.price-field');
            commonInputs.forEach(input => {
                const field = input.dataset.field;
                let value = input.value;
                
                // Convert diskon to number
                if (field === 'diskon') {
                    value = parseInt(value) || 0;
                }
                
                priceData[field] = value;
            });
            
            // Add harga (numeric only)
            priceData.harga = priceData.harga_display.replace(/[^0-9]/g, '');
            
            // Get extra fields (kuota_area1, dll)
            const extraContainer = item.querySelector('.extra-fields');
            if (extraContainer) {
                const extraInputs = extraContainer.querySelectorAll('input[data-extra="value"]');
                extraInputs.forEach(input => {
                    const field = input.dataset.field;
                    priceData[field] = input.value;
                });
            }
            
            configData.settings.business.prices.push(priceData);
        });
        
        // Save to backend
        const response = await fetch('/api/config/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(configData.settings)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ Settings saved successfully!\n\nAll fields saved dynamically - no hardcode!');
            await loadConfigData(); // Reload to confirm
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error saving settings: ' + error);
    }
}

// Note: Media upload for Settings tab removed
// All media management now in Templates Tab > Media Manager

// ===== Templates Tab =====

let selectedMediaForTemplate = null;
let currentEditingTemplateIndex = null;

function renderConfigTemplates() {
    if (!configData.templates) return;
    
    // Promo templates
    renderPromoTemplateList('promo-templates-list', configData.templates.promo_templates || []);
    
    // Value templates
    renderTemplateList('value-templates-list', configData.templates.value_templates || [], 'value_templates');
    
    // Tips
    renderTipsList('tips-list', configData.templates.tips || []);
}

function renderPromoTemplateList(containerId, templates) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    templates.forEach((template, index) => {
        const div = document.createElement('div');
        div.className = 'template-item';
        
        // Handle both string and object formats - extract text only
        const templateText = typeof template === 'object' ? template.text : template;
        
        // Simple render - text input + delete button only
        div.innerHTML = `
            <input type="text" value="${escapeHtml(templateText)}" data-key="promo_templates" data-index="${index}" style="flex: 1;">
            <button class="btn-delete" onclick="deleteTemplate('promo_templates', ${index})">❌</button>
        `;
        
        container.appendChild(div);
    });
}

function renderTemplateList(containerId, templates, key) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    templates.forEach((template, index) => {
        const div = document.createElement('div');
        div.className = 'template-item';
        
        // Handle both string and object formats
        const templateText = typeof template === 'object' ? template.text : template;
        const templateMedia = typeof template === 'object' ? template.media : null;
        
        div.innerHTML = `
            <input type="text" value="${escapeHtml(templateText)}" data-key="${key}" data-index="${index}">
            ${templateMedia ? `<span class="media-indicator">📎 ${templateMedia}</span>` : ''}
            <button class="btn-delete" onclick="deleteTemplate('${key}', ${index})">❌</button>
        `;
        container.appendChild(div);
    });
}

function renderTipsList(containerId, tips) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    tips.forEach((tip, index) => {
        const div = document.createElement('div');
        div.className = 'template-item';
        div.innerHTML = `
            <input type="text" value="${tip}" data-key="tips" data-index="${index}">
            <button class="btn-delete" onclick="deleteTip(${index})">❌</button>
        `;
        container.appendChild(div);
    });
}

function addTemplate(type) {
    const key = type === 'promo' ? 'promo_templates' : 'value_templates';
    
    if (!configData.templates[key]) {
        configData.templates[key] = [];
    }
    
    // Promo templates use object format, value templates use string format
    if (type === 'promo') {
        const defaultTemplate = {
            text: '🔥 KUOTA XL MURAH! 10GB cuma Rp25.000! Order: {wa_number}',
            media: null
        };
        configData.templates[key].push(defaultTemplate);
    } else {
        const defaultTemplate = '💡 Tips hemat kuota baru...';
        configData.templates[key].push(defaultTemplate);
    }
    
    renderConfigTemplates();
}

function addTip() {
    if (!configData.templates.tips) {
        configData.templates.tips = [];
    }
    
    configData.templates.tips.push('Your tip here...');
    renderConfigTemplates();
}

function deleteTemplate(key, index) {
    if (confirm('Delete this template?')) {
        configData.templates[key].splice(index, 1);
        renderConfigTemplates();
    }
}

function deleteTip(index) {
    if (confirm('Delete this tip?')) {
        configData.templates.tips.splice(index, 1);
        renderConfigTemplates();
    }
}

async function previewTweet() {
    const template = document.getElementById('preview-input').value;
    
    if (!template) {
        alert('Enter a template first!');
        return;
    }
    
    const output = document.getElementById('preview-output');
    output.innerHTML = '<p style="color: #666;">Generating preview...</p>';
    
    try {
        const response = await fetch('/api/preview-tweet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ template: template, use_ai: true })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const data = result.data;
            output.className = 'success';
            output.innerHTML = `
                <strong>Original:</strong><br>
                <p style="margin: 5px 0 15px 0;">${data.original}</p>
                <strong>AI Generated:</strong><br>
                <p style="margin: 5px 0;">${data.generated}</p>
                <div class="preview-meta">
                    Length: ${data.length}/280 characters
                    ${data.length > 280 ? ' ⚠️ Too long!' : ' ✅'}
                </div>
            `;
        } else {
            output.innerHTML = `<p style="color: #ef4444;">Error: ${result.error}</p>`;
        }
    } catch (error) {
        output.innerHTML = `<p style="color: #ef4444;">Error: ${error}</p>`;
    }
}

async function saveTemplates() {
    try {
        // Collect data from inputs
        const templateInputs = document.querySelectorAll('.template-item input[data-key]');
        
        templateInputs.forEach(input => {
            const key = input.dataset.key;
            const index = parseInt(input.dataset.index);
            
            // For promo_templates, preserve object structure (for future media support)
            if (key === 'promo_templates') {
                const currentTemplate = configData.templates[key][index];
                
                if (typeof currentTemplate === 'object') {
                    // Preserve existing media value (if any)
                    const existingMedia = currentTemplate.media;
                    configData.templates[key][index] = {
                        text: input.value,
                        media: existingMedia || null
                    };
                } else {
                    // Convert string to object format
                    configData.templates[key][index] = {
                        text: input.value,
                        media: null
                    };
                }
            } else {
                // For other templates (value_templates, tips), keep as string
                configData.templates[key][index] = input.value;
            }
        });
        
        // Save to backend
        const response = await fetch('/api/config/templates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(configData.templates)
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
}

// ===== Keywords Tab =====

function renderConfigKeywords() {
    if (!configData.keywords) return;
    
    renderKeywordList('high-keywords-list', configData.keywords.high_intent || [], 'high_intent');
    renderKeywordList('medium-keywords-list', configData.keywords.medium_intent || [], 'medium_intent');
    renderKeywordList('low-keywords-list', configData.keywords.low_intent || [], 'low_intent');
}

function renderKeywordList(containerId, keywords, key) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    keywords.forEach((keyword, index) => {
        const div = document.createElement('div');
        div.className = 'keyword-item';
        div.innerHTML = `
            <input type="text" value="${keyword}" data-key="${key}" data-index="${index}">
            <button class="btn-delete" onclick="deleteKeyword('${key}', ${index})">❌</button>
        `;
        container.appendChild(div);
    });
}

function addKeyword(intent) {
    const key = intent + '_intent';
    
    if (!configData.keywords[key]) {
        configData.keywords[key] = [];
    }
    
    configData.keywords[key].push('new keyword');
    renderConfigKeywords();
}

function deleteKeyword(key, index) {
    if (confirm('Delete this keyword?')) {
        configData.keywords[key].splice(index, 1);
        renderConfigKeywords();
    }
}

async function saveKeywords() {
    try {
        // Collect data from inputs
        const keywordInputs = document.querySelectorAll('.keyword-item input');
        
        keywordInputs.forEach(input => {
            const key = input.dataset.key;
            const index = parseInt(input.dataset.index);
            configData.keywords[key][index] = input.value;
        });
        
        // Save to backend
        const response = await fetch('/api/config/keywords', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(configData.keywords)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ Keywords saved successfully!');
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error saving keywords: ' + error);
    }
}

// ===== Media Gallery Functions =====

async function refreshMediaGallery() {
    try {
        const response = await fetch('/api/media/list');
        const result = await response.json();
        
        if (result.success) {
            const gallery = document.getElementById('media-gallery');
            const files = result.files || [];
            
            if (files.length === 0) {
                gallery.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">📁 No media files yet. Upload images/videos above!</p>';
                return;
            }
            
            gallery.innerHTML = '';
            
            files.forEach(file => {
                const div = document.createElement('div');
                div.className = 'media-item';
                
                // Determine if image or video
                const isVideo = file.toLowerCase().endsWith('.mp4');
                const mediaPath = `media/promo/${file}`;
                
                // Check if this media is assigned to current editing template
                const isAssigned = currentEditingTemplateIndex !== null && 
                                   configData.templates.promo_templates[currentEditingTemplateIndex]?.media === mediaPath;
                
                if (isAssigned) {
                    div.classList.add('selected');
                }
                
                div.innerHTML = `
                    ${isVideo ? 
                        `<video src="/${mediaPath}" muted></video>` :
                        `<img src="/${mediaPath}" alt="${file}">`
                    }
                    ${isVideo ? '<span class="media-badge">VIDEO</span>' : ''}
                    <div class="media-item-actions">
                        <button onclick="deleteMediaFile('${file}')" title="Delete">🗑️</button>
                    </div>
                    <div class="media-item-info">
                        <div class="media-item-name" title="${file}">${file}</div>
                    </div>
                `;
                
                // Click to select/assign media
                div.onclick = function(e) {
                    if (e.target.tagName === 'BUTTON') return;
                    
                    if (currentEditingTemplateIndex !== null) {
                        assignMediaToTemplate(currentEditingTemplateIndex, file);
                    }
                };
                
                gallery.appendChild(div);
            });
        }
    } catch (error) {
        console.error('Error loading media gallery:', error);
    }
}

function showMediaGalleryForTemplate(templateIndex) {
    currentEditingTemplateIndex = templateIndex;
    
    // Remove highlight from all templates
    document.querySelectorAll('.template-item').forEach(item => {
        item.style.border = '';
        item.style.background = '';
    });
    
    // Highlight selected template
    const templateItem = document.querySelector(`.template-item[data-template-index="${templateIndex}"]`);
    if (templateItem) {
        templateItem.style.border = '3px solid #667eea';
        templateItem.style.background = '#f0f4ff';
    }
    
    // Scroll to media gallery
    const gallery = document.getElementById('media-gallery');
    gallery.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Refresh gallery to show selection
    refreshMediaGallery();
    
    // Highlight media manager
    const mediaManager = gallery.parentElement;
    const originalBorder = mediaManager.style.border;
    const originalBg = mediaManager.style.background;
    
    mediaManager.style.border = '2px solid #10b981';
    mediaManager.style.padding = '15px';
    mediaManager.style.borderRadius = '8px';
    mediaManager.style.background = '#ecfdf5';
    
    // Add instruction text
    let instruction = document.getElementById('media-instruction');
    if (!instruction) {
        instruction = document.createElement('div');
        instruction.id = 'media-instruction';
        instruction.style.cssText = 'background: #10b981; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: center; font-weight: bold;';
        gallery.parentElement.insertBefore(instruction, gallery);
    }
    instruction.textContent = `📌 Selecting media for Template ${templateIndex + 1}. Click an image below to assign.`;
    
    setTimeout(() => {
        mediaManager.style.border = originalBorder;
        mediaManager.style.padding = '';
        mediaManager.style.background = originalBg;
        if (instruction) {
            instruction.remove();
        }
    }, 5000);
}

async function assignMediaToTemplate(templateIndex, mediaFile) {
    try {
        console.log(`Assigning media "${mediaFile}" to template ${templateIndex}`);
        
        const response = await fetch('/api/templates/assign-media', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                template_index: templateIndex,
                media_file: mediaFile
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Success feedback
            alert(`✅ Success!\n\nMedia "${mediaFile}" assigned to Template ${templateIndex + 1}`);
            
            // Clear selection
            currentEditingTemplateIndex = null;
            
            // Remove highlights
            document.querySelectorAll('.template-item').forEach(item => {
                item.style.border = '';
                item.style.background = '';
            });
            
            // Remove instruction
            const instruction = document.getElementById('media-instruction');
            if (instruction) {
                instruction.remove();
            }
            
            // Reload to show updated template
            await loadConfigData();
            
            // Scroll back to the template
            setTimeout(() => {
                const updatedTemplate = document.querySelector(`.template-item[data-template-index="${templateIndex}"]`);
                if (updatedTemplate) {
                    updatedTemplate.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    // Flash animation
                    updatedTemplate.style.border = '3px solid #10b981';
                    updatedTemplate.style.background = '#ecfdf5';
                    setTimeout(() => {
                        updatedTemplate.style.border = '';
                        updatedTemplate.style.background = '';
                    }, 2000);
                }
            }, 500);
            
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error assigning media: ' + error);
        console.error('Assign media error:', error);
    }
}

async function removeMediaFromTemplate(templateIndex) {
    if (!confirm(`Remove media from Template ${templateIndex + 1}?`)) return;
    
    try {
        console.log(`Removing media from template ${templateIndex}`);
        
        const response = await fetch('/api/templates/assign-media', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                template_index: templateIndex,
                media_file: null
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`✅ Media removed from Template ${templateIndex + 1}\n\nTemplate will now post as text-only.`);
            await loadConfigData();
            
            // Highlight updated template
            setTimeout(() => {
                const updatedTemplate = document.querySelector(`.template-item[data-template-index="${templateIndex}"]`);
                if (updatedTemplate) {
                    updatedTemplate.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    updatedTemplate.style.border = '3px solid #f59e0b';
                    updatedTemplate.style.background = '#fffbeb';
                    setTimeout(() => {
                        updatedTemplate.style.border = '';
                        updatedTemplate.style.background = '';
                    }, 2000);
                }
            }, 500);
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error: ' + error);
        console.error('Remove media error:', error);
    }
}

async function deleteMediaFile(filename) {
    if (!confirm(`Delete "${filename}"?\n\nThis will remove the file permanently.`)) return;
    
    try {
        const response = await fetch('/api/media/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ Media deleted');
            await refreshMediaGallery();
            await loadConfigData(); // Reload to update templates
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Error: ' + error);
    }
}

// Handle media upload for templates
document.addEventListener('DOMContentLoaded', function() {
    const templateMediaInput = document.getElementById('input-template-media');
    if (templateMediaInput) {
        templateMediaInput.addEventListener('change', handleTemplateMediaUpload);
    }
});

async function handleTemplateMediaUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Check file size (max 15MB)
    if (file.size > 15 * 1024 * 1024) {
        alert('❌ File too large! Max 15MB');
        event.target.value = '';
        return;
    }
    
    // Check file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'video/mp4'];
    if (!allowedTypes.includes(file.type)) {
        alert('❌ Invalid file type! Only JPG, PNG, MP4 allowed');
        event.target.value = '';
        return;
    }
    
    // Upload file
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const uploadBtn = document.querySelector('.btn-primary.btn-sm');
        const originalText = uploadBtn.textContent;
        uploadBtn.textContent = '⏳ Uploading...';
        uploadBtn.disabled = true;
        
        const response = await fetch('/api/media/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ Media uploaded: ' + result.filename);
            await refreshMediaGallery();
        } else {
            alert('❌ Upload failed: ' + result.error);
        }
        
        uploadBtn.textContent = originalText;
        uploadBtn.disabled = false;
        event.target.value = '';
        
    } catch (error) {
        alert('❌ Upload error: ' + error);
        event.target.value = '';
    }
}

