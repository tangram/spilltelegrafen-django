from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs, urlunparse

register = template.Library()

@register.filter(is_safe=True)
def textile(value):
    try:
        import textile
        from textile.tools import sanitizer
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in 'textile' filter: The Python textile library isn't installed.")
        return force_unicode(value)
    else:
        textiled = textile.textile(
                value, head_offset=2, auto_link=True, html_type='html'
            )

        try:
            soup = BeautifulSoup(textiled)
        except:
            return

        blacklist = [
            'form', 'input', 'textarea', 'button', 'font',
            'table', 'tbody', 'thead', 'tr', 'td',
        ]

        for tag in soup.find_all():
            if tag.name.lower() in blacklist:
                tag.extract()

        textiled = unicode(soup)

        images = [
            'jpg', 'jpeg', 'png', 'gif'
        ]
        # convert 'Tube links to embeds and image links to <img>
        for link in soup.find_all('a'):
            url = urlparse(link.get('href'))

            video = None
            if url.netloc == 'youtu.be':
                video = url.path
            elif url.netloc in ('youtube.com', 'www.youtube.com'):
                query = parse_qs(url.query)
                video = query["v"][0]
            if video:
                embed = '<iframe width="640" height="360" src="http://www.youtube.com/embed/%s?rel=0" frameborder="0" allowfullscreen></iframe>' % video
                textiled = textiled.replace(str(link), embed)

            image = None
            if (url.path).split('.')[-1] in images:
                image = '<img src="%s">' % urlunparse((url.scheme, url.netloc, url.path, None, None, None))
                textiled = textiled.replace(str(link), image)

        return mark_safe(textiled)