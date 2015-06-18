'use strict';

var Gallery = function(item) {
  if (!(this instanceof Gallery)) {
    return new Gallery('.gallery-list');
  }
  this.gallery = $(item);
  this.getImageId($(item));
};


Gallery.prototype.getImageId = function() {
  $(document).on('click',
    '.gallery-list__item-link', function(event) {

        var popup = require('./popup.js').Popup();
        popup.showPopup();

        $('.fotorama').fotorama({
          width: '100%',
          fit: 'cover',
          loop: true,
          maxwidth: '100%',
          minheight: '500',
          nav: 'thumbs',
          ratio: '16/9',
          thumbwidth: '80',
          thumbheight: '55',
          data: IMAGES_LIST
        });
        var fotorama = $('.fotorama').data('fotorama'),
            target = $(this).data('fotorama-image-id');

        fotorama.show(target - 1);

        return event.preventDefault();
      });
};


module.exports.Gallery = Gallery;