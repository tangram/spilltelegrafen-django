// autogrow plugin
(function(b){b.fn.autogrow=function(){this.filter("textarea").each(function(){var a=b(this),e=a.height(),d=b("<div></div>").css({position:"absolute",top:-1E4,left:-1E4,width:b(this).width(),fontSize:a.css("fontSize"),fontFamily:a.css("fontFamily"),lineHeight:a.css("lineHeight"),resize:"none"}).addClass("shadow").appendTo(document.body),a=function(){var a=this;setTimeout(function(){var c=a.value.replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/&/g,"&amp;").replace(/\n/g,"<br/>&nbsp;");if(c===""|| b.trim(c)==="")c="a";d.html(c);b(a).css("height",Math.max(d[0].offsetHeight+20,e))},0)};b(this).change(a).keyup(a).keydown(a).focus(a);a.apply(this)});return this}})(jQuery);

// autogrow textareas
$(document).ready(function() {
    $('textarea#id_body').css({
        'width': '98%'
    }).autogrow();
});
