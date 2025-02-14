document.addEventListener("DOMContentLoaded", function() {
    var stripePublicKey = "{{ stripe_public_key }}";  
    var clientSecret = document.getElementById('id_client_secret').value;  

    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();

    // Define custom styling for the card element
    var style = {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            },
            border: '1px solid black'
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };

    var card = elements.create('card', {style: style});
    card.mount('#card-element');

    card.on('change', function(event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: document.getElementById('name').value  
                }
            }
        }).then(function(result) {
            if (result.error) {
                var displayError = document.getElementById('card-errors');
                displayError.textContent = result.error.message;
            } else {
                form.submit();
            }
        });
    });

    function showLoading(isLoading) {
        var loadingOverlay = document.getElementById('loading-overlay');
        if (isLoading) {
            loadingOverlay.style.display = 'block';
        } else {
            loadingOverlay.style.display = 'none';
        }
    }
});
