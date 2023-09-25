var currentIndex = 0;
var images = document.querySelectorAll("#slideshow img");
var prevBtn = document.getElementById("prevBtn");
var nextBtn = document.getElementById("nextBtn");

function showImage(index) {
    images.forEach(function (image) {
        image.style.display = "none";
    });
    images[index].style.display = "block";
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(currentIndex);
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    showImage(currentIndex);
}

prevBtn.addEventListener("click", prevImage);
nextBtn.addEventListener("click", nextImage);

// Automatyczna zmiana zdjęć co kilka sekund
setInterval(nextImage, 3000); // Zmiana co 3 sekund
