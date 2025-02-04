document.addEventListener("DOMContentLoaded", function() {
  var stripe = Stripe(document.getElementById('id_stripe_public_key').textContent);
  var elements = stripe.elements();

  var style = {
      base: {
          color: '#32325d',
          fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
          fontSmoothing: 'antialiased',
          fontSize: '16px',
          '::placeholder': {
              color: '#aab7c4'
          }
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
      showLoading(true);

      stripe.createToken(card).then(function(result) {
          if (result.error) {
              var errorElement = document.getElementById('card-errors');
              errorElement.textContent = result.error.message;
              showLoading(false);
          } else {
              stripeTokenHandler(result.token);
          }
      });
  });

  function stripeTokenHandler(token) {
      var form = document.getElementById('payment-form');
      var hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'stripeToken');
      hiddenInput.setAttribute('value', token.id);
      form.appendChild(hiddenInput);

      form.submit();
  }

  function showLoading(isLoading) {
      var loadingOverlay = document.getElementById('loading-overlay');
      if (isLoading) {
          loadingOverlay.style.display = 'block';
      } else {
          loadingOverlay.style.display = 'none';
      }
  }
});
