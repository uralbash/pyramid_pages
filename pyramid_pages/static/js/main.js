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