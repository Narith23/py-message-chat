/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!****************************************************!*\
  !*** ./resources/js/pages/session-timeout.init.js ***!
  \****************************************************/
/*
Template Name: Minible - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Session Timeout Js File
*/

$.sessionTimeout({
  keepAliveUrl: 'pages-starter',
  logoutButton: 'Logout',
  logoutUrl: 'auth-login',
  redirUrl: 'auth-lock-screen',
  warnAfter: 3000,
  redirAfter: 30000,
  countdownMessage: 'Redirecting in {timer} seconds.'
});
$('#session-timeout-dialog  [data-dismiss=modal]').attr("data-bs-dismiss", "modal");
/******/ })()
;