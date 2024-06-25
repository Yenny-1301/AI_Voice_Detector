document.addEventListener("DOMContentLoaded", function (event) {
    document.getElementById('audio-form').addEventListener('submit', async function (event) {
        event.preventDefault();
        const fileInput = document.getElementById('audio-file');
        if (fileInput.files.length === 0) {
            alert('Por favor, sube un archivo de audio.');
            return;
        }

        button = document.querySelector('button[type=submit]');
        let resultBox = document.getElementById('result-container');

        resultBox.innerHTML= "";
        resultBox.classList.remove('success', 'warning');
        originalContent = button.innerText;
        button.innerText= ""; 
        
        span = document.createElement('span');
        span.classList.add('spinner-border');
        span.classList.add('spinner-border-sm');

        button.appendChild(span);
        
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:8000/predict/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Error en la predicción');
            }

            const result = await response.json();
            
            let successContent = `<span id="header">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                    <path d="m10.97 4.97-.02.022-3.473 4.425-2.093-2.094a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05"/>
                </svg>
                Es probable este audio sea autentico
            </span> El origen del audio no parece haber sido generado con inteligencia artificial.
            Nuestro sistema no ha detectado indicios claros de manipulación mediante IA.
            Se recomienda seguir verificando la autenticidad del contenido.`;

            let warningContent = `<span id="header">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                    <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
                </svg>
                Es probable este audio sea generado con AI
            </span> El audio analizado parece haber sido generado con inteligencia artificial.
            Nuestro sistema ha identificado patrones característicos que sugieren su origen 
            artificial.`;

            let p = document.createElement('p');
            p.innerHTML = result == 1 ? successContent : warningContent;

            let resultBox = document.getElementById('result-container');
            resultBox.classList.add(result == 1 ? 'success' : 'warning');
            resultBox.appendChild(p);

            button.removeChild(span);
            button.innerText = originalContent;

        } catch (error) {
            document.getElementById('result-container').innerText = `Error`;
        }
    });
});