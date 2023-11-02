var currentIndex = 0;
    var images = document.querySelectorAll("#slideshow img");
    var prevBtn = document.getElementById("prevBtn");
    var nextBtn = document.getElementById("nextBtn");
    var clickArea = document.getElementById("clickArea");

    function showImage(index) {
        images.forEach(function (image) {
            image.classList.remove("active");
        });
        images[index].classList.add("active");
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage(currentIndex);
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        showImage(currentIndex);
    }

    function handleAreaClick(event) {
        var rect = clickArea.getBoundingClientRect();
        var x = event.clientX - rect.left;
        var y = event.clientY - rect.top;

        var clickAreaWidth = rect.width;
        var clickAreaHeight = rect.height;

        if (x < clickAreaWidth / 2) {
            // Kliknięcie po lewej stronie obrazu
            prevImage();
        } else {
            // Kliknięcie po prawej stronie obrazu
            nextImage();
        }
    }


    prevBtn.addEventListener("click", prevImage);
    nextBtn.addEventListener("click", nextImage);

    clickArea.addEventListener("click", handleAreaClick);

    // Automatyczna zmiana zdjęć co kilka sekund
    setInterval(nextImage, 5000); // Zmiana co 5 sekund

    // Wywołanie funkcji showImage po załadowaniu strony
    window.addEventListener("load", function () {
        showImage(currentIndex);
    });

