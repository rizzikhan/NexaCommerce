document.addEventListener("DOMContentLoaded", () => {
  const addToCartButtons = document.querySelectorAll(".add-to-cart");
  const cartButton = document.getElementById("cartButton");
  const cartModal = document.getElementById("cartModal");
  const closeCartModal = document.getElementById("closeCartModal");
  const cartItemsContainer = document.getElementById("cartItems");

  addToCartButtons.forEach((button) => {
      button.addEventListener("click", () => {
          const productId = button.getAttribute("data-product-id");
          console.log("Add to Cart clicked for Product ID:", productId);

          const quantityInput = document.querySelector(
              `.quantity-input[data-product-id="${productId}"]`
          );

          const quantity = quantityInput ? parseInt(quantityInput.value, 10) : 1;
          const stock = parseInt(quantityInput.getAttribute("max"), 10); 

          if (isNaN(quantity) || quantity <= 0) {
              showNotification("Error", "Quantity must be a positive number.");
              return;
          }

          if (quantity > stock) {
              showNotification("Error", "Quantity exceeds available stock.");
              return;
          }

          fetch("/api/cart/", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": getCSRFToken(),
              },
              body: JSON.stringify({ product_id: productId, quantity: quantity }),
          })
              .then((response) => {
                  if (!response.ok) {
                      throw new Error(`HTTP error! Status: ${response.status}`);
                  }
                  return response.json();
              })
              .then((data) => {
                  showNotification("Success", "Product added to cart successfully!");
                  console.log("Product added to cart response:", data);
              })
              .catch((error) => {
                  console.error("Error adding product to cart:", error);
                  showNotification("Error", "Failed to add product to cart.");
              });
      });
  });
  cartButton.addEventListener("click", () => {
    fetchCartItems();
    cartModal.classList.remove("hidden");
  });


  closeCartModal.addEventListener("click", () => {
    cartModal.classList.add("hidden");
  });

  function fetchCartItems() {
    fetch("/api/cart/")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Cart data:", data);
        cartItemsContainer.innerHTML = ""; 

        if (data.length === 0) {
          cartItemsContainer.innerHTML = "<p>Your cart is empty.</p>";
          return;
        }

        data.forEach((item) => {
          const cartItem = `
            <div class="flex justify-between items-center mb-4">
              <span>${item.product_name}</span>
              <span>$${item.product_price}</span>
              <span>Qty: ${item.quantity}</span>
              <button
                class="remove-from-cart text-red-500 hover:text-red-700"
                data-cart-id="${item.id}"
              >
                Remove
              </button>
            </div>
          `;
          cartItemsContainer.insertAdjacentHTML("beforeend", cartItem);

        });

        attachRemoveButtons(); 
        
      })
      .catch((error) => console.error("Error fetching cart items:", error));
  }


  function attachRemoveButtons() {
    const removeButtons = document.querySelectorAll(".remove-from-cart");
  
    removeButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const cartId = button.getAttribute("data-cart-id");
        console.log(`Clicked Remove for Cart ID: ${cartId}`);
  
        fetch(`/api/cart/${cartId}/`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log(`Item ${cartId} removed from cart`);
            showNotification("error", "Product deleted successfully!");
            fetchCartItems();
          })
          .catch((error) => console.error("Error removing item:", error));
      });
    });
  }
  cartModal.addEventListener("click", (event) => {
    if (event.target === cartModal) {
      cartModal.classList.add("hidden");
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
});
