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

  $(document).on('click',
    '.popup-background', this.hidePopup.bind(this)
  );
};

Popup.prototype.showPopup = function() {
  this.popup.css({ display: 'table' });
};

Popup.prototype.hidePopup = function(event) {
  this.popup.css({ display: 'none' });
  if ($(event.target).closest('.popup-background').length > 0){
    this.popup.css({ display: 'none' });
  }
};

module.exports.Popup = Popup;