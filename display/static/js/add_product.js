document.addEventListener("DOMContentLoaded", () => {
    const addProductButton = document.getElementById("addProductButton");
    const addProductModal = document.getElementById("addProductModal");
    const closeAddProductModal = document.getElementById("closeAddProductModal");
    const addProductForm = document.getElementById("addProductForm");
    const merchantProductsContainer = document.getElementById("merchantProducts");
    const categoryDropdown = document.getElementById("productCategory");
    addProductButton.addEventListener("click", () => {
        addProductModal.classList.remove("hidden");
        setTimeout(fetchCategories, 100); 
    });

    closeAddProductModal.addEventListener("click", () => {
        addProductModal.classList.add("hidden");
    });

    function fetchCategories() {
        fetch("/api/categories/")
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch categories");
                }
                return response.json();
            })
            .then(categories => {
                console.log("Fetched categories:", categories);
                categoryDropdown.innerHTML = `<option value="" disabled selected>Select a Category</option>`;
                categories.forEach(category => {
                    const option = document.createElement("option");
                    option.value = category.id;
                    option.textContent = category.name;
                    categoryDropdown.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Error fetching categories:", error);
                showNotification("Error", "Failed to load categories");
            });
    }
    
    addProductForm.addEventListener("submit", (e) => {
        e.preventDefault();
    
        const formData = new FormData(addProductForm);
        const categoryId = document.getElementById("productCategory").value;
    
        if (!categoryId) {
            alert("Please select a category");
            return;
        }
    
        formData.append("category", categoryId);
    
        fetch("/api/products/add/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            body: formData,
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.product) {
                appendMerchantProduct(data.product); 
                showNotification("Success", "Product added successfully!");
            } else {
                console.error("No product data in the response.");
                showNotification("Warning", "Product added, but could not refresh view. Please reload the page.");
            }
    
            addProductModal.classList.add("hidden");
            addProductForm.reset(); 
        })
        .catch((error) => {
            console.error("Error adding product:", error);
            showNotification("Warning", "Failed to add product. Please try again!");
        });
    });
    
    function appendMerchantProduct(product) {
        let merchantProductsContainer = document.getElementById("merchantProducts");
    
        if (!merchantProductsContainer) {
            merchantProductsContainer = document.createElement("div");
            merchantProductsContainer.id = "merchantProducts";
            merchantProductsContainer.className = "grid grid-cols-3 sm:grid-cols-4 lg:grid-cols-5 gap-6 ml-5 mr-5";
            const header = document.createElement("h2");
            header.className = "text-2xl font-bold mb-6 mt-4 ml-5 mr-5";
            header.innerText = "Your Products";
            const parentContainer = document.querySelector("body"); 
            parentContainer.appendChild(header);
            parentContainer.appendChild(merchantProductsContainer);
        }
    
        const productCard = `
            <div class="bg-white shadow-md rounded-lg overflow-hidden">
                <a class="block">
                    ${
                        product.image.includes('res.cloudinary.com')
                            ? `<img 
                                  src="${product.image}" 
                                  alt="${product.name}" 
                                  class="w-full h-48 object-cover transition-transform duration-300 hover:scale-105" />`
                            : `<img 
                                  src="https://res.cloudinary.com/dq8k7uqzw/${product.image.replace(/^image\/upload\//, '')}" 
                                  alt="${product.name}" 
                                  class="w-full h-48 object-cover transition-transform duration-300 hover:scale-105" />`
                    }
                </a>
                <div class="p-4">
                    <h3 class="text-lg font-semibold">${product.name}</h3>
                    <p class="text-gray-500 text-sm">${product.description}</p>
                    <p class="text-blue-500 font-bold text-lg">$${product.price}</p>
                    <p class="text-sm text-green-600 font-medium mt-2">Category: ${
                        product.category ? product.category.name : 'No Category'
                    }</p>
                    <button
                        class="update-product bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mt-2"
                        data-product-id="${product.id}"
                    >
                        Update
                    </button>
                    <button
                        class="delete-product bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 mt-2"
                        data-product-id="${product.id}"
                    >
                        Delete
                    </button>
                </div>
            </div>
        `;
        merchantProductsContainer.insertAdjacentHTML("afterbegin", productCard);
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
