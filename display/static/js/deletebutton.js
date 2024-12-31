document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById("deleteConfirmationModal");
    const confirmDeleteButton = document.getElementById("confirmDeleteButton");
    const cancelDeleteButton = document.getElementById("cancelDeleteButton");
    const closeDeleteButton = document.getElementById("closeDeleteConfirmationModal");

    let productIdToDelete = null;

    document.body.addEventListener("click", (event) => {
        if (event.target.classList.contains("delete-product")) {
            productIdToDelete = event.target.getAttribute("data-product-id"); 
            deleteModal.classList.remove("hidden"); 
        }
    });

    confirmDeleteButton.addEventListener("click", () => {
        if (productIdToDelete) {
            deleteProduct(productIdToDelete); 
            fetchMerchantProducts()
            showNotification("error", "Product deleted successfully!");

        }
    });

    cancelDeleteButton.addEventListener("click", () => {
        deleteModal.classList.add("hidden"); 
        productIdToDelete = null; 
    });

    closeDeleteButton.addEventListener("click", () => {
        deleteModal.classList.add("hidden"); 
        productIdToDelete = null; 
    });

    function deleteProduct(productId) {
        fetch(`/api/products/${productId}/delete`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
        })
            .then((response) => {
                if (response.status === 204) {
                    console.log(`Product with ID ${productId} deleted successfully.`);
                    deleteModal.classList.add("hidden");
                    productIdToDelete = null; 
                    fetchMerchantProducts(); 
                } else {
                    return response.json().then((data) => {
                        throw new Error(data.error || "Failed to delete the product.");
                    });
                }
            })
            .catch((error) => console.error("Error deleting product:", error));
    }

    function fetchMerchantProducts() {
        fetch("/api/merchant-products/")
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                const container = document.getElementById("merchantProducts");
                container.innerHTML = ""; 
    
                if (data.length === 0) {
                    container.innerHTML = "<p>No products to show.</p>";
                } else {
                    data.forEach((product) => {
                        const productCard = `
                            <div class="bg-white shadow-md rounded-lg overflow-hidden">
                                <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover" />
                                <div class="p-4">
                                    <h3 class="text-lg font-semibold">${product.name}</h3>
                                    <p class="text-gray-500 text-sm">${product.description}</p>
                                    <p class="text-blue-500 font-bold text-lg">$${product.price}</p>
                                    <button
                                        class="update-product bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                                        data-product-id="${product.id}"
                                    >
                                        Update
                                    </button>
                                    <button
                                        class="delete-product bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                                        data-product-id="${product.id}"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        `;
                        container.insertAdjacentHTML("beforeend", productCard);
                    });
                }
            })
            .catch((error) => console.error("Error fetching merchant products:", error));
    }

    
    function getCSRFToken() {
        const cookies = document.cookie.split("; ");
        for (const cookie of cookies) {
            if (cookie.startsWith("csrftoken=")) {
                return cookie.split("=")[1];
            }
        }
        return null;
    }


    
});
