var photoModal = document.getElementById('photoModal');
if (photoModal) {
    buttonPrev = document.getElementById('photoModalPrev');
    buttonNext = document.getElementById('photoModalNext');

    photoModal.addEventListener('show.bs.modal', function (event) {
        // Button that triggered the modal
        var button = event.relatedTarget;
        // Extract info from data-bs-* attributes
        var photo_url = button.getAttribute('data-bs-image-url');
        // Update the modal's content.
        var modalImage = photoModal.querySelector('.modal-body img');
      
        modalImage.src = photo_url;

        // handle prev/next buttons
        var photos = document.getElementsByClassName('card');
        photos = [].slice.call(photos);

        const testFunction = (element) => location.protocol + '//' + location.host + element.querySelector('.card .stretched-link').dataset.bsImageUrl == document.querySelector('.modal-body img').src;
        var currentId = photos.findIndex(testFunction);

        if (currentId == 0)
        {
            // remove prev button
            buttonPrev.style.visibility = "hidden";
        } else {
            buttonPrev.style.visibility = "visible";
        }

        if (currentId == photos.length - 1)
        {
            // remove next button
            buttonNext.style.visibility = "hidden";
        } else {
            buttonNext.style.visibility = "visible";
        }
    });

    buttonPrev.addEventListener('click', function (event) {
        var photos = document.getElementsByClassName('card');
        photos = [].slice.call(photos);

        const testFunction = (element) => location.protocol + '//' + location.host + element.querySelector('.card .stretched-link').dataset.bsImageUrl == document.querySelector('.modal-body img').src;
        var currentId = photos.findIndex(testFunction);

        if (currentId != 0)
        {
            var modalImage = photoModal.querySelector('.modal-body img');
            var nextImageUrl = photos[currentId - 1].querySelector('.card .stretched-link').dataset.bsImageUrl;
            modalImage.src = nextImageUrl;

            if (currentId - 1 == 0)
            {
                // remove prev button
                buttonPrev.style.visibility = "hidden";
            } else if (currentId == photos.length - 1)
            {
                // add next button
                buttonNext.style.visibility = "visible";
            }
        } 
    });

    buttonNext.addEventListener('click', function (event) {
        var photos = document.getElementsByClassName('card');
        photos = [].slice.call(photos);

        const testFunction = (element) => location.protocol + '//' + location.host + element.querySelector('.card .stretched-link').dataset.bsImageUrl == document.querySelector('.modal-body img').src;
        var currentId = photos.findIndex(testFunction);

        if (currentId != photos.length - 1)
        {
            var modalImage = photoModal.querySelector('.modal-body img');
            var nextImageUrl = photos[currentId + 1].querySelector('.card .stretched-link').dataset.bsImageUrl;
            modalImage.src = nextImageUrl;
            
            if (currentId == 0)
            {
                // add prev button
                buttonPrev.style.visibility = "visible";
            } else if (currentId + 1 == photos.length - 1)
            {
                // remove next button
                buttonNext.style.visibility = "hidden";
            }
        }
    });
}
