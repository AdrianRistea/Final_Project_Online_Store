document.addEventListener('DOMContentLoaded', function () {
    const proceedToPaymentButton = document.getElementById('proceedToPayment');

    proceedToPaymentButton.addEventListener('click', function (event) {
        event.preventDefault(); // Opriți comportamentul implicit al linkului

        console.log('Button clicked'); // Verificați dacă butonul este detectat

        // Afișați mesajul
        const messageElement = document.createElement('div');
        messageElement.className = 'alert alert-success';
        messageElement.textContent = 'Plata a fost realizată cu succes!';
        document.body.appendChild(messageElement);

        // Așteptați 1 secundă înainte de a elimina mesajul
        setTimeout(function () {
            messageElement.remove();
            console.log('Message removed'); // Verificați dacă mesajul este eliminat
        }, 1000); // Așteptați 1 secundă înainte de a elimina mesajul
    });
});
