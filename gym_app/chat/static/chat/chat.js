let socket;
const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const groupSelect = document.getElementById('group-select');

// Conecta al WebSocket usando el grupo seleccionado
function connectWebSocket(groupName) {
    if (!groupName) {
        console.error("No se ha seleccionado ningún grupo.");
        return;
    }

    if (socket) socket.close();

    socket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + groupName + '/');

    socket.onopen = () => {
        console.log("Conectado al WebSocket del grupo:", groupName);
    };

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const msg = document.createElement('div');
        msg.classList.add('mb-2');
        msg.innerHTML = `<span style="color: #333;">${data.message}</span>`;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    socket.onerror = function (e) {
        console.error("Error en WebSocket:", e);
    };

    socket.onclose = function (e) {
        console.warn("WebSocket cerrado:", e);
    };
}

// Cambia de grupo dinámicamente
groupSelect.onchange = () => {
    chatBox.innerHTML = '';
    connectWebSocket(groupSelect.value);
};

// Envía el mensaje al WebSocket
chatForm.onsubmit = function (e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (message === "") return;

    socket.send(JSON.stringify({ 'message': message }));

    const userMsg = document.createElement('div');
    userMsg.classList.add('mb-2');
    userMsg.innerHTML = `<strong style="color: #007bff;">Tú:</strong> ${message}`;
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    chatInput.value = '';
};

window.onload = () => {
    const groupSelect = document.getElementById('group-select');
    if (groupSelect) {
        const initialGroup = groupSelect.value;
        if (initialGroup) {
            connectWebSocket(initialGroup);
        }
    } else {
        console.warn("No se encontró el selector de grupo.");
    }
};
