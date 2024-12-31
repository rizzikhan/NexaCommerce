document.addEventListener("DOMContentLoaded", () => {
    const commentsContainer = document.getElementById("comments-container");
    const addCommentForm = document.getElementById("add-comment-form");
    const toggleCommentsButton = document.getElementById("toggle-comments");
    const productIdElement = document.querySelector(".add-to-cart");

    if (!productIdElement) {
        console.error("Product ID not found on the page.");
        return;
    }

    const productId = productIdElement.getAttribute("data-product-id");
    console.log("Product ID:", productId);

    function loadComments() {
        fetch(`/products/${productId}/comments/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Error fetching comments: ${response.status}`);
                }
                return response.json();
            })
            .then((comments) => {
                commentsContainer.innerHTML = "";
                comments.forEach((comment) => {
                    const commentElement = `
                        <div class="border p-4 rounded-lg">
                            <h4 class="font-bold">${comment.user}</h4>
                            <p>${comment.comment}</p>
                            <span class="text-yellow-500">Rating: ${comment.rating}</span>
                            <span class="text-gray-500 text-sm">(${comment.created_at})</span>
                        </div>
                    `;
                    commentsContainer.insertAdjacentHTML("beforeend", commentElement);
                });
            })
            .catch((error) => console.error("Error fetching comments:", error));
    }


    if (toggleCommentsButton) {
        toggleCommentsButton.addEventListener("click", () => {
            commentsContainer.classList.toggle("hidden");
            if (commentsContainer.classList.contains("hidden")) {
                toggleCommentsButton.textContent = "Show Comments";
            } else {
                toggleCommentsButton.textContent = "Hide Comments";
                loadComments(); 
            }
        });
    }

    loadComments();

    if (addCommentForm) {
        addCommentForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const comment = this.querySelector("textarea[name='comment']").value;
            const rating = this.querySelector("input[name='rating']").value;

            fetch(`/products/${productId}/add-comment/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({
                    comment: comment,
                    rating: rating,
                }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Error adding comment: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    showNotification("Success", "Comment added successfully!");
                    this.reset(); 
                    loadComments(); 
                })
                .catch((error) => console.error("Error adding comment:", error));
        });
    }
});

function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        if (cookie.startsWith("csrftoken=")) {
            return cookie.split("=")[1];
        }
    }
    return null;
}
