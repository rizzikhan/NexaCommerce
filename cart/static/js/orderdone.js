

document.addEventListener("DOMContentLoaded", function () {
    const ordersButton = document.getElementById("ordersButton");
    const ordersModal = document.getElementById("ordersModal");
    const ordersList = document.getElementById("ordersList");
    
    ordersButton.addEventListener("click", async function () {
        ordersModal.classList.remove("hidden");

        try {
            const response = await fetch("/api/cart/orders/", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("Failed to fetch orders.");
            }

            const data = await response.json();

            ordersList.innerHTML = "";

            if (data.orders.length === 0) {
                ordersList.innerHTML = `<p class="text-gray-500">No orders found.</p>`;
            } else {
                data.orders.forEach((order) => {
                    const orderHTML = `
                        <div class="border p-4 rounded-md shadow-sm">
                            <p><strong>Order ID:</strong> ${order.id}</p>
                            <p><strong>Total Amount:</strong> $${order.total_amount}</p>
                            <p><strong>Order Date:</strong> ${order.created_at}</p>
                            <p><strong>Payment Intent ID:</strong> ${order.intent}</p>
                            <ul class="mt-2">
                                ${order.products
                                    .map(
                                        (product) =>
                                            `<li>${product.name} - Qty: ${product.quantity} - $${product.price}</li>`
                                    )
                                    .join("")}
                            </ul>
                            <button
                                class="mt-2 ${
                                    order.is_refunded
                                        ? "bg-gray-500 text-white cursor-not-allowed"
                                        : "bg-red-500 text-white refund-button"
                                } px-3 py-1 rounded"
                                data-order-id="${order.id}"
                                data-intent-id="${order.intent}"
                                ${order.is_refunded ? "disabled" : ""}
                            >
                                ${order.is_refunded ? "Refunded" : "Cancel & Refund"}
                            </button>
                        </div>
                    `;
                    ordersList.innerHTML += orderHTML;
                });

                document.querySelectorAll(".refund-button").forEach((button) => {
                    button.addEventListener("click", async function () {
                        const orderId = button.getAttribute("data-order-id");
                        const intentId = button.getAttribute("data-intent-id");

                        try {
                            const csrfToken = getCSRFToken();
                            console.log("csrfToken")
                            console.log(csrfToken)
                            console.log("orderId")
                            console.log(orderId)
                            console.log("intentId")
                            console.log(intentId)

                            const refundResponse = await fetch("/api/cart/refund/", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                    "X-CSRFToken": csrfToken,
                                },
                                credentials: "include",
                                body: JSON.stringify({
                                    order_id: orderId,
                                    intent_id: intentId,
                                }),
                            });
                            console.log("refundResponse")
                            console.log(refundResponse)

                            const refundData = await refundResponse.json();

                            if (refundResponse.ok || refundData.message === "Refund processed successfully.") {
                                showNotification("Success", "Refund processed successfully.");
                                button.innerText = "Refunded";
                                button.classList.remove("bg-red-500");
                                button.classList.add("bg-gray-500", "cursor-not-allowed");
                                button.disabled = true;
                            } else {
                                const errorMessage = refundData.error || "Refund could not be processed.";
                                throw new Error(errorMessage);
                            }
                        } catch (error) {
                            console.error("Refund error:", error);
                            setTimeout(() => location.reload(), 2000);
                            showNotification("error", "Either already refunded or Refund could not be processed. Please try again later.");

                        }
                    });
                });
            }
        } catch (error) {
            console.error("Error fetching orders:", error);
            ordersList.innerHTML = `<p class="text-red-500">Failed to load orders.</p>`;
        }
    });



    ordersModal.addEventListener("click", function (event) {
        if (event.target === ordersModal) {
            ordersModal.classList.add("hidden");
        }
    });
});
function getCSRFToken() {
    let cookieValue = null;
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
            cookieValue = cookie.substring(name.length + 1);
            break;
        }
    }
    return cookieValue;
}