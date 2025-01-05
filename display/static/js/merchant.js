document.addEventListener("DOMContentLoaded", () => {
  const updateProductForm = document.getElementById("updateProductForm");
  const updateModal = document.getElementById("updateModal");
  const closeUpdateModal = document.getElementById("closeUpdateModal");
  const merchantProductsContainer = document.getElementById("merchantProductsContainer");

  document.addEventListener("click", (event) => {
      if (event.target.classList.contains("update-product")) {
          const productId = event.target.getAttribute("data-product-id");

          fetch(`/api/products/${productId}/update`)
              .then((response) => {
                  if (!response.ok) {
                      throw new Error(`HTTP error! Status: ${response.status}`);
                  }
                  return response.json();
              })
              .then((product) => {
                  document.getElementById("updateProductName").value = product.name;
                  document.getElementById("updateProductPrice").value = product.price;
                  document.getElementById("updateProductDescription").value = product.description;
                  updateModal.setAttribute("data-product-id", productId);
                  updateModal.classList.remove("hidden");
              })
              .catch((error) => {
                  console.error("Error fetching product details:", error);
                  showNotification("Error", "Failed to fetch product details.");
              });
      }
  });

  document.getElementById("saveProductChanges").addEventListener("click", () => {
      const productId = updateModal.getAttribute("data-product-id");

      const name = document.getElementById("updateProductName").value.trim();
      const priceInput = document.getElementById("updateProductPrice").value.trim();
      const description = document.getElementById("updateProductDescription").value.trim();

      
      const price = parseFloat(priceInput);

      if (!name || !description) {
          showNotification("Error", "Name and Description cannot be empty.");
          return;
      }

      if (isNaN(price) || price <= 0) {
          showNotification("Error", "Price must be a positive number greater than zero.");
          return;
      }

      fetch(`/api/products/${productId}/update`, {
          method: "PUT",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({
              name: name,
              price: price,
              description: description,
          }),
      })
          .then((response) => {
              if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
          })
          .then((data) => {
              updateModal.classList.add("hidden");
              fetchMerchantProducts();
              showNotification("Success", "Product updated successfully!");
          })
          .catch((error) => {
              console.error("Error updating product:", error);
              showNotification("Error", "Failed to update product. Please try again.");
          });
  });

  closeUpdateModal.addEventListener("click", () => {
      updateModal.classList.add("hidden");
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
                      const imageUrl = product.image.includes('res.cloudinary.com')
                          ? product.image
                          : `https://res.cloudinary.com/dq8k7uqzw/${product.image.replace(/^image\/upload\//, '')}`;
  
                      const productCard = `
                          <div class="bg-white shadow-md rounded-lg overflow-hidden">
                              <a  class="block">
                                  <img 
                                      src="${imageUrl}" 
                                      alt="${product.name}" 
                                      class="w-full h-48 object-cover transition-transform duration-300 hover:scale-105" 
                                  />
                              </a>
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
  
  });
  