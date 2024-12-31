document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".watchlist-toggle").forEach((button) => {
        button.addEventListener("click", async function () {
            const productId = button.getAttribute("data-product-id");
            console.log("Product ID:", productId);

            try {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const response = await fetch(`/watchlist/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                    },
                    body: JSON.stringify({ product_id: productId }),
                });

                const data = await response.json();
                if (response.ok) {
                    const svg = button.querySelector("svg");
                    if (data.in_watchlist) {
                        svg.classList.add("text-red-500");
                        svg.classList.remove("text-gray-500");
                        showNotification("Success", "Added to watchlist ");
                    } else {
                        svg.classList.add("text-gray-500");
                        svg.classList.remove("text-red-500");
                        showNotification("error", "Removed from watchlist!");

                    }
                } else {
                    console.error("Error from backend:", data);
                }
            } catch (error) {
                console.error("Error toggling watchlist:", error);
                alert("An error occurred. Please try again.");
            }
        });
    });
});
