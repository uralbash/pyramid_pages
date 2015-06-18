(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var popup = require('./popup.js').Popup(),
    gallery = require('./gallery.js').Gallery();

(function($){

  'use strict';

  $(window).load(function(){

    var ACTIVE = 'main-menu-list__item_state_active';

    $('.main-menu-list__item')
      .hover(function() {
        var self = $(this);
        if(self.has('.main-menu-list').length > 0) {
          self.addClass(ACTIVE);
          self.siblings('.' + ACTIVE)
              .removeClass(ACTIVE);
          self.find('.main-menu-list .main-menu-list__item')
              .removeClass(ACTIVE);
        }
      })
      .mouseleave(function() {
        var self = $(this);
        self.parent()
            .find('.main-menu-list__item_state_active')
            .removeClass(ACTIVE);
      });

  });
})(jQuery);
},{"./gallery.js":2,"./popup.js":3}],2:[function(require,module,exports){
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
          data: [
            {
              img: 'http://i.imgur.com/ZVTBpjV.jpg',
              thumb: 'http://i.imgur.com/ZVTBpjV.jpg'
            }, {
              img: 'http://i.imgur.com/1RHsVNy.jpg',
              thumb: 'http://i.imgur.com/1RHsVNy.jpg'
            }, {
              img: 'http://i.imgur.com/fmck85z.jpg',
              thumb: 'http://i.imgur.com/fmck85z.jpg'
            }
          ]
        });
        var fotorama = $('.fotorama').data('fotorama'),
            target = $(this).data('fotorama-image-id');

        fotorama.show(target - 1);

        return event.preventDefault();
      });
};


module.exports.Gallery = Gallery;
},{"./popup.js":3}],3:[function(require,module,exports){
'use strict';

var Popup = function(item) {
  if (!(this instanceof Popup)) {
    return new Popup('.popup');
  }
  this.popup = $(item);
  this.popupContainer = $('.popup-inner__content-gallery');
  this._bindEvents();
};

Popup.prototype._bindEvents = function() {
  $(document).on('click',
    '.popup-inner__content-link', this.hidePopup.bind(this)
  );
};

Popup.prototype.showPopup = function() {
  this.popup.css({ display: 'table' });
};

Popup.prototype.hidePopup = function() {
  this.popup.css({ display: 'none' });
};

module.exports.Popup = Popup;
},{}]},{},[1])

