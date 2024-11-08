


/* @odoo-module */

import publicWidget from 'web.public.widget';

publicWidget.registry.CarouselController = publicWidget.Widget.extend({
    selector: '#carouselExampleControls',

    events: {
        'click .thumbnail-image': '_onThumbnailClick', // Bắt sự kiện khi nhấp vào ảnh thumbnail
    },

    /**
     * Khởi tạo widget
     */
    start() {    
        return this._super(...arguments);
    },

    /**
     * Xử lý sự kiện khi nhấp vào ảnh thumbnail
     * @param {Event} ev 
     */
    _onThumbnailClick(ev) {
        ev.preventDefault();
        const index = parseInt(ev.currentTarget.getAttribute('data-index'), 10);
        
        // Khởi tạo carousel và chuyển tới slide tương ứng
        const carouselElement = document.querySelector(this.selector);
        if (carouselElement) {
            const carouselInstance = new bootstrap.Carousel(carouselElement);
            carouselInstance.to(index);
        }
    },
});
