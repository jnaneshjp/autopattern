let workflows = [];

// ---------- Init ----------
document.addEventListener('DOMContentLoaded', () => {
    loadWorkflows();
});

chrome.runtime.onMessage.addListener(msg => {
    if (msg.action === 'refresh_dashboard') {
        loadWorkflows();
    }
});

// ---------- Load ----------
function loadWorkflows() {
    chrome.runtime.sendMessage({ action: 'GET_WORKFLOWS' }, res => {
        if (res?.status === 'ok') {
            workflows = res.workflows || [];
            renderWorkflows();
        }
    });
}

// ---------- Render ----------
function renderWorkflows() {
    const list = document.getElementById('workflows-list');
    list.innerHTML = '';

    if (!workflows.length) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = `
            <span class="empty-state-icon">📭</span>
            <p>No workflows recorded yet. Start by opening the extension popup!</p>
        `;
        list.appendChild(emptyState);
        updateStats({ workflows: 0 });
        return;
    }

    workflows.forEach((w, idx) => {
        const div = document.createElement('div');
        div.className = 'workflow-card';
        
        const title = document.createElement('h3');
        title.textContent = w.name;
        
        const date = document.createElement('small');
        date.textContent = new Date(w.createdAt).toLocaleString();
        
        const viewBtn = document.createElement('button');
        viewBtn.className = 'btn-view';
        viewBtn.textContent = 'View';
        viewBtn.onclick = (e) => {
            e.preventDefault();
            viewWorkflow(idx);
        };
        
        const automateBtn = document.createElement('button');
        automateBtn.className = 'btn-automate';
        automateBtn.textContent = 'Automate';
        automateBtn.onclick = (e) => {
            e.preventDefault();
            // Functionality to be added later
        };
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn-delete';
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = (e) => {
            e.preventDefault();
            deleteWorkflow(idx);
        };
        
        const actions = document.createElement('div');
        actions.className = 'workflow-actions';
        actions.appendChild(viewBtn);
        actions.appendChild(automateBtn);
        actions.appendChild(deleteBtn);
        
        div.appendChild(title);
        div.appendChild(date);
        div.appendChild(actions);
        list.appendChild(div);
    });

    updateStats({ workflows: workflows.length });
}


// ---------- Stats ----------
function updateStats(stats) {
    document.getElementById('stat-workflows').textContent = stats.workflows || 0;
}

// ---------- Actions ----------
function viewWorkflow(idx) {
    const wf = workflows[idx];
    if (!wf) {
        console.error('Workflow not found at index', idx);
        return;
    }

    const events = wf.events || [];

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';

    const content = document.createElement('div');
    content.className = 'modal-content';
    
    const title = document.createElement('h3');
    title.textContent = wf.name;
    
    const eventInfo = document.createElement('p');
    eventInfo.innerHTML = `Events: ${events.length}`;
    
    const pre = document.createElement('pre');
    pre.textContent = JSON.stringify(events, null, 2);
    
    const closeBtn = document.createElement('button');
    closeBtn.textContent = 'Close';
    closeBtn.onclick = () => overlay.remove();
    
    content.appendChild(title);
    content.appendChild(eventInfo);
    content.appendChild(pre);
    content.appendChild(closeBtn);
    
    overlay.appendChild(content);
    overlay.onclick = (e) => {
        if (e.target === overlay) overlay.remove();
    };
    
    document.body.appendChild(overlay);
}



function deleteWorkflow(idx) {
    const wf = workflows[idx];
    if (!wf) {
        console.error('Workflow not found at index', idx);
        return;
    }

    if (!confirm(`Delete "${wf.name}"? This cannot be undone.`)) return;

    chrome.runtime.sendMessage(
        { action: 'DELETE_WORKFLOW', id: wf.id },
        (res) => {
            if (res?.status === 'ok') {
                loadWorkflows();
            } else {
                alert('Failed to delete workflow');
            }
        }
    );
}


// ---------- Utils ----------
function escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
}
