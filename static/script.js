document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("exchange-form");
    
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const amount = document.getElementById("amount").value;
        const fromCurrency = document.getElementById("from-currency").value;
        const toCurrency = document.getElementById("to-currency").value;
        const data = {
            amount: amount,
            from: fromCurrency,
            to: toCurrency
        };

        fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                document.getElementById("converted-amount").textContent = data.converted_amount.toFixed(2);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});