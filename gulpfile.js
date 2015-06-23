'use strict';

var gulp = require('gulp'),
    plugins = require('gulp-load-plugins')({ pattern: ['gulp-*', 'gulp.*'] });

var browserify = require('browserify'),
    browserSync = require('browser-sync'),
    mainBowerFiles = require('main-bower-files'),
    minimist = require('minimist');

var map = require('vinyl-map'),
    buffer = require('vinyl-buffer'),
    source = require('vinyl-source-stream');

var TARGET_CSS_FILE = '__pyramid_pages.css',
    TARGET_JS_FILE = '__pyramid_pages.js',
    BROWSERIFY_FILE = 'main.js';

var CSS_PATH = './pyramid_pages/static/css/',
    JS_PATH = './pyramid_pages/static/js/',
    IMG_PATH = './pyramid_pages/static/img/',
    FONT_PATH = './pyramid_pages/static/fonts/';

var TARGET_CSS_PATH = CSS_PATH + TARGET_CSS_FILE,
    TARGET_JS_PATH = JS_PATH + TARGET_JS_FILE;

var CSS_FILES = [
  './pyramid_pages/static/css/*.css',
  './pyramid_pages/static/css/**/*.css',
  '!pyramid_pages/static/css/no-js.css',
  '!pyramid_pages/static/css/' + TARGET_CSS_FILE
];

var JS_FILES = [
  './pyramid_pages/static/js/*.js',
  './pyramid_pages/static/js/**/*.js',
  '!pyramid_pages/static/js/' + TARGET_JS_FILE,
  '!pyramid_pages/static/js/vendor/*.js'
];

var TEMPLATES_FILES = [
  './pyramid_pages/**/*.jinja2'
];

var EXAMPLE_TARGET_CSS_FILE = '__main.css',
    EXAMPLE_CSS_PATH = './example/static/css/',
    EXAMPLE_TARGET_CSS_PATH = EXAMPLE_CSS_PATH + EXAMPLE_TARGET_CSS_FILE;

var EXAMPLE_TARGET_JS_FILE = '__main.js',
    EXAMPLE_JS_PATH = './example/static/js/',
    EXAMPLE_TARGET_JS_PATH = EXAMPLE_JS_PATH + EXAMPLE_TARGET_JS_FILE;

var EXAMPLE_CSS_FILES = [
  './example/static/css/*.css',
  './example/static/css/**/*.css',
  '!example/static/css/' + EXAMPLE_TARGET_CSS_FILE
];

var EXAMPLE_JS_FILES = [
  './example/static/js/*.js',
  './example/static/js/**/*.js',
  '!example/static/js/' + EXAMPLE_TARGET_JS_FILE,
  '!example/static/js/vendor/*.js'
];

var EXAMPLE_TEMPLATES_FILES = [
  './example/**/*.jinja2'
];

var knownOptions = {
  string: 'env',
  default: { env: process.env.NODE_ENV || 'development' }
};

var options = minimist(process.argv.slice(2), knownOptions);

var processors = [
    require('postcss-nested'),
    require('autoprefixer-core')({
      browsers: [
        'Firefox >= 3',
        'Explorer >= 6',
        'Opera >= 9',
        'Chrome >= 15',
        'Safari >= 4',
        '> 1%'
      ],
      cascade: false
    }),
    require('postcss-css-variables'),
    require('postcss-opacity')
  ];


gulp.task('browser-sync', function() {
  browserSync({
    proxy: '127.0.0.1:6543',
    logLevel: 'info',
    open: false
  });
});


gulp.task('bower-js', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(js|map)$/i) }),
                 { base: 'bower_components' })
  .pipe(plugins.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(JS_PATH + 'vendor/'))
  .pipe(map(function(code, filename) {
    plugins.util.log('Bower JS ' +
    plugins.util.colors.green(filename));
  }));
});


