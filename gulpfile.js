var autoprefixer = require('gulp-autoprefixer'),
    batch = require('gulp-batch'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    newer = require('gulp-newer'),
    sourcemaps = require('gulp-sourcemaps'),
    watch = require('gulp-watch');

var browserify = require('browserify'),
    browserSync = require('browser-sync'),
    buffer = require('vinyl-buffer'),
    map = require('vinyl-map'),
    mainBowerFiles = require('main-bower-files'),
    source = require('vinyl-source-stream');

gulp.task('browser-sync', function() {
    browserSync({
        proxy: "127.0.0.1:8080",
        logLevel: "silent",
    });
});

gulp.task('bower', function() {
    gulp.src(mainBowerFiles({filter: (/.*\.png$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./ps_pages/static/css/__bower_components/'))
        .pipe(map(function(code, filename) { gutil.log('Bower Images ' + gutil.colors.green(filename));
    }))
    gulp.src(mainBowerFiles({filter: (/.*\.css$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./ps_pages/static/css/__bower_components/'))
        .pipe(map(function(code, filename) { gutil.log('Bower CSS ' + gutil.colors.green(filename));
    }))
    gulp.src(mainBowerFiles({filter: (/.*\.js$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./ps_pages/static/js/__bower_components/'))
        .pipe(map(function(code, filename) { gutil.log('Bower JS ' + gutil.colors.green(filename));
    }))
});

gulp.task('browserify', function() {
    browserify('./ps_pages/static/js/main.js')
        .bundle()
        .pipe(source('__ps_pages.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({loadMaps: true}))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./ps_pages/static/js/'))
        .pipe(map(function(code, filename) { gutil.log('Browserify ' + gutil.colors.green(filename)); }))
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('css', function() {
    path = ['./ps_pages/static/css/*.css',
            './ps_pages/static/css/**/*.css',
            '!./ps_pages/static/css/__*.css'];
    gulp.src(path)
        .pipe(newer('./ps_pages/static/css/__ps_pages.css'))
        .pipe(sourcemaps.init())
        .pipe(autoprefixer({
            browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
            cascade: false
        }))
        .on('error', function(err) {
            gutil.log(gutil.colors.red('Autoprefixer Error'), gutil.colors.yellow(err.message));
        })
        .pipe(minifyCSS())
        .pipe(concat('__ps_pages.css'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./ps_pages/static/css/'))
        .pipe(map(function(code, filename) { gutil.log('CSS ' + gutil.colors.green(filename)); }))
        .on('error', gutil.log)
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('watch', function() {
    watch(['./ps_pages/static/css/*.css',
           './ps_pages/static/css/**/*.css',
           '!./ps_pages/static/css/__*.css'], { verbose: true }, batch(function () {
        gulp.start('css');
        cb();
    }));
    watch(['./ps_pages/static/js/*.js',
           './ps_pages/static/js/**/*.js',
           '!./ps_pages/static/js/__*.js'], { verbose: true }, batch(function (cb) {
        gulp.start('browserify');
        cb();
    }));
});

gulp.task('default', ['watch', 'browser-sync']);
