// autogrow plugin
(function(b){b.fn.autogrow=function(){this.filter("textarea").each(function(){var a=b(this),e=a.height(),d=b("<div></div>").css({position:"absolute",top:-1E4,left:-1E4,width:b(this).width(),fontSize:a.css("fontSize"),fontFamily:a.css("fontFamily"),lineHeight:a.css("lineHeight"),resize:"none"}).addClass("shadow").appendTo(document.body),a=function(){var a=this;setTimeout(function(){var c=a.value.replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/&/g,"&amp;").replace(/\n/g,"<br/>&nbsp;");if(c===""|| b.trim(c)==="")c="a";d.html(c);b(a).css("height",Math.max(d[0].offsetHeight+20,e))},0)};b(this).change(a).keyup(a).keydown(a).focus(a);a.apply(this)});return this}})(jQuery);

(function($) {
  // widearea!
  wideArea().setOptions({ closeIconLabel: "Lukk", changeThemeIconLabel: "Skift tema", fullScreenIconLabel: "Fullskjerm" });
  
  // autogrow textareas
  //$('textarea').autogrow();

  // resize videos
  $(function() {
    var $all = $("iframe[src^='http://www.youtube.com'], iframe[src^='http://vimeo.com']");

    $all.each(function() {
      var url = $(this).attr("src");
      var ch = "?";
      if(url.indexOf("?") != -1)
        ch = "&";
      $(this)
        .data('aspectRatio', this.height / this.width)
        .removeAttr('height')
        .removeAttr('width')
        .attr("src",url+ch+"wmode=transparent");;
    });

    $(window).resize(function() {
      $all.each(function() {
        var $el = $(this);
        var w = $el.parent().width();
        $el
          .width(w)
          .height(w * $el.data('aspectRatio'));
      });
    }).resize();
  });

  // ajax submit for comment form
  (function submitBind() {
    $('#comment').submit(function(e) {

      e.preventDefault();
      var form = $(e.target);

      $.post(form.attr('action'), form.serialize(), function(data) {
        $('#discussion').append(data);
        $('#comment textarea').val('');
      });

    });
  })();

  // ctrl/cmd + enter to submit
  $('form').keypress(function(e) {
    if (e.keyCode === 10 || e.keyCode == 13 && e.ctrlKey || e.metaKey) {
      $(this).submit();
    }
  });

})(jQuery);