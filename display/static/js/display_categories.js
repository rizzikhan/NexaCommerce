document.addEventListener('DOMContentLoaded', () => {
    const categoriesContainer = document.getElementById('categoriesContainer');

    function fetchCategories() {
        fetch('/api/categories/')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to fetch categories');
                }
                return response.json();
            })
            .then((categories) => {
                categoriesContainer.innerHTML = '';

                if (categories.length === 0) {
                    categoriesContainer.innerHTML = `
                        <p class="text-gray-500">No categories available</p>
                    `;
                    return;
                }

                categories.forEach(category => {
                    const categoryItem = document.createElement('div');
                    categoryItem.className = 'flex flex-col items-center text-center';

                    categoryItem.innerHTML = `
                        <a href="/category/${category.id}/" 
                           class="w-24 h-24 flex items-center justify-center rounded-full bg-yellow-200 hover:bg-yellow-300 shadow-md transition duration-300">
                            <span class="text-gray-800 font-semibold">${category.name}</span>
                        </a>
                        <span class="text-sm mt-2">${category.name}</span>
                    `;
                    
                    categoriesContainer.appendChild(categoryItem);
                });
            })
            .catch((error) => {
                console.error('Error fetching categories:', error);
                categoriesContainer.innerHTML = `
                    <p class="text-red-500">Failed to load categories</p>
                `;
            });
    }

    fetchCategories();
});
