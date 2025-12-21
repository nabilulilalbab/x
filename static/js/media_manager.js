// Media Manager JavaScript

let templates = [];
let mediaFiles = [];
let selectedTemplateIndex = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTemplates();
    loadMediaGallery();
});

// Load templates from API
async function loadTemplates() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        
        if (data.success) {
            templates = data.data.templates.promo_templates || [];
            renderTemplates();
        }
    } catch (error) {
        console.error('Error loading templates:', error);
        showStatus('Error loading templates', 'error');
    }
}

// Render templates list
function renderTemplates() {
    const container = document.getElementById('templates-list');
    
    if (templates.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📝</div><div class="empty-state-text">No templates found</div></div>';
        return;
    }
    
    container.innerHTML = '';
    
    templates.forEach((template, index) => {
        const text = typeof template === 'object' ? template.text : template;
        const media = typeof template === 'object' ? template.media : null;
        
        const card = document.createElement('div');
        card.className = 'template-card';
        if (selectedTemplateIndex === index) {
            card.classList.add('selected');
        }
        
        let mediaStatus = '';
        if (media) {
            const filename = media.split('/').pop();
            mediaStatus = `
                <div class="template-media-status has-media">
                    <img src="/${media}" onerror="this.style.display='none'" style="margin-right: 8px;">
                    ✅ ${filename}
                    <button onclick="removeMediaFromTemplate(${index}, event)" style="margin-left: auto; padding: 4px 8px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 11px;">Remove</button>
                </div>
            `;
        } else {
            mediaStatus = `
                <div class="template-media-status no-media">
                    ❌ No media assigned
                </div>
            `;
        }
        
        card.innerHTML = `
            <div class="template-number">Template ${index + 1}</div>
            <div class="template-text">${text.substring(0, 100)}${text.length > 100 ? '...' : ''}</div>
            ${mediaStatus}
        `;
        
        card.onclick = () => selectTemplate(index);
        
        container.appendChild(card);
    });
}

// Select template
function selectTemplate(index) {
    selectedTemplateIndex = index;
    
    const template = templates[index];
    const text = typeof template === 'object' ? template.text : template;
    
    // Update UI
    renderTemplates();
    
    // Show selected template info
    const info = document.getElementById('selected-template-info');
    const textSpan = document.getElementById('selected-template-text');
    
    info.style.display = 'block';
    textSpan.textContent = `Template ${index + 1}: ${text.substring(0, 60)}...`;
    
    // Highlight assigned media in gallery
    highlightAssignedMedia();
}

// Load media gallery
async function loadMediaGallery() {
    const gallery = document.getElementById('media-gallery');
    gallery.innerHTML = '<div class="loading"><div class="spinner"></div>Loading media...</div>';
    
    try {
        const response = await fetch('/api/media/list');
        const data = await response.json();
        
        if (data.success) {
            mediaFiles = data.files || [];
            renderMediaGallery();
        } else {
            gallery.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📁</div><div class="empty-state-text">Error loading media</div></div>';
        }
    } catch (error) {
        console.error('Error loading media:', error);
        gallery.innerHTML = '<div class="empty-state"><div class="empty-state-icon">❌</div><div class="empty-state-text">Error loading media</div></div>';
    }
}

// Render media gallery
function renderMediaGallery() {
    const gallery = document.getElementById('media-gallery');
    
    if (mediaFiles.length === 0) {
        gallery.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📁</div><div class="empty-state-text">No media files yet<br><small>Upload images/videos to get started</small></div></div>';
        return;
    }
    
    gallery.innerHTML = '';
    
    mediaFiles.forEach(filename => {
        const item = document.createElement('div');
        item.className = 'media-item';
        
        const mediaPath = `media/promo/${filename}`;
        const isVideo = filename.toLowerCase().endsWith('.mp4');
        
        // Check if this media is assigned to any template
        const assignedTo = templates.findIndex(t => 
            typeof t === 'object' && t.media === mediaPath
        );
        
        if (assignedTo >= 0) {
            item.classList.add('assigned');
        }
        
        item.innerHTML = `
            ${isVideo ? 
                `<video src="/${mediaPath}" muted></video>` :
                `<img src="/${mediaPath}" alt="${filename}">`
            }
            ${assignedTo >= 0 ? 
                `<div class="media-badge assigned">Template ${assignedTo + 1}</div>` :
                ''
            }
            <div class="media-item-overlay">
                <div class="media-item-actions">
                    <button onclick="assignMedia('${filename}', event)">Assign</button>
                    <button onclick="deleteMedia('${filename}', event)">Delete</button>
                </div>
            </div>
            <div class="media-item-info">
                <div class="media-item-name">${filename}</div>
            </div>
        `;
        
        // Click to assign if template is selected
        item.onclick = function(e) {
            if (e.target.tagName !== 'BUTTON') {
                if (selectedTemplateIndex !== null) {
                    assignMedia(filename, e);
                } else {
                    showStatus('Please select a template first', 'error');
                }
            }
        };
        
        gallery.appendChild(item);
    });
}