gulp.task('bower-css', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(css)$/i) }),
                 { base: 'bower_components' })
  .pipe(plugins.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(CSS_PATH + 'vendor/'))
  .pipe(map(function(code, filename) {
    plugins.util.log('Bower CSS ' +
    plugins.util.colors.green(filename));
  }));
});


gulp.task('bower-img', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(png|jpg|gif)$/i) }),
                 { base: 'bower_components' })
  .pipe(plugins.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(IMG_PATH))
  .pipe(map(function(code, filename) {
    plugins.util.log('Bower Images ' +
    plugins.util.colors.green(filename));
  }));
});


gulp.task('bower-font', function() {
  return gulp.src(mainBowerFiles(
    { filter: (/.*\.(svg|ttf|woff|woff2|otf)$/i) }), { base: 'bower_components' })
    .pipe(plugins.rename(function (path) {
      path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
    }))
    .pipe(gulp.dest(FONT_PATH))
    .pipe(map(function(code, filename) {
      plugins.util.log('Bower Fonts ' +
      plugins.util.colors.green(filename));
    }));
});


gulp.task('browserify', function() {

  var b = browserify({
    entries: JS_PATH + BROWSERIFY_FILE,
    debug: true
  });
  return b.bundle()
    .pipe(source(TARGET_JS_PATH))
    .pipe(buffer())
    .pipe(plugins.sourcemaps.init({loadMaps: true}))
    .pipe(plugins.if(options.env === 'production',
      plugins.uglify()))
    .pipe(plugins.if(options.env === 'development',
      plugins.sourcemaps.write('./')))
    .pipe(gulp.dest('./'))
    .pipe(map(function(code, filename) {
      plugins.util.log('Browserify ' +
      plugins.util.colors.green(filename));
    }))
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('css', function() {
  return gulp.src(CSS_FILES)
    .pipe(plugins.newer(TARGET_CSS_PATH))
    .pipe(plugins.sourcemaps.init())
    .pipe(plugins.postcss(processors))
    .on('error', function(err) {
      plugins.util.log(plugins.util.colors.red('PostCSS Error'),
      plugins.util.colors.yellow(err.message));
    })
    .pipe(plugins.cssBase64({
      extensions: ['png', 'jpg', 'gif'],
      maxWeightResource: 100,
    }))
    .on('error', function(err) {
      plugins.util.log(plugins.util.colors.red('Base64 Error'),
      plugins.util.colors.yellow(err.message));
    })
    .pipe(plugins.modifyCssUrls({
      modify: function (url, filePath) {
        if(filePath.indexOf('vendor') > -1) {
          if(url.indexOf('./font') > -1) {
            url = './../' + url.substring(url.indexOf('font'));
          } else if(url.indexOf('./img') > -1) {
            url = './../img/vendor/' + url.substring(url.indexOf('img'));
          }
          if(url.match(/.*\.(png|jpg|gif)$/i)) {
            url = './../img/vendor/' + url.substring(url.indexOf('/'));
          }
          return url;
        } else {
          return url;
        }
      }
    }))
    .pipe(plugins.concat(TARGET_CSS_FILE))
    .pipe(plugins.if(options.env === 'development',
      plugins.sourcemaps.write('.')))
    .pipe(plugins.if(options.env === 'production',
      plugins.minifyCss({ keepSpecialComments: 0 })))
    .pipe(gulp.dest(CSS_PATH))
    .on('error', plugins.util.log)
    .pipe(plugins.filter('*.css'))
    .pipe(map(function(code, filename) {
      plugins.util.log('CSS ' +
      plugins.util.colors.green(filename));
    }))
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('html', function() {
  return gulp.src(TEMPLATES_FILES)
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('dev-browserify', function() {

  var b = browserify({
    entries: EXAMPLE_JS_PATH + BROWSERIFY_FILE,
    debug: true
  });

  return b.bundle()
    .pipe(source(EXAMPLE_TARGET_JS_PATH))
    .pipe(buffer())
    .pipe(plugins.sourcemaps.init({loadMaps: true}))
    .pipe(plugins.if(options.env === 'production',
      plugins.uglify()))
    .pipe(plugins.if(options.env === 'development',
      plugins.sourcemaps.write('./')))
    .pipe(gulp.dest('./'))
    .pipe(map(function(code, filename) {
      plugins.util.log('Browserify ' +
      plugins.util.colors.green(filename));
    }))
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('dev-css', function() {
  return gulp.src(EXAMPLE_CSS_FILES)
    .pipe(plugins.newer(EXAMPLE_TARGET_CSS_PATH))
    .pipe(plugins.sourcemaps.init())
    .pipe(plugins.postcss(processors))
    .on('error', function(err) {
      plugins.util.log(plugins.util.colors.red('PostCSS Error'),
      plugins.util.colors.yellow(err.message));
    })
    .pipe(plugins.cssBase64({
      extensions: ['png', 'jpg', 'gif'],
      maxWeightResource: 100,
    }))
    .on('error', function(err) {
      plugins.util.log(plugins.util.colors.red('Base64 Error'),
      plugins.util.colors.yellow(err.message));
    })
    .pipe(plugins.modifyCssUrls({
      modify: function (url, filePath) {
        if(filePath.indexOf('vendor') > -1) {
          if(url.indexOf('./font') > -1) {
            url = './../' + url.substring(url.indexOf('font'));
          } else if(url.indexOf('./img') > -1) {
            url = './../img/vendor/' + url.substring(url.indexOf('img'));
          }
          if(url.match(/.*\.(png|jpg|gif)$/i)) {
            url = './../img/vendor/' + url.substring(url.indexOf('/'));
          }
          return url;
        } else {
          return url;
        }
      }
    }))
    .pipe(plugins.concat(EXAMPLE_TARGET_CSS_FILE))
    .pipe(plugins.if(options.env === 'development',
      plugins.sourcemaps.write('.')))
    .pipe(plugins.if(options.env === 'production',
      plugins.minifyCss({ keepSpecialComments: 0 })))
    .pipe(gulp.dest(EXAMPLE_CSS_PATH))
    .on('error', plugins.util.log)
    .pipe(plugins.filter('*.css'))
    .pipe(map(function(code, filename) {
      plugins.util.log('CSS ' +
      plugins.util.colors.green(filename));
    }))
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('dev-html', function() {
  return gulp.src(EXAMPLE_TEMPLATES_FILES)
    .pipe(browserSync.reload({ stream:true }));
});

gulp.task('watch', function() {
  plugins.watch(CSS_FILES,{ verbose: true },
    plugins.batch(function (cb) {
      gulp.start('css');
      cb();
    }));

  plugins.watch(JS_FILES, { verbose: true },
    plugins.batch(function (cb) {
      gulp.start('browserify');
      cb();
    }));

  plugins.watch(TEMPLATES_FILES, { verbose: true },
    plugins.batch(function (cb) {
      gulp.start('html');
      cb();
    }));

  if(options.env === 'development') {
    plugins.watch(EXAMPLE_CSS_FILES,{ verbose: true },
      plugins.batch(function (cb) {
        gulp.start('dev-css');
        cb();
      }));

    plugins.watch(EXAMPLE_JS_FILES,{ verbose: true },
      plugins.batch(function (cb) {
        gulp.start('dev-browserify');
        cb();
      }));

    plugins.watch(EXAMPLE_TEMPLATES_FILES, { verbose: true },
      plugins.batch(function (cb) {
        gulp.start('dev-html');
        cb();
      }));
  }
});


gulp.task('default', ['browser-sync', 'watch']);
gulp.task('bower', ['bower-js', 'bower-css', 'bower-img', 'bower-font']);
gulp.task('build', ['bower', 'css', 'browserify']);
gulp.task('dev-build', ['dev-css', 'dev-browserify']);
gulp.task('build-all', ['bower', 'build', 'dev-build']);
