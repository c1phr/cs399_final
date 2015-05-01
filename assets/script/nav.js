/**
 * Created by chrisheiser1 on 4/30/15.
 */
$(document).ready(function() {
var $menu = $("nav#menu");
var $mobmenu = $menu.clone();
$menu.addClass("hidden-xs");
$mobmenu.attr( "id", "mobile-menu" );
$mobmenu.mmenu();
$menu.mmenu({ offCanvas: false });

<!-- Close mobile menu when resizing browser window -->
$(window).resize(function() {
  if ($(this).width() > 767) {
    $mobmenu.trigger("close.mm");
  }
});
});