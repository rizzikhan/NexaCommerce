document.addEventListener("DOMContentLoaded", function () {
  const profileButton = document.getElementById("profileButton");
  const profileModal = document.getElementById("profileModal");
  const closeModal = document.getElementById("closeModal");
  const closeModalButton = document.getElementById("closeModalButton");
  const watchlistContainer = document.getElementById("watchlistContainer");

  profileButton.addEventListener("click", async () => {
      profileModal.classList.remove("hidden");

      try {
          const response = await fetch("/api/watchlist/", {
              method: "GET",
              headers: {
                  "Content-Type": "application/json",
              },
          });

          if (!response.ok) {
              throw new Error("Failed to fetch watchlist.");
          }

          const data = await response.json();
          console.log("Watchlist Data:", data.watchlist);

          watchlistContainer.innerHTML = "";

          if (data.watchlist.length === 0) {
              watchlistContainer.innerHTML = `<p class="text-gray-500">Your watchlist is empty.</p>`;
          } else {
              data.watchlist.forEach((item) => {
                  const productHTML = `
                      <div class="flex items-center justify-between border p-4 rounded-md">
                          <div class="flex items-center">
                              <img
                                  src="${item.product_image || '/static/images/no-image.png'}"
                                  alt="${item.product_name}"
                                  class="h-16 w-16 object-cover rounded-md"
                              />
                              <div class="ml-4">
                                  <p class="font-bold">${item.product_name}</p>
                                  <p class="text-blue-500">$${item.product_price}</p>
                              </div>
                          </div>
                          <div>
                              <button
                                  class="add-to-cart bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                                  data-product-id="${item.product_id}"
                              >
                                  Add to Cart
                              </button>
                          </div>
                      </div>
                  `;
                  watchlistContainer.innerHTML += productHTML;
              });
          }
      } catch (error) {
          console.error("Error fetching watchlist:", error);
          watchlistContainer.innerHTML = `<p class="text-red-500">Failed to load watchlist.</p>`;
      }
  });

  watchlistContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("add-to-cart")) {
          const productId = event.target.getAttribute("data-product-id");
          console.log("Add to Cart clicked for Product ID:", productId);
          addToCart(productId); 
      }
  });

  closeModal.addEventListener("click", () => {
      profileModal.classList.add("hidden");
  });

  closeModalButton.addEventListener("click", () => {
      profileModal.classList.add("hidden");
  });

  profileModal.addEventListener("click", (event) => {
      if (event.target === profileModal) {
          profileModal.classList.add("hidden");
      }
  });

  function addToCart(productId) {
      fetch("/api/cart/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({ product_id: productId, quantity: 1 }),
      })
          .then((response) => response.json())
          .then((data) => {
              console.log("Product added to cart:", data);
              showNotification("Success", "Product added to cart successfully!");

          })
          .catch((error) => {
              console.error("Error adding product to cart:", error);
              showNotification("error", "Failed to add product to cart. Please try again.");
          });
  }

  function getCSRFToken() {
      const cookieValue = document.cookie
          .split("; ")
          .find((row) => row.startsWith("csrftoken="))
          ?.split("=")[1];
      return cookieValue || "";
  }
});
