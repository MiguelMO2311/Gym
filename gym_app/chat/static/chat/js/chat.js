let socket;
const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const groupSelect = document.getElementById('group-select');

// Detecta protocolo seguro si estás en HTTPS
function getWebSocketProtocol() {
    return window.location.protocol === 'https:' ? 'wss://' : 'ws://';
}

// Conecta al WebSocket usando el grupo seleccionado
function connectWebSocket(groupName) {
    if (!groupName || typeof groupName !== 'string') {
        console.error("❌ Grupo inválido:", groupName);
        return;
    }

    // Cierra conexión anterior si existe
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close(1000, "Cambio de grupo");
    }

    const protocol = getWebSocketProtocol();
    const socketUrl = `${protocol}${window.location.host}/ws/chat/${groupName}/`;
    console.log("🔄 Conectando a:", socketUrl);

    socket = new WebSocket(socketUrl);

    socket.onopen = () => {
        console.log("✅ Conectado al WebSocket del grupo:", groupName);
    };

    socket.onmessage = function (e) {
        try {
            const data = JSON.parse(e.data);
            const msg = document.createElement('div');
            msg.classList.add('mb-2');
            msg.innerHTML = `<span style="color: #333;">${data.message}</span>`;
            chatBox.appendChild(msg);
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (err) {
            console.error("❌ Error al procesar mensaje:", err);
        }
    };

    socket.onerror = function (e) {
        console.error("❌ Error en WebSocket:", e);
    };

    socket.onclose = function (e) {
        console.warn(`⚠️ WebSocket cerrado (código ${e.code}):`, e.reason || 'Sin motivo');
    };
}

// Cambia de grupo dinámicamente
groupSelect.onchange = () => {
    const selectedGroup = groupSelect.value;
    if (!selectedGroup) {
        console.warn("⚠️ Grupo seleccionado vacío.");
        return;
    }
    chatBox.innerHTML = '';
    connectWebSocket(selectedGroup);
};

// Envía el mensaje al WebSocket
chatForm.onsubmit = function (e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.warn("⚠️ WebSocket no disponible. Estado:", socket?.readyState);
        return;
    }

    socket.send(JSON.stringify({ message }));

    const userMsg = document.createElement('div');
    userMsg.classList.add('mb-2');
    userMsg.innerHTML = `<strong style="color: #007bff;">Tú:</strong> ${message}`;
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    chatInput.value = '';
};

// Inicializa el WebSocket al cargar la página
window.onload = () => {
    if (groupSelect && groupSelect.options.length > 0) {
        const initialGroup = groupSelect.value;
        if (initialGroup) {
            connectWebSocket(initialGroup);
        } else {
            console.warn("⚠️ El grupo inicial está vacío.");
        }
    } else {
        console.warn("⚠️ No hay opciones de grupo disponibles.");
    }
};
