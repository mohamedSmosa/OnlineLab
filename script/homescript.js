// JavaScript for slideshow functionality
let slideIndex = 0;

function showSlides() {
    const slides = document.getElementsByClassName("slide");
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("slide-display");
    }

    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    slides[slideIndex - 1].classList.add("slide-display");
    setTimeout(showSlides, 3000); // Change image every 3 seconds
}

showSlides();
