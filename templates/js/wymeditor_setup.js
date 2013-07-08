$(document).ready(function() {

  wymeditor_filer = function(wym, wdw) {
    var filer_url = '/admin/filer/folder/',
    dlg = $(wdw.document.body);

    if (dlg.hasClass('wym_dialog_image')) {
      dlg.find('.wym_src')
        .css('width', '200px')
        .attr('id', 'filer_image')
        .after('<a id="filer_link" title="Filer" href="#">Filer</a>');
      dlg.find('fieldset')
        .append('<a id="link_filer"><img id="filer_image_thumbnail_img" /></a>'
          + '<br /><span id="help_filer"></span>');
      dlg.find('#filer_link').click(function() {
        filer_window = wdw.open(
            filer_url + '?pop=1',
            'filer_image',
            'height=600,width=840,resizable=yes,scrollbars=yes'
          );
        filer_window.focus();
        return false;
      });
    }
  }

  $('textarea').wymeditor({
    lang: 'nb',
    skin: 'default',
    logoHtml: '',
    postInitDialog: wymeditor_filer,
  });

});
