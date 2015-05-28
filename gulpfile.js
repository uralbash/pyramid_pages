'use strict';

var gulp = require('gulp'),
    $ = require('gulp-load-plugins')({ pattern: ['gulp-*', 'gulp.*'] }),
    minifyCSS = require('gulp-minify-css');

var browserify = require('browserify'),
    browserSync = require('browser-sync'),
    buffer = require('vinyl-buffer'),
    map = require('vinyl-map'),
    mainBowerFiles = require('main-bower-files'),
    source = require('vinyl-source-stream');

var TARGET_CSS_FILE = '__ps_pages.css',
    TARGET_JS_FILE = '__ps_pages.js',
    BROWSERIFY_FILE = 'main.js';

var CSS_PATH = './ps_pages/static/css/',
    JS_PATH = './ps_pages/static/js/',
    IMG_PATH = './ps_pages/static/img/';

var TARGET_CSS_PATH = CSS_PATH + TARGET_CSS_FILE,
    TARGET_JS_PATH = JS_PATH + TARGET_JS_FILE;

var CSS_FILES = ['./ps_pages/static/css/*.css',
                 './ps_pages/static/css/**/*.css',
                 '!ps_pages/static/css/no-js.css',
                 '!ps_pages/static/css/' + TARGET_CSS_FILE
                ],
    JS_FILES = ['./ps_pages/static/js/*.js',
                './ps_pages/static/js/**/*.js',
                '!ps_pages/static/js/' + TARGET_JS_FILE,
                '!ps_pages/static/js/vendor/*.js'
               ],
    TEMPLATES_FILES = ['*.html'];


gulp.task('browser-sync', function() {
  browserSync({
    proxy: '127.0.0.1:8080',
    logLevel: 'silent'
  });
});


gulp.task('bower-js', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(js|map)$/i) }),
                 { base: 'bower_components' })
  .pipe($.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(JS_PATH + 'vendor/'))
  .pipe(map(function(code, filename) {
    $.util.log('Bower JS ' +
    $.util.colors.green(filename));
  }));
});


gulp.task('bower-css', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(css)$/i) }),
                 { base: 'bower_components' })
  .pipe($.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(CSS_PATH + 'vendor/'))
  .pipe(map(function(code, filename) {
    $.util.log('Bower CSS ' +
    $.util.colors.green(filename));
  }));
});


gulp.task('bower-img', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(png|jpg|gif)$/i) }),
                 { base: 'bower_components' })
  .pipe($.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(IMG_PATH))
  .pipe(map(function(code, filename) {
    $.util.log('Bower Images ' +
    $.util.colors.green(filename));
  }));
});


gulp.task('browserify', function() {
  return browserify(JS_PATH + BROWSERIFY_FILE)
    .bundle()
    .pipe(source(TARGET_JS_PATH))
    .pipe(buffer())
    .pipe($.sourcemaps.init({ loadMaps: true }))
    .pipe($.sourcemaps.write('./'))
    .pipe(gulp.dest('./'))
    .pipe(map(function(code, filename) {
      $.util.log('Browserify ' +
      $.util.colors.green(filename));
    }))
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('css', function() {
  return gulp.src(CSS_FILES)
    .pipe($.newer(TARGET_CSS_PATH))
    .pipe($.sourcemaps.init())
    .pipe($.autoprefixer({
      browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9',
                 'Chrome >= 15', 'Safari >= 4', '> 1%'],
      cascade: false
    }))
    .on('error', function(err) {
      $.util.log($.util.colors.red('Autoprefixer Error'),
      $.util.colors.yellow(err.message));
    })
    .pipe($.cssBase64({
      extensions: ['png', 'jpg', 'gif'],
      maxWeightResource: 100,
    }))
    .on('error', function(err) {
      $.util.log($.util.colors.red('Base64 Error'),
      $.util.colors.yellow(err.message));
    })
    .pipe($.concat(TARGET_CSS_FILE))
    .pipe(minifyCSS({ keepSpecialComments: 0 }))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest(CSS_PATH))
    .on('error', $.util.log)
    .pipe($.filter('*.css'))
    .pipe(map(function(code, filename) {
      $.util.log('CSS ' +
      $.util.colors.green(filename));
    }))
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('html', function() {
  return gulp.src(TEMPLATES_FILES)
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('watch', function() {
  $.watch(CSS_FILES,{ verbose: true },
    $.batch(function (cb) {
      gulp.start('css');
      cb();
    }));

  $.watch(JS_FILES, { verbose: true },
    $.batch(function (cb) {
      console.log(JS_FILES);
      gulp.start('browserify');
      cb();
    }));

  $.watch(TEMPLATES_FILES, { verbose: true },
    $.batch(function (cb) {
      gulp.start('html');
      cb();
    }));
});


gulp.task('default', ['browser-sync', 'watch']);
gulp.task('bower', ['bower-js', 'bower-css', 'bower-img']);
gulp.task('build', ['bower', 'css', 'js']);