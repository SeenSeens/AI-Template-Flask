'use strict'
class Custom {
    // Constructor
    // Owl Carousel
    sliderTintuc() {
        $('#carouselBlogSlide').owlCarousel({
            loop:true,
            margin:5,
        })
    }
}
// Khởi tạo class khi DOM đã sẵn sàng
jQuery(document).ready( async ($) => {
    const custom = new Custom()
    custom.sliderTintuc();
})