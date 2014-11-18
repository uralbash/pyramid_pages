var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch');

var _ = require("underscore"),
    glob = require("glob"),
    minimatch = require("minimatch");

function getFiles(path) {
    var files = glob.sync(path + '**/*.css');
    target = minimatch.match(files, '__*.css', { matchBase: true });
    ignore = _.map(target, function(item){ return '!' + item; });
    result = files.concat(ignore);
    return result;
}

gulp.task('css', function() {

    var path = glob.sync('./*/static/css/'),
        concatFiles = getFiles(path);

    gulp.src(concatFiles)
        .pipe(autoprefixer({
            browsers: [
                'Firefox >= 3',
                'Explorer >= 6',
                'Opera >= 9',
                'Chrome >= 15',
                'Safari >= 4',
                '> 1%'],
            cascade: false
        }))
        .pipe(minifyCSS())
        .pipe(concat('__pages.css'))
        .pipe(gulp.dest(path + '/'));
});

gulp.task('watch', function () {

    var path = glob.sync('./*/static/*/'),
        watchFiles = getFiles(path);

    watch(watchFiles, function (files) {
        gulp.start('css', cb);
    });
});

gulp.task('default', ['watch']);