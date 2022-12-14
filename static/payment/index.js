//'use strict',https://stripe.com/docs/payments/quickstart;
//import stripe in views

var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);

var elem = document.getElementById('submit'); // finding sumbmit button
clientsecret = elem.getAttribute('data-secret'); //data-secret created by stripe for each user

// Set up Stripe.js and Elements to use in checkout form (pre formated elements)
var elements = stripe.elements();
// jss not css
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};


var card = elements.create("card", { style: style });
card.mount("#card-element");
//error on top of the payment
card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
ev.preventDefault();

var custName = document.getElementById("custName").value;
var custAdd = document.getElementById("custAdd").value;
var custAdd2 = document.getElementById("custAdd2").value;
var postCode = document.getElementById("postCode").value;

//sending server to inform about started the payment using clintsecret order_key to data base and payment succeeded payment status to true
$.ajax({
  type: "POST",
  url: 'http://127.0.0.1:8000/orders/add/', //post data
  data: {
    order_key: clientsecret,
    csrfmiddlewaretoken: CSRF_TOKEN, //data sending according to this defined in order key in order class session data    csrfmiddlewaretoken: CSRF_TOKEN,//csrf tokken from home.html post method
    action: "post",
  },
  success: function (json) {
    console.log(json.success)

      //to confirm ordersending data to stripe 
      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:custAdd,
                line2:custAdd2
            },
            name: custName
          },
        }
      }).then(function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });
    },
    error: function (xhr, errmsg, err) {},
  });



});

