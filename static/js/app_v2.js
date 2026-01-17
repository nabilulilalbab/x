/**
 * Twitter Bot Dashboard V2 - Main Application
 * Clean, reactive dashboard with native multi-account support
 */

// ============= STATE MANAGEMENT =============

const State = {
    currentAccount: null,
    accounts: [],
    accountInfo: null,
    stats: null,
    config: null,
    multiStatus: null,
    
    setCurrentAccount(accountId) {
        this.currentAccount = accountId;
        localStorage.setItem('currentAccount', accountId);
        console.log('📌 Current account set to:', accountId);
    },
    
    getCurrentAccount() {
        return this.currentAccount || localStorage.getItem('currentAccount');
    },
    
    setAccounts(accounts) {
        this.accounts = accounts;
    },
    
    getAccount(accountId) {
        return this.accounts.find(a => a.id === accountId);
    },
    
    setAccountInfo(accountInfo) {
        this.accountInfo = accountInfo;
    },
    
    setMultiStatus(status) {
        this.multiStatus = status;
    }
};

// ============= API CLIENT =============

const API = {
    baseURL: '/api/v2',
    
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Accounts
    async getAccounts() {
        return await this.request('/accounts');
    },
    
    async getAccount(accountId) {
        return await this.request(`/accounts/${accountId}`);
    },
    
    // Stats
    async getStats(accountId) {
        return await this.request(`/stats/${accountId}`);
    },
    
    async getTweets(accountId, limit = 10) {
        return await this.request(`/tweets/${accountId}?limit=${limit}`);
    },
    
    async getLogs(accountId, limit = 20) {
        return await this.request(`/logs/${accountId}?limit=${limit}`);
    },
    
    async getKeywords(accountId, days = 7) {
        return await this.request(`/keywords/${accountId}?days=${days}`);
    },
    
    // Config
    async getConfig(accountId) {
        return await this.request(`/config/${accountId}`);
    },
    
    async updateSettings(accountId, settings) {
        return await this.request(`/config/${accountId}/settings`, {
            method: 'POST',
            body: JSON.stringify(settings)
        });
    },
    
    async updateTemplates(accountId, templates) {
        return await this.request(`/config/${accountId}/templates`, {
            method: 'POST',
            body: JSON.stringify(templates)
        });
    },
    
    // Actions
    async runSlot(accountId, slot) {
        return await this.request(`/actions/${accountId}/run-slot`, {
            method: 'POST',
            body: JSON.stringify({ slot })
        });
    },
    
    // Conversions
    async getConversions(accountId, days = 7) {
        return await this.request(`/conversions/${accountId}?days=${days}`);
    },
    
    async addConversion(accountId, data) {
        return await this.request(`/conversions/${accountId}/add`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    // Multi-account control
    async getMultiStatus() {
        return await this.request('/multi/status');
    },
    
    async startAllAccounts() {
        return await this.request('/multi/start-all', { method: 'POST' });
    },
    
    async stopAllAccounts() {
        return await this.request('/multi/stop-all', { method: 'POST' });
    },
    
    async startAccount(accountId) {
        return await this.request(`/multi/accounts/${accountId}/start`, { method: 'POST' });
    },
    
    async stopAccount(accountId) {
        return await this.request(`/multi/accounts/${accountId}/stop`, { method: 'POST' });
    },
    
    async restartAccount(accountId) {
        return await this.request(`/multi/accounts/${accountId}/restart`, { method: 'POST' });
    }
};

// ============= UI HELPERS =============

const UI = {
    showLoading() {
        document.getElementById('loadingState').style.display = 'block';
        document.getElementById('noAccountState').style.display = 'none';
        document.getElementById('dashboardContent').style.display = 'none';
    },
    
    showNoAccount() {
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('noAccountState').style.display = 'block';
        document.getElementById('dashboardContent').style.display = 'none';
    },
    
    showDashboard() {
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('noAccountState').style.display = 'none';
        document.getElementById('dashboardContent').style.display = 'block';
    },
    
    showAlert(message, type = 'success') {
        const container = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        
        container.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 5000);
    },
    
    renderStats(stats) {
        const grid = document.getElementById('statsGrid');
        
        // Get account info including WA number
        const account = State.accountInfo || {};
        const waNumber = account.wa_number || '-';
        const waLink = account.wa_link || '#';
        
        grid.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">WhatsApp Order</div>
                <div class="stat-value" style="font-size: 18px;">
                    ${waNumber !== '-' ? 
                        `<a href="${waLink}" target="_blank" style="color: #10b981; text-decoration: none;">📱 ${waNumber}</a>` : 
                        '<span style="color: #999;">Not set</span>'
                    }
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Followers</div>
                <div class="stat-value">${stats.followers?.current || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Tweets Today</div>
                <div class="stat-value">${stats.today?.tweets_posted || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Likes Today</div>
                <div class="stat-value">${stats.today?.likes_given || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Replies Today</div>
                <div class="stat-value">${stats.today?.replies_made || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Engagement Rate</div>
                <div class="stat-value">${((stats.tweets?.avg_engagement || 0) * 100).toFixed(2)}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Orders (7d)</div>
                <div class="stat-value">${stats.conversions?.week?.total_orders || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Revenue (7d)</div>
                <div class="stat-value" style="font-size: 18px;">Rp ${(stats.conversions?.week?.total_revenue || 0).toLocaleString('id-ID')}</div>
            </div>
        `;
    },
    
    renderTweets(tweets) {
        const container = document.getElementById('recentTweets');
        
        if (!tweets || tweets.length === 0) {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No tweets yet</p>';
            return;
        }
        
        let html = '<table><thead><tr><th>Tweet</th><th>Type</th><th>Views</th><th>Likes</th><th>Engagement</th></tr></thead><tbody>';
        
        tweets.forEach(tweet => {
            const engagementRate = ((tweet.engagement_rate || 0) * 100).toFixed(2);
            html += `
                <tr>
                    <td>${tweet.tweet_text.substring(0, 60)}...</td>
                    <td>${tweet.tweet_type}</td>
                    <td>${tweet.views || 0}</td>
                    <td>${tweet.likes || 0}</td>
                    <td>${engagementRate}%</td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    },
    
    renderKeywords(keywords) {
        const container = document.getElementById('keywordPerformance');
        
        if (!keywords || keywords.length === 0) {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No keyword data yet</p>';
            return;
        }
        
        let html = '<table><thead><tr><th>Keyword</th><th>Found</th><th>Engaged</th><th>Rate</th></tr></thead><tbody>';
        
        keywords.forEach(kw => {
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
    },
    
    renderSettings(settings) {
        const container = document.getElementById('settingsEditor');
        const business = settings.business || {};
        
        container.innerHTML = `
            <div class="form-group">
                <label>Product Name</label>
                <input type="text" id="input-product" value="${business.product || ''}" />
            </div>
            <div class="form-group">
                <label>WhatsApp Number</label>
                <input type="text" id="input-wa-number" value="${business.wa_number || ''}" />
            </div>
            <div class="form-group">
                <label>WhatsApp Link</label>
                <input type="text" id="input-wa-link" value="${business.wa_link || ''}" />
            </div>
            <button class="btn btn-success" onclick="app.saveSettings()">💾 Save Settings</button>
        `;
    },
    
    renderTemplates(templates) {
        const container = document.getElementById('templatesEditor');
        const promoTemplates = templates.promo_templates || [];
        
        let html = '<h4>Promo Templates</h4>';
        
        promoTemplates.forEach((template, index) => {
            const text = typeof template === 'object' ? template.text : template;
            html += `
                <div class="template-item">
                    <textarea id="template-${index}" data-index="${index}">${text}</textarea>
                    <div class="template-actions">
                        <button class="btn btn-sm btn-danger" onclick="app.deleteTemplate(${index})">🗑️ Delete</button>
                    </div>
                </div>
            `;
        });
        
        html += '<button class="btn btn-primary" onclick="app.addTemplate()">➕ Add Template</button>';
        html += '<button class="btn btn-success" onclick="app.saveTemplates()" style="margin-left: 10px;">💾 Save Templates</button>';
        
        container.innerHTML = html;
    },
    
    renderLogs(logs) {
        const container = document.getElementById('activityLogs');
        
        if (!logs || logs.length === 0) {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No logs yet</p>';
            return;
        }
        
        let html = '';
        
        logs.forEach(log => {
            const time = new Date(log.timestamp).toLocaleTimeString();
            const message = log.details || log.activity_type;
            
            html += `
                <div class="log-entry">
                    <div class="log-time">${time}</div>
                    <div>${message}</div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }
};

// ============= MAIN APP =============

const app = {
    async init() {
        console.log('🚀 Initializing Dashboard V2...');
        
        try {
            // Load accounts
            const response = await API.getAccounts();
            State.setAccounts(response.data.accounts);
            
            // Load multi-account status
            await this.loadMultiStatus();
            
            // Populate account selector
            this.populateAccountSelector();
            
            // Restore last selected account
            const lastAccount = State.getCurrentAccount();
            if (lastAccount && State.getAccount(lastAccount)) {
                document.getElementById('accountSelector').value = lastAccount;
                await this.selectAccount(lastAccount);
            } else {
                UI.showNoAccount();
            }
            
            console.log('✅ Dashboard initialized');
        } catch (error) {
            console.error('❌ Initialization error:', error);
            UI.showAlert('Failed to initialize dashboard: ' + error.message, 'error');
        }
    },
    
    populateAccountSelector() {
        const selector = document.getElementById('accountSelector');
        
        // Clear existing options except first
        while (selector.options.length > 1) {
            selector.remove(1);
        }
        
        // Add account options
        State.accounts.forEach(account => {
            const option = document.createElement('option');
            option.value = account.id;
            option.textContent = `${account.name} (${account.username})`;
            if (!account.enabled) {
                option.textContent += ' [Disabled]';
            }
            selector.appendChild(option);
        });
    },
    
    async selectAccount(accountId) {
        if (!accountId) {
            UI.showNoAccount();
            return;
        }
        
        console.log('🔄 Switching to account:', accountId);
        UI.showLoading();
        
        try {
            // Set current account
            State.setCurrentAccount(accountId);
            
            // Load account info first (including wa_number)
            const accountResponse = await API.getAccount(accountId);
            State.setAccountInfo(accountResponse.data);
            
            // Load all data
            await Promise.all([
                this.loadStats(),
                this.loadTweets(),
                this.loadKeywords(),
                this.loadConfig(),
                this.loadLogs(),
                this.loadMultiStatus()
            ]);
            
            // Show dashboard
            UI.showDashboard();
            
            console.log('✅ Account loaded:', accountId);
        } catch (error) {
            console.error('❌ Error loading account:', error);
            UI.showAlert('Failed to load account data: ' + error.message, 'error');
            UI.showNoAccount();
        }
    },
    
    async loadStats() {
        const accountId = State.getCurrentAccount();
        const response = await API.getStats(accountId);
        State.stats = response.data;
        UI.renderStats(response.data);
    },
    
    async loadTweets() {
        const accountId = State.getCurrentAccount();
        const response = await API.getTweets(accountId);
        UI.renderTweets(response.data);
    },
    
    async loadKeywords() {
        const accountId = State.getCurrentAccount();
        const response = await API.getKeywords(accountId);
        UI.renderKeywords(response.data);
    },
    
    async loadConfig() {
        const accountId = State.getCurrentAccount();
        const response = await API.getConfig(accountId);
        State.config = response.data;
        UI.renderSettings(response.data.settings);
        UI.renderTemplates(response.data.templates);
    },
    
    async loadLogs() {
        const accountId = State.getCurrentAccount();
        const response = await API.getLogs(accountId);
        UI.renderLogs(response.data);
    },
    
    async refresh() {
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        UI.showAlert('Refreshing data...', 'success');
        await this.selectAccount(accountId);
    },
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`tab-${tabName}`).classList.add('active');
        
        // Load data when switching tabs
        if (tabName === 'accounts') {
            // Reload accounts from server first to get latest data
            API.getAccounts().then(response => {
                State.setAccounts(response.data.accounts);
                this.loadAccountsTable();
            });
        } else if (tabName === 'config') {
            // Load media list when opening config tab
            this.loadMediaList();
        }
    },
    
    async saveSettings() {
        const accountId = State.getCurrentAccount();
        
        try {
            const settings = State.config.settings;
            settings.business.product = document.getElementById('input-product').value;
            settings.business.wa_number = document.getElementById('input-wa-number').value;
            settings.business.wa_link = document.getElementById('input-wa-link').value;
            
            await API.updateSettings(accountId, settings);
            UI.showAlert('Settings saved successfully!', 'success');
        } catch (error) {
            console.error('Error saving settings:', error);
            UI.showAlert('Failed to save settings: ' + error.message, 'error');
        }
    },
    
    addTemplate() {
        const templates = State.config.templates;
        if (!templates.promo_templates) {
            templates.promo_templates = [];
        }
        
        templates.promo_templates.push({
            text: '🔥 New template here...',
            media: null
        });
        
        UI.renderTemplates(templates);
    },
    
    deleteTemplate(index) {
        if (!confirm('Delete this template?')) return;
        
        const templates = State.config.templates;
        templates.promo_templates.splice(index, 1);
        UI.renderTemplates(templates);
    },
    
    async saveTemplates() {
        const accountId = State.getCurrentAccount();
        
        try {
            const templates = State.config.templates;
            
            // Update templates from textareas
            const textareas = document.querySelectorAll('#templatesEditor textarea');
            textareas.forEach(textarea => {
                const index = parseInt(textarea.dataset.index);
                const currentTemplate = templates.promo_templates[index];
                
                if (typeof currentTemplate === 'object') {
                    currentTemplate.text = textarea.value;
                } else {
                    templates.promo_templates[index] = {
                        text: textarea.value,
                        media: null
                    };
                }
            });
            
            await API.updateTemplates(accountId, templates);
            UI.showAlert('Templates saved successfully!', 'success');
        } catch (error) {
            console.error('Error saving templates:', error);
            UI.showAlert('Failed to save templates: ' + error.message, 'error');
        }
    },
    
    async runSlot(slot) {
        const accountId = State.getCurrentAccount();
        
        if (!confirm(`Run ${slot} slot now?`)) return;
        
        try {
            await API.runSlot(accountId, slot);
            UI.showAlert(`${slot} slot started! Check logs for progress.`, 'success');
            
            // Refresh logs after 3 seconds
            setTimeout(() => this.loadLogs(), 3000);
        } catch (error) {
            console.error('Error running slot:', error);
            UI.showAlert('Failed to run slot: ' + error.message, 'error');
        }
    },
    
    async addConversion() {
        const accountId = State.getCurrentAccount();
        
        try {
            const data = {
                source: document.getElementById('input-conv-source').value,
                wa_messages: parseInt(document.getElementById('input-conv-messages').value),
                confirmed_orders: parseInt(document.getElementById('input-conv-orders').value),
                revenue: parseInt(document.getElementById('input-conv-revenue').value)
            };
            
            await API.addConversion(accountId, data);
            UI.showAlert('Conversion added successfully!', 'success');
            
            // Reset form
            document.getElementById('input-conv-messages').value = '1';
            document.getElementById('input-conv-orders').value = '1';
            document.getElementById('input-conv-revenue').value = '0';
            
            // Refresh stats
            await this.loadStats();
        } catch (error) {
            console.error('Error adding conversion:', error);
            UI.showAlert('Failed to add conversion: ' + error.message, 'error');
        }
    },
    
    // Multi-account control functions
    async loadMultiStatus() {
        try {
            const response = await API.getMultiStatus();
            State.setMultiStatus(response.data);
            this.updateControlButtons();
        } catch (error) {
            console.error('Error loading multi status:', error);
        }
    },
    
    async startAllAccounts() {
        try {
            UI.showAlert('Starting all accounts...', 'info');
            await API.startAllAccounts();
            
            setTimeout(async () => {
                await this.loadMultiStatus();
                UI.showAlert('Start command sent to all accounts', 'success');
            }, 2000);
        } catch (error) {
            console.error('Error starting all:', error);
            UI.showAlert('Failed to start all accounts: ' + error.message, 'error');
        }
    },
    
    async stopAllAccounts() {
        try {
            UI.showAlert('Stopping all accounts...', 'info');
            await API.stopAllAccounts();
            
            setTimeout(async () => {
                await this.loadMultiStatus();
                UI.showAlert('Stop command sent to all accounts', 'success');
            }, 2000);
        } catch (error) {
            console.error('Error stopping all:', error);
            UI.showAlert('Failed to stop all accounts: ' + error.message, 'error');
        }
    },
    
    async startCurrentAccount() {
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        try {
            UI.showAlert(`Starting ${accountId}...`, 'info');
            await API.startAccount(accountId);
            
            setTimeout(async () => {
                await this.loadMultiStatus();
                UI.showAlert(`Start command sent to ${accountId}`, 'success');
            }, 2000);
        } catch (error) {
            console.error('Error starting account:', error);
            UI.showAlert('Failed to start account: ' + error.message, 'error');
        }
    },
    
    async stopCurrentAccount() {
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        try {
            UI.showAlert(`Stopping ${accountId}...`, 'info');
            await API.stopAccount(accountId);
            
            setTimeout(async () => {
                await this.loadMultiStatus();
                UI.showAlert(`Stop command sent to ${accountId}`, 'success');
            }, 2000);
        } catch (error) {
            console.error('Error stopping account:', error);
            UI.showAlert('Failed to stop account: ' + error.message, 'error');
        }
    },
    
    async restartCurrentAccount() {
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        try {
            UI.showAlert(`Restarting ${accountId}...`, 'info');
            await API.restartAccount(accountId);
            
            setTimeout(async () => {
                await this.loadMultiStatus();
                UI.showAlert(`Restart command sent to ${accountId}`, 'success');
            }, 2000);
        } catch (error) {
            console.error('Error restarting account:', error);
            UI.showAlert('Failed to restart account: ' + error.message, 'error');
        }
    },
    
    updateControlButtons() {
        const accountId = State.getCurrentAccount();
        if (!accountId || !State.multiStatus) return;
        
        const statuses = State.multiStatus.statuses || {};
        const accountStatus = statuses[accountId];
        
        if (!accountStatus) return;
        
        const isRunning = accountStatus.status === 'running';
        
        // Update button visibility/state
        const startBtn = document.getElementById('btnStartAccount');
        const stopBtn = document.getElementById('btnStopAccount');
        const restartBtn = document.getElementById('btnRestartAccount');
        
        if (startBtn) startBtn.style.display = isRunning ? 'none' : 'inline-block';
        if (stopBtn) stopBtn.style.display = isRunning ? 'inline-block' : 'none';
        if (restartBtn) restartBtn.style.display = isRunning ? 'inline-block' : 'none';
        
        // Update status indicator
        const statusIndicator = document.getElementById('accountStatusIndicator');
        if (statusIndicator) {
            const statusIcon = isRunning ? '🟢' : accountStatus.status === 'idle' ? '⚪' : '🔴';
            const statusText = accountStatus.status.toUpperCase();
            statusIndicator.innerHTML = `${statusIcon} ${statusText}`;
        }
    },
    
    // Account Management Functions
    async loadAccountsTable() {
        try {
            const response = await API.getAccounts();
            const accounts = response.data.accounts;
            
            const tbody = document.getElementById('accountsTableBody');
            if (!tbody) return;
            
            if (accounts.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="padding: 20px; text-align: center; color: #999;">No accounts found. Click Add Account to create one.</td></tr>';
                return;
            }
            
            tbody.innerHTML = accounts.map(account => {
                const status = State.multiStatus?.statuses?.[account.id]?.status || 'unknown';
                const statusIcon = status === 'running' ? '🟢' : status === 'idle' ? '⚪' : '🔴';
                const waNumber = account.wa_number || '-';
                
                return `
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 12px;"><strong>${account.id}</strong></td>
                        <td style="padding: 12px;">${account.name}</td>
                        <td style="padding: 12px;">${account.username}</td>
                        <td style="padding: 12px;">📱 ${waNumber}</td>
                        <td style="padding: 12px;">${statusIcon} ${status.toUpperCase()}</td>
                        <td style="padding: 12px;">
                            <label style="display: flex; align-items: center; cursor: pointer;">
                                <input type="checkbox" ${account.enabled ? 'checked' : ''} onchange="app.toggleAccountEnabled('${account.id}', this.checked)" style="margin-right: 5px;">
                            </label>
                        </td>
                        <td style="padding: 12px;">
                            <div style="display: flex; gap: 5px; flex-wrap: wrap;">
                                ${status === 'running' ? 
                                    `<button class="btn btn-sm" style="background: #ef4444; color: white; padding: 5px 10px; font-size: 12px;" onclick="app.stopAccount('${account.id}')">⏹️ Stop</button>` :
                                    `<button class="btn btn-sm" style="background: #10b981; color: white; padding: 5px 10px; font-size: 12px;" onclick="app.startAccount('${account.id}')">▶️ Start</button>`
                                }
                                <button class="btn btn-sm" style="background: #667eea; color: white; padding: 5px 10px; font-size: 12px;" onclick="app.showEditAccountModal('${account.id}')">✏️ Edit</button>
                                <button class="btn btn-sm" style="background: #f59e0b; color: white; padding: 5px 10px; font-size: 12px;" onclick="app.showCookiesModal('${account.id}')">🍪 Cookies</button>
                                <button class="btn btn-sm" style="background: #ef4444; color: white; padding: 5px 10px; font-size: 12px;" onclick="app.deleteAccount('${account.id}')" ${account.enabled ? 'disabled title="Disable account first"' : ''}>🗑️ Delete</button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        } catch (error) {
            console.error('Error loading accounts table:', error);
        }
    },
    
    showAddAccountModal() {
        document.getElementById('accountModalTitle').textContent = '➕ Add New Account';
        document.getElementById('accountForm').reset();
        document.getElementById('accountId').disabled = false;
        document.getElementById('accountModal').style.display = 'flex';
    },
    
    showEditAccountModal(accountId) {
        const account = State.getAccount(accountId);
        if (!account) return;
        
        document.getElementById('accountModalTitle').textContent = '✏️ Edit Account';
        document.getElementById('accountId').value = account.id;
        document.getElementById('accountId').disabled = true;
        document.getElementById('accountName').value = account.name;
        document.getElementById('accountUsername').value = account.username;
        document.getElementById('accountWaNumber').value = account.wa_number || '';
        document.getElementById('accountDescription').value = account.description || '';
        document.getElementById('accountEnabled').checked = account.enabled;
        document.getElementById('accountModal').style.display = 'flex';
    },
    
    closeAccountModal() {
        document.getElementById('accountModal').style.display = 'none';
    },
    
    async saveAccount(event) {
        event.preventDefault();
        
        const accountData = {
            id: document.getElementById('accountId').value,
            name: document.getElementById('accountName').value,
            username: document.getElementById('accountUsername').value,
            wa_number: document.getElementById('accountWaNumber').value,
            description: document.getElementById('accountDescription').value,
            enabled: document.getElementById('accountEnabled').checked
        };
        
        try {
            UI.showAlert('Saving account...', 'info');
            
            // Use dashboard.py API for account creation
            const response = await fetch('http://localhost:5000/api/accounts/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(accountData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                UI.showAlert('✅ Account saved successfully!', 'success');
                this.closeAccountModal();
                
                // Reload accounts and refresh everything
                const accountsResponse = await API.getAccounts();
                State.setAccounts(accountsResponse.data.accounts);
                await this.loadMultiStatus(); // Refresh status
                this.populateAccountSelector();
                this.loadAccountsTable(); // Refresh table
            } else {
                UI.showAlert('❌ Error: ' + result.error, 'error');
            }
        } catch (error) {
            console.error('Error saving account:', error);
            UI.showAlert('Failed to save account: ' + error.message, 'error');
        }
    },
    
    async toggleAccountEnabled(accountId, enabled) {
        try {
            UI.showAlert(`${enabled ? '✅ Enabling' : '⏸️ Disabling'} account...`, 'info');
            
            const response = await fetch(`http://localhost:5000/api/accounts/${accountId}/update`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled })
            });
            
            const result = await response.json();
            
            if (result.success) {
                UI.showAlert(`✅ Account ${enabled ? 'enabled' : 'disabled'}`, 'success');
                
                // Wait a bit for AccountManager to reload
                await new Promise(resolve => setTimeout(resolve, 500));
                
                // Reload accounts from server
                const accountsResponse = await API.getAccounts();
                State.setAccounts(accountsResponse.data.accounts);
                await this.loadAccountsTable();
            } else {
                UI.showAlert('❌ Error: ' + result.error, 'error');
                // Revert checkbox
                await this.loadAccountsTable();
            }
        } catch (error) {
            console.error('Error toggling account:', error);
            UI.showAlert('❌ Failed to toggle account: ' + error.message, 'error');
            // Revert checkbox
            await this.loadAccountsTable();
        }
    },
    
    async deleteAccount(accountId) {
        const account = State.getAccount(accountId);
        const accountName = account ? account.name : accountId;
        
        if (!confirm(`⚠️ Are you sure you want to delete account "${accountName}"?\n\nThis will:\n• Delete account folder\n• Remove from config\n• Create backup\n\nThis cannot be easily undone!`)) {
            return;
        }
        
        try {
            UI.showAlert('🗑️ Deleting account...', 'info');
            
            const response = await fetch(`http://localhost:5000/api/accounts/${accountId}/delete`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                UI.showAlert('✅ Account deleted successfully', 'success');
                
                // Reload accounts
                const accountsResponse = await API.getAccounts();
                State.setAccounts(accountsResponse.data.accounts);
                this.populateAccountSelector();
                await this.loadAccountsTable();
            } else {
                UI.showAlert('❌ Error: ' + result.error, 'error');
            }
        } catch (error) {
            console.error('Error deleting account:', error);
            UI.showAlert('❌ Failed to delete account: ' + error.message, 'error');
        }
    },
    
    showCookiesModal(accountId) {
        const account = State.getAccount(accountId);
        if (!account) return;
        
        document.getElementById('cookiesAccountName').textContent = account.name;
        document.getElementById('cookiesInput').value = '';
        document.getElementById('cookiesInput').dataset.accountId = accountId;
        document.getElementById('cookiesModal').style.display = 'flex';
    },
    
    closeCookiesModal() {
        document.getElementById('cookiesModal').style.display = 'none';
    },
    
    async saveCookies() {
        const cookiesInput = document.getElementById('cookiesInput');
        const cookiesText = cookiesInput.value.trim();
        
        if (!cookiesText) {
            UI.showAlert('⚠️ Please paste cookies JSON', 'error');
            return;
        }
        
        const accountId = cookiesInput.dataset.accountId;
        
        try {
            UI.showAlert('🔄 Validating and saving cookies...', 'info');
            
            // Parse JSON
            let cookiesData;
            try {
                cookiesData = JSON.parse(cookiesText);
            } catch (e) {
                UI.showAlert('❌ Invalid JSON format. Please check your cookies.', 'error');
                return;
            }
            
            // Send to Dashboard V1 API (which handles conversion and validation)
            const response = await fetch(`http://localhost:5000/api/accounts/${accountId}/cookies/upload`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cookies: cookiesData })
            });
            
            const result = await response.json();
            
            if (result.success) {
                UI.showAlert('✅ Cookies saved and validated successfully!', 'success');
                this.closeCookiesModal();
                
                // Refresh account info
                await this.loadMultiStatus();
                
                // If on accounts tab, refresh table
                if (document.getElementById('tab-accounts').classList.contains('active')) {
                    await this.loadAccountsTable();
                }
            } else {
                UI.showAlert('❌ Error: ' + result.error, 'error');
            }
        } catch (error) {
            console.error('Error saving cookies:', error);
            UI.showAlert('❌ Failed to save cookies: ' + error.message, 'error');
        }
    },
    
    async startAccount(accountId) {
        try {
            UI.showAlert(`Starting ${accountId}...`, 'info');
            await API.startAccount(accountId);
            
            setTimeout(async () => {
                await this.loadMultiStatus();
                await this.loadAccountsTable();
                UI.showAlert(`${accountId} started`, 'success');
            }, 2000);
        } catch (error) {
            console.error('Error starting account:', error);
            UI.showAlert('Failed to start account: ' + error.message, 'error');
        }
    },
    
    async stopAccount(accountId) {
        try {
            UI.showAlert(`Stopping ${accountId}...`, 'info');
            await API.stopAccount(accountId);
            
            setTimeout(async () => {
                await this.loadMultiStatus();
                await this.loadAccountsTable();
                UI.showAlert(`${accountId} stopped`, 'success');
            }, 2000);
        } catch (error) {
            console.error('Error stopping account:', error);
            UI.showAlert('Failed to stop account: ' + error.message, 'error');
        }
    },
    
    // Media Management Functions
    async loadMediaList() {
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        try {
            const response = await fetch(`/api/v2/accounts/${accountId}/media`);
            const result = await response.json();
            
            const mediaList = document.getElementById('mediaList');
            if (!mediaList) return;
            
            if (result.success && result.data.media_files.length > 0) {
                mediaList.innerHTML = result.data.media_files.map(file => `
                    <div style="border: 2px solid #e5e7eb; border-radius: 8px; padding: 10px; text-align: center;">
                        <div style="height: 100px; background: #f9fafb; border-radius: 4px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; overflow: hidden;">
                            ${file.type === 'video' ? 
                                `<video src="${file.url}" style="max-width: 100%; max-height: 100%; object-fit: contain;" muted></video>` :
                                `<img src="${file.url}" style="max-width: 100%; max-height: 100%; object-fit: contain;" alt="${file.name}">`
                            }
                        </div>
                        <div style="font-size: 12px; font-weight: 600; margin-bottom: 5px; word-break: break-all;">${file.name}</div>
                        <div style="font-size: 11px; color: #999;">${(file.size / 1024).toFixed(1)} KB</div>
                    </div>
                `).join('');
            } else {
                mediaList.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 20px; color: #999;">No media files. Click Upload Media to add.</div>';
            }
            
            // Also load templates
            await this.loadTemplatesList();
        } catch (error) {
            console.error('Error loading media:', error);
        }
    },
    
    async loadTemplatesList() {
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        try {
            const response = await API.getConfig(accountId);
            const config = response.data;
            
            const templatesList = document.getElementById('templatesList');
            if (!templatesList) return;
            
            const promoTemplates = config.templates?.promo_templates || [];
            
            if (promoTemplates.length === 0) {
                templatesList.innerHTML = '<div style="text-align: center; padding: 20px; color: #999;">No promo templates found.</div>';
                return;
            }
            
            // Get media files
            const mediaResponse = await fetch(`/api/v2/accounts/${accountId}/media`);
            const mediaResult = await mediaResponse.json();
            const mediaFiles = mediaResult.success ? mediaResult.data.media_files : [];
            
            templatesList.innerHTML = promoTemplates.map((template, index) => {
                const text = typeof template === 'object' ? template.text : template;
                const media = typeof template === 'object' ? template.media : null;
                const mediaFile = media ? media.split('/').pop() : null;
                
                return `
                    <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: between; align-items: start; gap: 15px;">
                            <div style="flex: 1;">
                                <div style="font-weight: 600; margin-bottom: 5px;">Template ${index + 1}</div>
                                <div style="font-size: 14px; color: #666; margin-bottom: 10px;">${text.substring(0, 100)}${text.length > 100 ? '...' : ''}</div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <select onchange="app.assignMediaToTemplate(${index}, this.value)" style="padding: 5px 10px; border: 1px solid #e5e7eb; border-radius: 4px;">
                                        <option value="">No media</option>
                                        ${mediaFiles.map(file => `
                                            <option value="${file.name}" ${mediaFile === file.name ? 'selected' : ''}>${file.name}</option>
                                        `).join('')}
                                    </select>
                                    ${media ? `<span style="color: #10b981;">✅ ${mediaFile}</span>` : '<span style="color: #999;">No media</span>'}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        } catch (error) {
            console.error('Error loading templates:', error);
        }
    },
    
    showUploadMediaModal() {
        document.getElementById('mediaFileInput').value = '';
        document.getElementById('uploadMediaModal').style.display = 'flex';
    },
    
    closeUploadMediaModal() {
        document.getElementById('uploadMediaModal').style.display = 'none';
    },
    
    async uploadMedia() {
        const fileInput = document.getElementById('mediaFileInput');
        const file = fileInput.files[0];
        
        if (!file) {
            UI.showAlert('⚠️ Please select a file', 'error');
            return;
        }
        
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        try {
            UI.showAlert('📤 Uploading media...', 'info');
            
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`/api/v2/accounts/${accountId}/media/upload`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                UI.showAlert('✅ Media uploaded successfully!', 'success');
                this.closeUploadMediaModal();
                await this.loadMediaList();
            } else {
                UI.showAlert('❌ Error: ' + result.error, 'error');
            }
        } catch (error) {
            console.error('Error uploading media:', error);
            UI.showAlert('❌ Failed to upload media: ' + error.message, 'error');
        }
    },
    
    async assignMediaToTemplate(templateIndex, mediaFile) {
        const accountId = State.getCurrentAccount();
        if (!accountId) return;
        
        try {
            UI.showAlert('🔄 Assigning media to template...', 'info');
            
            const response = await fetch(`/api/v2/accounts/${accountId}/templates/assign-media`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    template_index: templateIndex,
                    media_file: mediaFile || null
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                UI.showAlert('✅ Media assigned successfully!', 'success');
                await this.loadTemplatesList();
            } else {
                UI.showAlert('❌ Error: ' + result.error, 'error');
            }
        } catch (error) {
            console.error('Error assigning media:', error);
            UI.showAlert('❌ Failed to assign media: ' + error.message, 'error');
        }
    }
};

// ============= EVENT LISTENERS =============

document.addEventListener('DOMContentLoaded', () => {
    app.init();
    
    // Account selector change
    document.getElementById('accountSelector').addEventListener('change', (e) => {
        app.selectAccount(e.target.value);
    });
});

// Auto-refresh every 30 seconds
setInterval(() => {
    const accountId = State.getCurrentAccount();
    if (accountId) {
        app.loadStats();
        app.loadLogs();
        app.loadMultiStatus();
    }
}, 30000);

console.log('✅ Dashboard V2 loaded!');
