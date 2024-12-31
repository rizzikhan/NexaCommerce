const stripe = Stripe("pk_test_51QVznhLNMLN2YT09jSLF7OaHQOMtOBcm6wLth49uy13QEpc9T6d2MXkVTqb7RwBdjLptdGt1NeGtm8WKogRcVx1z00sf2SfliC");

fetch("/api/cart/create-checkout-session/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
    },
})
    .then((response) => {
        if (!response.ok) {
            throw new Error("Failed to create checkout session.");
        }
        return response.json();
    })
    .then((data) => {
        if (data.sessionId) {
            stripe.redirectToCheckout({ sessionId: data.sessionId });
        } else {
            console.error("No session ID returned:", data);
        }
    })
    .catch((error) => console.error("Error creating checkout session:", error));
