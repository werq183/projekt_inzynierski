document.getElementById('image-form').onsubmit = function() {
            document.getElementById('loading-message').style.display = 'block';
        };

        function imageLoaded() {
            var imagesContainer = document.getElementById('images-container');
            var images = imagesContainer.getElementsByTagName('img');
            var allImagesLoaded = true;
            for (var i = 0; i < images.length; i++) {
                if (!images[i].complete) {
                    allImagesLoaded = false;
                    break;
                }
            }
            if (allImagesLoaded) {
                document.getElementById('loading-message').style.display = 'none';
            }
        }