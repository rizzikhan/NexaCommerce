let currentIndex = 0;
const carouselContainer = document.getElementById('carousel-container');
const totalSlides = document.querySelectorAll('#carousel-container > div').length;

// Automatic sliding
function startAutoSlide() {
    return setInterval(() => {
        currentIndex = (currentIndex + 1) % totalSlides;
        carouselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    }, 3000);
}

let slideInterval = startAutoSlide();

// Manual sliding
document.getElementById('next').addEventListener('click', () => {
    clearInterval(slideInterval); // Stop automatic sliding
    currentIndex = (currentIndex + 1) % totalSlides;
    carouselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    slideInterval = startAutoSlide(); // Restart automatic sliding
});

document.getElementById('prev').addEventListener('click', () => {
    clearInterval(slideInterval); // Stop automatic sliding
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    carouselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    slideInterval = startAutoSlide(); // Restart automatic sliding
});
