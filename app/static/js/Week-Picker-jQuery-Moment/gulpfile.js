/* eslint-disable */
const gulp = require("gulp");
const gutil = require("gulp-util");
const eslint = require("gulp-eslint");
const uglify = require("gulp-uglify");
const cleanCSS = require('gulp-clean-css');

gulp.task("lint", function () {
	return gulp.src("src/*.js")
		.pipe(eslint())
		.pipe(eslint.format())
		.pipe(eslint.failAfterError());
})

gulp.task("compress-js", function () {
	return gulp.src("src/*.js")
		.pipe(uglify())
		.pipe(gulp.dest("dist"));
})

gulp.task("compress-css", function () {
	return gulp.src("src/css/*.css")
		.pipe(cleanCSS())
		.pipe(gulp.dest("dist"));
})

gulp.task("watch", function () {
	gulp.watch("src/*.js", ["lint", "compress-js"]);
	gulp.watch("src/css/*.css", ["compress-css"]);
})