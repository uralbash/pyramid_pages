'use strict';

var gulp = require('gulp'),
    plugins = require('gulp-load-plugins')({ pattern: ['gulp-*', 'gulp.*'] });

var map = require('vinyl-map'),
    mainBowerFiles = require('main-bower-files');

var CSS_PATH = './static/css/',
    JS_PATH = './static/js/',
    IMG_PATH = './static/img/';


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


gulp.task('bower', ['bower-js', 'bower-css', 'bower-img']);
