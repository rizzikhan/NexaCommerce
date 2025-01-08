document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.querySelector("#searchBar");
  const productContainer = document.querySelector("#productContainer");

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim();
    if (query) {
      fetch(`/api/products/?search=${query}`)
        .then((response) => response.json())
        .then((data) => {
          productContainer.innerHTML = "";
          if (data.length === 0) {
            productContainer.innerHTML = "<p>No products found.</p>";
          } else {
            data.forEach((product) => {

              


const productCard = `
  <div class=" bg-purple-100 shadow-md rounded-lg outline-none overflow-hidden">
    <a href="http://127.0.0.1:8000/api/products/${product.id}/detailpage" class="block rounded-lg outline-none">
      ${
        product.image.includes('res.cloudinary.com')
          ? `<img 
              src="${product.image}" 
              alt="${product.name}" 
              class="w-full h-48 bg-gray-200 flex items-center justify-center text-gray-500" />`
          : `<img 
              src="https://res.cloudinary.com/dq8k7uqzw/${product.image.replace(/^image\/upload\//, '')}" 
              alt="${product.name}" 
              class="w-full h-48 bg-gray-200 flex items-center justify-center text-gray-500" />`
      }
    </a>
    <div class="p-4">
      <h3 class="block bg-purple-200 rounded text-lg font-semibold text-black-300">${product.name}</h3>
      <p class="text-gray-500 text-sm bg-purple-100 rounded">${product.description}</p>
      <p class="text-blue-500 font-bold text-lg bg-purple-100 rounded">$${product.price}</p>

      </div>
  </div>
`;

productContainer.insertAdjacentHTML("beforeend", productCard);

            
            
            });
          }
        })
        .catch((error) => console.error("Error fetching products:", error));
    } else {
      productContainer.innerHTML = "<p>Start typing to search products...</p>";
    }
  });
});
