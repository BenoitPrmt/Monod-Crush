document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const burgerButton = document.querySelector('.navbar-burger');
    const navbarMenu = document.querySelector('.navbar-menu');

    const dropdownContainer = document.querySelector('.navbar-item.has-dropdown');
    const dropdownMenu = document.querySelector('.navbar-dropdown');

    window.onresize = function() {
        if (window.innerWidth > 1025) {
            navbarMenu.classList.remove('is-active');
            burgerButton.classList.remove('is-active');
            dropdownMenu.classList.remove('is-hidden');
        }
    }

    if (burgerButton && navbarMenu) {
        burgerButton.addEventListener('click', () => {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            burgerButton.classList.toggle('is-active');
            navbarMenu.classList.toggle('is-active');

            if (burgerButton.classList.contains('is-active')) {
                // en ouvrant le menu on cache le dropdown
                dropdownMenu.classList.add('is-hidden');
            } else {
                // en fermant le menu, on remet le dropdown menu en place
                dropdownMenu.classList.remove('is-hidden');
            }
        });
    }



    dropdownContainer.addEventListener('click', () => {
        if (burgerButton.classList.contains('is-active')) {

            if (burgerButton.classList.contains('is-active')) {
                dropdownMenu.classList.toggle('is-hidden');
            }
        }

    });
});