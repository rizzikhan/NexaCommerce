document.addEventListener('DOMContentLoaded', () => {
    const filterButton = document.getElementById('filterButton');
    const filterSidebar = document.getElementById('filterSidebar');
    const closeFilterSidebar = document.getElementById('closeFilterSidebar');
    const categoryFilter = document.getElementById('categoryFilter');
    const priceMin = document.getElementById('priceMin');
    const priceMax = document.getElementById('priceMax');
    const stockFilter = document.getElementById('stockFilter');
    const sortFilter = document.getElementById('sortFilter');
    const applyFilters = document.getElementById('applyFilters');
    const clearFilters = document.getElementById('clearFilters');
    const productContainer = document.getElementById('productContainer');

    filterButton.addEventListener('click', () => {
        filterSidebar.classList.remove('hidden');
    });

    closeFilterSidebar.addEventListener('click', () => {
        filterSidebar.classList.add('hidden');
    });

    function fetchCategories() {
        fetch('/api/categories/')
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch categories');
                return response.json();
            })
            .then(categories => {
                categoryFilter.innerHTML = '<option value="">All Categories</option>';
                categories.forEach(category => {
                    categoryFilter.innerHTML += `<option value="${category.id}">${category.name}</option>`;
                });
            })
            .catch(error => console.error('❌ Error fetching categories:', error));
    }

    function applyFiltersOnCurrentView() {
        const params = new URLSearchParams();
        if (priceMin.value) params.append('price_min', priceMin.value);
        if (priceMax.value) params.append('price_max', priceMax.value);
        if (categoryFilter.value) params.append('category', categoryFilter.value);
        if (stockFilter.value) params.append('in_stock', stockFilter.value);
        if (sortFilter.value) params.append('sort', sortFilter.value);
    
        console.log('Applying Filters:', params.toString()); 
    
        fetch(`/api/filterproducts/?${params.toString()}`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch filtered products');
                return response.json();
            })
            .then(data => {
                console.log('Filtered Data:', data); 
    
                productContainer.querySelectorAll('.product-card').forEach(card => {
                    card.classList.add('hidden');
                });
    
                const productOrder = data.products.map(product => product.id); 
    
                productOrder.forEach(productId => {
                    const productCard = productContainer.querySelector(`[data-product-id="${productId}"]`);
                    if (productCard) {
                        productCard.classList.remove('hidden');
                        productContainer.appendChild(productCard);
                    }
                });
            })
            .catch(error => console.error('❌ Error applying filters:', error));
    }
    

    clearFilters.addEventListener('click', () => {
        priceMin.value = '';
        priceMax.value = '';
        categoryFilter.value = '';
        stockFilter.value = '';
        sortFilter.value = '';

        productContainer.querySelectorAll('.product-card').forEach(card => {
            card.classList.remove('hidden');
        });
    });

    applyFilters.addEventListener('click', () => {
        applyFiltersOnCurrentView();
        filterSidebar.classList.add('hidden');
    });

    fetchCategories();
});
