'use strict';

if (typeof $ === 'undefined') { require('jquery'); }

var fotorama = require('./vendor/fotorama.js'),
    popup = require('./popup.js').Popup(),
    gallery = require('./gallery.js').Gallery();