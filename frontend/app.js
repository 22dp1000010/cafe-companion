// Café Companion Frontend
const API_BASE = '';  // Relative to current domain
let currentUserId = 'user_001';

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const userIdInput = document.getElementById('userId');
const setUserBtn = document.getElementById('setUserBtn');
const refreshWaitBtn = document.getElementById('refreshWaitBtn');
const submitInterestsBtn = document.getElementById('submitInterestsBtn');
const interestsInput = document.getElementById('interestsInput');
const waitMinutes = document.getElementById('waitMinutes');
const queueSize = document.getElementById('queueSize');
const matchesDisplay = document.getElementById('matchesDisplay');
const orderSummary = document.getElementById('orderSummary');

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

setUserBtn.addEventListener('click', () => {
    currentUserId = userIdInput.value.trim() || 'user_001';
    addBotMessage(`User switched to ${currentUserId}`);
    refreshWaitTime();
    loadMatches();
});

refreshWaitBtn.addEventListener('click', refreshWaitTime);
submitInterestsBtn.addEventListener('click', submitInterests);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    refreshWaitTime();
    userIdInput.value = currentUserId;
});

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addUserMessage(message);
    chatInput.value = '';

    // Send to backend
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUserId,
                message: message,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            addBotMessage(`Error: ${error.detail || 'Failed to get response'}`);
            return;
        }

        const data = await response.json();

        // Add bot response
        addBotMessage(data.reply);

        // Show recommendation if present
        if (data.recommendation) {
            addBotMessage(`💡 ${data.recommendation}`);
        }

        // Show order confirmation if order intent detected
        if (data.order_intent && data.order_intent.items) {
            const items = data.order_intent.items.join(', ');
            const confirmMsg = `✅ Order received: ${items}`;
            const orderDiv = document.createElement('div');
            orderDiv.className = 'message bot-message order-confirmation';
            orderDiv.innerHTML = `<p>${confirmMsg}</p>`;
            chatMessages.appendChild(orderDiv);

            // Update order summary
            updateOrderSummary(data.order_intent.items);
        }

        // Refresh wait time after order
        if (data.order_intent) {
            setTimeout(refreshWaitTime, 500);
        }
    } catch (error) {
        addBotMessage(`Network error: ${error.message}`);
    }
}

function addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'message user-message';
    div.innerHTML = `<p>${escapeHtml(text)}</p>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(text) {
    const div = document.createElement('div');
    div.className = 'message bot-message';
    div.innerHTML = `<p>${escapeHtml(text)}</p>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function refreshWaitTime() {
    try {
        const response = await fetch(`${API_BASE}/api/wait-time`);
        if (!response.ok) {
            const error = await response.json();
            waitMinutes.textContent = 'N/A';
            queueSize.textContent = '0';
            return;
        }

        const data = await response.json();
        waitMinutes.textContent = data.estimated_wait_minutes;
        queueSize.textContent = data.queue_size;
    } catch (error) {
        console.error('Failed to fetch wait time:', error);
        waitMinutes.textContent = 'N/A';
    }
}

async function submitInterests() {
    const interests = interestsInput.value
        .split(',')
        .map((i) => i.trim())
        .filter((i) => i.length > 0);

    if (interests.length === 0) {
        alert('Please enter at least one interest');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/interests`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUserId,
                interests: interests,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.detail || 'Failed to submit interests'}`);
            return;
        }

        const data = await response.json();
        addBotMessage(`📍 Interests updated! Found ${data.matches_found} matching café friends!`);
        loadMatches();
    } catch (error) {
        alert(`Network error: ${error.message}`);
    }
}

async function loadMatches() {
    try {
        const response = await fetch(`${API_BASE}/api/matches/${currentUserId}`);
        if (!response.ok) return;

        const data = await response.json();
        const matches = data.matches || [];

        matchesDisplay.innerHTML = '';

        if (matches.length === 0) {
            matchesDisplay.innerHTML = '<p id="noMatches" style="color: #666; font-size: 0.9em;">No matches yet</p>';
            return;
        }

        matches.forEach((match) => {
            const div = document.createElement('div');
            div.className = 'match-item';
            const commonTags = match.common_interests
                ? match.common_interests.join(', ')
                : 'shared interests';
            div.innerHTML = `
                <strong>${match.matched_user_name || 'Café Friend'}</strong>
                <div class="match-tags">📌 ${commonTags}</div>
                <div class="match-score">Score: ${(match.score * 100).toFixed(0)}%</div>
            `;
            matchesDisplay.appendChild(div);
        });
    } catch (error) {
        console.error('Failed to load matches:', error);
    }
}

function updateOrderSummary(items) {
    orderSummary.innerHTML = '';
    items.forEach((item) => {
        const div = document.createElement('div');
        div.className = 'order-item';
        div.innerHTML = `
            <strong>🛍️ ${item}</strong>
            <small>Status: Queued</small>
        `;
        orderSummary.appendChild(div);
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
