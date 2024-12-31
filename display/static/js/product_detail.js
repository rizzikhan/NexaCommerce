document.addEventListener("DOMContentLoaded", () => {
    const commentsContainer = document.getElementById("comments-container");
    const addCommentForm = document.getElementById("add-comment-form");
    const toggleWatchlist = document.getElementById("toggle-watchlist");

    async function loadComments() {
        const response = await fetch(window.location.pathname + "comments/");
        const data = await response.json();
        commentsContainer.innerHTML = "";

        if (data.comments.length === 0) {
            commentsContainer.innerHTML = "<p class='text-gray-500'>No comments yet. Be the first to comment!</p>";
        } else {
            data.comments.forEach(comment => {
                const commentHTML = `
                    <div class="border p-4 rounded-md">
                        <p class="font-semibold">${comment.user}</p>
                        <p>${comment.comment_text}</p>
                        <p class="text-sm text-gray-500">${comment.created_at}</p>
                        <p class="text-yellow-500">Rating: ${comment.rating} / 5</p>
                    </div>
                `;
                commentsContainer.innerHTML += commentHTML;
            });
        }
    }

    addCommentForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(addCommentForm);
        const response = await fetch(window.location.pathname, {
            method: "POST",
            body: formData,
        });
        if (response.ok) {
            loadComments();
            addCommentForm.reset();
        } else {
            alert("Failed to add comment.");
        }
    });

    toggleWatchlist.addEventListener("click", async () => {
        const productId = toggleWatchlist.dataset.productId;
        const response = await fetch("/api/watchlist/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ product_id: productId }),
        });
        const data = await response.json();
        if (data.success) {
            toggleWatchlist.classList.toggle("text-red-500");
            toggleWatchlist.classList.toggle("text-gray-500");
        }
    });

    loadComments();
});