// Highlight assigned media
function highlightAssignedMedia() {
    if (selectedTemplateIndex === null) return;
    
    const template = templates[selectedTemplateIndex];
    const media = typeof template === 'object' ? template.media : null;
    
    document.querySelectorAll('.media-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    if (media) {
        const filename = media.split('/').pop();
        const items = document.querySelectorAll('.media-item');
        items.forEach(item => {
            if (item.textContent.includes(filename)) {
                item.style.border = '3px solid #667eea';
            }
        });
    }
}

// Assign media to selected template
async function assignMedia(filename, event) {
    event.stopPropagation();
    
    if (selectedTemplateIndex === null) {
        showStatus('Please select a template first', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/templates/assign-media', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                template_index: selectedTemplateIndex,
                media_file: filename
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus(`✅ Media assigned to Template ${selectedTemplateIndex + 1}`, 'success');
            
            // Reload data
            await loadTemplates();
            renderMediaGallery();
        } else {
            showStatus('Error: ' + result.error, 'error');
        }
    } catch (error) {
        showStatus('Error assigning media', 'error');
        console.error('Error:', error);
    }
}

// Delete media file
async function deleteMedia(filename, event) {
    event.stopPropagation();
    
    if (!confirm(`Delete "${filename}"?\n\nThis will remove the file and unassign it from any templates.`)) {
        return;
    }
    
    try {
        const response = await fetch('/api/media/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus('Media deleted', 'success');
            
            // Reload data
            await loadMediaGallery();
            await loadTemplates();
        } else {
            showStatus('Error: ' + result.error, 'error');
        }
    } catch (error) {
        showStatus('Error deleting media', 'error');
        console.error('Error:', error);
    }
}

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file
    if (file.size > 15 * 1024 * 1024) {
        showStatus('File too large! Max 15MB', 'error');
        event.target.value = '';
        return;
    }
    
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'video/mp4'];
    if (!allowedTypes.includes(file.type)) {
        showStatus('Invalid file type! Only JPG, PNG, GIF, MP4 allowed', 'error');
        event.target.value = '';
        return;
    }
    
    // Upload
    const formData = new FormData();
    formData.append('file', file);
    
    showStatus('Uploading...', 'success');
    
    try {
        const response = await fetch('/api/media/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus(`✅ Uploaded: ${result.filename}`, 'success');
            
            // Reload gallery
            await loadMediaGallery();
        } else {
            showStatus('Upload failed: ' + result.error, 'error');
        }
        
        event.target.value = '';
    } catch (error) {
        showStatus('Upload error', 'error');
        console.error('Error:', error);
        event.target.value = '';
    }
}

// Remove media from template
async function removeMediaFromTemplate(index, event) {
    event.stopPropagation();
    
    if (!confirm(`Remove media from Template ${index + 1}?`)) {
        return;
    }
    
    try {
        const response = await fetch('/api/templates/assign-media', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                template_index: index,
                media_file: null
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus(`✅ Media removed from Template ${index + 1}`, 'success');
            
            // Reload data
            await loadTemplates();
            renderMediaGallery();
        } else {
            showStatus('Error: ' + result.error, 'error');
        }
    } catch (error) {
        showStatus('Error removing media', 'error');
        console.error('Error:', error);
    }
}

// Show status message
function showStatus(message, type = 'success') {
    const statusBar = document.getElementById('status-bar');
    const statusMessage = document.getElementById('status-message');
    
    statusMessage.textContent = message;
    statusBar.className = 'status-bar ' + type;
    statusBar.style.display = 'block';
    
    setTimeout(() => {
        statusBar.style.display = 'none';
    }, 3000);
}
