document.addEventListener('DOMContentLoaded', () => {
    const categoryButton = document.getElementById('categoriesButton');
    const categoryDropdown = document.getElementById('categoryDropdown');
    const categoryList = document.getElementById('categoryList');
    let categoriesLoaded = false;

    categoryButton.addEventListener('click', (event) => {
        event.stopPropagation(); 
        categoryDropdown.classList.toggle('hidden');

        if (!categoriesLoaded) {
            fetchCategories();
            categoriesLoaded = true;
        }
    });

    function fetchCategories() {
        fetch('/api/categories/')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to fetch categories');
                }
                return response.json();
            })
            .then((categories) => {
                categoryList.innerHTML = ''; 
                
                if (categories.length === 0) {
                    categoryList.innerHTML = `
                        <li class="px-4 py-2 text-gray-500">No categories available</li>
                    `;
                    return;
                }

                categories.forEach(category => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        <a href="/category/${category.id}/" class="block px-4 py-2 hover:bg-gray-100">
                            ${category.name}
                        </a>
                    `;
                    categoryList.appendChild(listItem);
                });
            })
            .catch((error) => {
                console.error('Error fetching categories:', error);
                categoryList.innerHTML = `
                    <li class="px-4 py-2 text-red-500">Error loading categories</li>
                `;
            });
    }

    document.addEventListener('click', (event) => {
        if (
            !categoryButton.contains(event.target) &&
            !categoryDropdown.contains(event.target)
        ) {
            categoryDropdown.classList.add('hidden');
        }
    });
});
