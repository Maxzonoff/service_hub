/* Service Hub — чат заказа (polling раз в 5 секунд) */

document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('chatOrderSelect');
    const messages = document.getElementById('chatMessages');
    const form = document.getElementById('chatForm');
    const input = document.getElementById('chatInput');
    if (!select || !form) return;

    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrf = csrfInput ? csrfInput.value : '';
    let currentOrderId = null;
    let pollTimer = null;

    select.addEventListener('change', () => {
        currentOrderId = select.value;
        if (!currentOrderId) {
            messages.innerHTML = '<p class="text-muted text-center">Выберите заказ</p>';
            form.classList.add('d-none');
            return;
        }
        form.classList.remove('d-none');
        loadMessages();
        if (pollTimer) clearInterval(pollTimer);
        pollTimer = setInterval(loadMessages, 5000);
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text || !currentOrderId) return;

        const fd = new FormData();
        fd.append('text', text);

        try {
            const res = await fetch(`/orders/${currentOrderId}/message/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrf },
                body: fd,
            });
            if (res.ok) {
                input.value = '';
                loadMessages();
            } else {
                alert('Не удалось отправить сообщение');
            }
        } catch (err) {
            console.error(err);
        }
    });

    async function loadMessages() {
        if (!currentOrderId) return;
        try {
            const res = await fetch(`/orders/${currentOrderId}/messages/`);
            const data = await res.json();
            messages.innerHTML = '';

            if (!data.messages.length) {
                messages.innerHTML = '<p class="text-muted text-center">Начните общение</p>';
                return;
            }

            data.messages.forEach(m => {
                const div = document.createElement('div');
                div.className = 'chat-message ' + (m.is_admin ? 'from-admin' : 'from-client');
                div.innerHTML = `${escapeHtml(m.text)}<time>${m.created_at}</time>`;
                messages.appendChild(div);
            });
            messages.scrollTop = messages.scrollHeight;
        } catch (err) {
            console.error(err);
        }
    }

    function escapeHtml(str) {
        return String(str).replace(/[&<>"']/g, c => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[c]));
    }
});