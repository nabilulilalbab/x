// Config Editor Patch for Multi-Account
// This ensures all config editing functions work properly

(function() {
    'use strict';
    
    console.log('🔧 Loading config editor patch...');
    
    // Wait for original functions to be defined
    const waitForFunctions = setInterval(function() {
        if (typeof window.addTemplate !== 'undefined' && 
            typeof window.addTip !== 'undefined' && 
            typeof window.addPrice !== 'undefined' &&
            typeof window.addKeyword !== 'undefined') {
            
            clearInterval(waitForFunctions);
            
            // Store originals
            const originalAddTemplate = window.addTemplate;
            const originalAddTip = window.addTip;
            const originalAddPrice = window.addPrice;
            const originalAddKeyword = window.addKeyword;
            
            // Override addTemplate
            window.addTemplate = function(type) {
                console.log('🔧 addTemplate called for type:', type);
                
                if (!window.configData || !window.configData.templates) {
                    console.error('❌ configData.templates not loaded');
                    alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
                    return;
                }
                
                try {
                    originalAddTemplate(type);
                    console.log('✅ Template added successfully');
                } catch (error) {
                    console.error('❌ Error in addTemplate:', error);
                    
                    // Fallback: add manually
                    const key = type === 'promo' ? 'promo_templates' : 'value_templates';
                    
                    if (!window.configData.templates[key]) {
                        window.configData.templates[key] = [];
                    }
                    
                    if (type === 'promo') {
                        window.configData.templates[key].push({
                            text: '🔥 KUOTA XL MURAH! 10GB cuma Rp25.000! Order: {wa_number}',
                            media: null
                        });
                    } else {
                        window.configData.templates[key].push('💡 Tips hemat kuota baru...');
                    }
                    
                    if (window.renderConfigTemplates) {
                        window.renderConfigTemplates();
                    }
                }
            };
            
            // Override addTip
            window.addTip = function() {
                console.log('🔧 addTip called');
                
                if (!window.configData || !window.configData.templates) {
                    console.error('❌ configData.templates not loaded');
                    alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
                    return;
                }
                
                try {
                    originalAddTip();
                    console.log('✅ Tip added successfully');
                } catch (error) {
                    console.error('❌ Error in addTip:', error);
                    
                    // Fallback: add manually
                    if (!window.configData.templates.tips) {
                        window.configData.templates.tips = [];
                    }
                    
                    window.configData.templates.tips.push('Your tip here...');
                    
                    if (window.renderConfigTemplates) {
                        window.renderConfigTemplates();
                    }
                }
            };
            
            // Override addPrice
            window.addPrice = function() {
                console.log('🔧 addPrice called');
                
                if (!window.configData || !window.configData.settings || !window.configData.settings.business) {
                    console.error('❌ configData.settings.business not loaded');
                    alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
                    return;
                }
                
                try {
                    originalAddPrice();
                    console.log('✅ Price added successfully');
                } catch (error) {
                    console.error('❌ Error in addPrice:', error);
                    
                    // Fallback: add manually
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
                }
            };
            
            // Override addKeyword
            window.addKeyword = function(intent) {
                console.log('🔧 addKeyword called for intent:', intent);
                
                if (!window.configData || !window.configData.keywords) {
                    console.error('❌ configData.keywords not loaded');
                    alert('⚠️ Config not loaded yet. Please wait a moment and try again.');
                    return;
                }
                
                try {
                    originalAddKeyword(intent);
                    console.log('✅ Keyword added successfully');
                } catch (error) {
                    console.error('❌ Error in addKeyword:', error);
                    
                    // Fallback: add manually
                    const key = intent + '_intent';
                    
                    if (!window.configData.keywords[key]) {
                        window.configData.keywords[key] = [];
                    }
                    
                    window.configData.keywords[key].push('new keyword');
                    
                    if (window.renderConfigKeywords) {
                        window.renderConfigKeywords();
                    }
                }
            };
            
            console.log('✅ Config editor patch applied successfully!');
            console.log('   - addTemplate patched');
            console.log('   - addTip patched');
            console.log('   - addPrice patched');
            console.log('   - addKeyword patched');
        }
    }, 100); // Check every 100ms
    
    // Stop checking after 10 seconds
    setTimeout(function() {
        clearInterval(waitForFunctions);
    }, 10000);
})();
