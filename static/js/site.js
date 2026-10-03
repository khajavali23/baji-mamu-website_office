document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       MOBILE MENU
    ===================================================== */

    const mobileNav = document.getElementById("mobileNav");
    const mainNav = document.querySelector(".main-nav");

    if (mobileNav && mainNav) {

        mobileNav.addEventListener("click", function () {

            mainNav.classList.toggle("open");

        });

    }

    


    /* =====================================================
       NAVIGATION DROPDOWNS
    ===================================================== */

    document.querySelectorAll(".nav-trigger").forEach(function (button) {

        button.addEventListener("click", function (event) {

            event.stopPropagation();

            const group = button.closest(".nav-group");

            document.querySelectorAll(".nav-group.open").forEach(function (item) {

                if (item !== group) {
                    item.classList.remove("open");
                }

            });

            group.classList.toggle("open");

        });

    });


    document.addEventListener("click", function () {

        document.querySelectorAll(".nav-group.open").forEach(function (group) {

            group.classList.remove("open");

        });

    });


    /* =====================================================
       HERO BANNER CAROUSEL
    ===================================================== */

    const heroSlides = document.querySelectorAll(".hero-slide");
    const featureSlides = document.querySelectorAll(".feature-slide");
    const featureCopies = document.querySelectorAll(".feature-copy");

    const previousButton = document.querySelector(".feature-prev");
    const nextButton = document.querySelector(".feature-next");

    const counterCurrent = document.querySelector(".counter-current");

    if (heroSlides.length > 0) {

        let current = 0;
        let autoPlay;


        function showSlide(index) {

            if (index < 0) {
                index = heroSlides.length - 1;
            }

            if (index >= heroSlides.length) {
                index = 0;
            }

            current = index;


            heroSlides.forEach(function (slide, i) {

                slide.classList.toggle(
                    "active",
                    i === current
                );

            });


            featureSlides.forEach(function (slide, i) {

                slide.classList.toggle(
                    "active",
                    i === current
                );

            });


            featureCopies.forEach(function (copy, i) {

                copy.classList.toggle(
                    "active",
                    i === current
                );

            });


            if (counterCurrent) {

                counterCurrent.textContent =
                    String(current + 1).padStart(2, "0");

            }

        }


        function nextSlide() {

            showSlide(current + 1);

        }


        function previousSlide() {

            showSlide(current - 1);

        }


        if (nextButton) {

            nextButton.addEventListener(
                "click",
                function () {

                    nextSlide();

                    restartAutoPlay();

                }
            );

        }


        if (previousButton) {

            previousButton.addEventListener(
                "click",
                function () {

                    previousSlide();

                    restartAutoPlay();

                }
            );

        }


        function startAutoPlay() {

            if (heroSlides.length > 1) {

                autoPlay = setInterval(
                    nextSlide,
                    6000
                );

            }

        }


        function restartAutoPlay() {

            clearInterval(autoPlay);

            startAutoPlay();

        }


        startAutoPlay();

    }

});


/* =====================================================
   HERO NEWS AUTO CAROUSEL
===================================================== */

const heroNewsImages = document.querySelectorAll(".hero-news-image");
const heroNewsCopies = document.querySelectorAll(".hero-news-copy");

const heroNewsPrev = document.querySelector(".hero-news-prev");
const heroNewsNext = document.querySelector(".hero-news-next");

const newsCurrent = document.querySelector(".news-current");


if (heroNewsCopies.length > 0) {

    let currentNews = 0;
    let newsAutoPlay;


    function showNews(index) {

        if (index < 0) {
            index = heroNewsCopies.length - 1;
        }

        if (index >= heroNewsCopies.length) {
            index = 0;
        }

        currentNews = index;


        /* NEWS IMAGES */

        heroNewsImages.forEach(function (image, i) {

            image.classList.toggle(
                "active",
                i === currentNews
            );

        });


        /* NEWS CONTENT */

        heroNewsCopies.forEach(function (copy, i) {

            copy.classList.toggle(
                "active",
                i === currentNews
            );

        });


        /* COUNTER */

        if (newsCurrent) {

            newsCurrent.textContent =
                String(currentNews + 1).padStart(2, "0");

        }

    }


    function nextNews() {

        showNews(currentNews + 1);

    }


    function previousNews() {

        showNews(currentNews - 1);

    }


    /* =================================================
       NEXT / PREVIOUS BUTTONS
    ================================================= */

    if (heroNewsNext) {

        heroNewsNext.addEventListener(
            "click",
            function () {

                nextNews();

                restartNewsAutoPlay();

            }
        );

    }


    if (heroNewsPrev) {

        heroNewsPrev.addEventListener(
            "click",
            function () {

                previousNews();

                restartNewsAutoPlay();

            }
        );

    }


    /* =================================================
       AUTO PLAY
    ================================================= */

    function startNewsAutoPlay() {

        if (heroNewsCopies.length > 1) {

            newsAutoPlay = setInterval(
                nextNews,
                5000
            );

        }

    }


    function restartNewsAutoPlay() {

        clearInterval(newsAutoPlay);

        startNewsAutoPlay();

    }


    /* START */

    showNews(0);

    startNewsAutoPlay();

}
/* =====================================================
   OPEN ALL BANNER BUTTONS IN NEW TAB
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(
        ".hero-secondary-actions a, .hero-primary-action a"
    ).forEach(function (link) {

        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener noreferrer");

    });

});