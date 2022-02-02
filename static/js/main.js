$(document).ready(function(){
    // Mobile Menu
    $('.header .menu-btn').on('click', function(e){
        $('header').toggleClass('menu-open');
        e.preventDefault();
    })
    // Products Slider
    $('.section-products .owl-carousel').owlCarousel({
        loop:false,
        margin:25,
        nav:false,
        responsive:{
            0:{
                items:1
            },
            768:{
                items:3
            },
            1000:{
                items:4
            }
        }
        
    })
    $('.section-products .owl-nav .owl-prev').click(function() {
        $('.section-products .owl-carousel').owlCarousel().trigger('prev.owl.carousel', [300]);;
    })
    $('.section-products .owl-nav .owl-next').click(function() {
        $('.section-products .owl-carousel').owlCarousel().trigger('next.owl.carousel');
    })
})