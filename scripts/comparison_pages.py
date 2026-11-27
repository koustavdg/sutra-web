"""Render the same comparison content for public builds and noindex previews."""
import html
import json
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime
try:
    from .product_facts import expand_facts
except ImportError:
    from product_facts import expand_facts

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://sutra-reader.com'
HEADINGS = {'compare-readers': 'Compare Sutra, Readest and Panels', 'sutra-vs-readest': 'Sutra vs Readest', 'sutra-vs-panels': 'Sutra vs Panels'}
QUESTIONS = {
    'compare-readers': [
        ('Can one app read regular EPUB ebooks and panel-by-panel CBZ comics?', 'Yes. Sutra reads regular text EPUB ebooks and guides you through detected CBZ comic panels on iOS and Android. EPUB and PDF reading are free; full CBZ and DRM-free MOBI reading require a one-time Pro purchase per platform. Panel detection is not guaranteed for every page layout.'),
        ('Can Sutra stream comics without downloading the whole archive?', 'Yes, with Sutra Pro and supported Kavita or Komga servers. Comic pages load on demand; individual pages still transfer and may be cached. Komga requires Page Streaming permission and library access. Download the complete comic for offline reading. Generic OPDS catalog access alone does not guarantee streaming.'),
        ('Can I read ebooks and comics without a subscription?', 'Sutra has free EPUB and PDF reading and optional Pro features purchased once per platform. Full CBZ and DRM-free MOBI require Pro. Readest and Panels also offer ways to use their apps without a subscription; compare the specific features and limits.'),
        ('Which personal libraries can Sutra connect to?', 'Sutra supports Kavita, Komga, Calibre Content Server, Calibre-Web, Calibre-Web-Automated, WebDAV and compatible OPDS feeds. Catalog access does not guarantee page streaming or server progress sync. {{product.komga_access}}'),
        ('Are Read Aloud and cross-platform sync available in Sutra?', 'Kokoro Read Aloud and pronunciation packs are in development. {{product.sync_status}} These are not counted as shipped advantages in this comparison.')],
    'sutra-vs-readest': [
        ('When is Sutra an alternative to Readest?', 'Consider Sutra if you want ebooks and panel-by-panel comics on iOS or Android, direct access to your personal libraries, no app analytics and a one-time Pro upgrade. Consider Readest if desktop or web reading and broader cloud synchronization are priorities.'),
        ('Does Readest require a subscription?', 'No. Readest has a free plan and optional one-time purchases as well as subscriptions. Compare the features you need rather than treating it as subscription-only.'),
        ('Will Sutra sync progress, highlights and notes across platforms?', '{{product.sync_status}} This does not mean that the standard KOSync protocol transports annotations or that third-party reader annotation compatibility is confirmed. Existing iOS iCloud sync is separate and already available.')],
    'sutra-vs-panels': [
        ('When is Sutra an alternative to Panels?', 'Consider Sutra when you want text ebooks and comics together, Android availability as well as iOS, and no app analytics. Panels may fit better if you need CBR today or an Apple-focused comic library with Mac reading.'),
        ('Is panel-by-panel comic reading exclusive to Sutra?', 'No. Sutra uses a custom panel detection engine, while Panels also advertises guided navigation. No head-to-head detection accuracy or rendering benchmark is claimed here.'),
        ('Can Sutra open CBR files today?', '{{product.cbr_status}} It should not be treated as an available reason to switch. Current comic support includes CBZ and compatible ZIP comic archives.')]
}

def esc(value):
    return html.escape(str(value), quote=True)


class ReleaseNotes(HTMLParser):
    """Count dated platform/version entries, not commits or upcoming plans."""
    def __init__(self):
        super().__init__()
        self.entries = []
        self.platform = None
        self.field = None
        self.fields = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        if tag == 'div' and 'version' in classes:
            self.platform = attrs.get('data-p')
            self.fields = {}
        for field in ('version-num', 'version-status'):
            if field in classes:
                self.field = field
                self.fields[field] = ''

    def handle_data(self, text):
        if self.field:
            self.fields[self.field] += text

    def handle_endtag(self, tag):
        if self.field == 'version-num' and tag == 'div':
            self.field = None
        elif self.field == 'version-status' and tag == 'span':
            self.field = None
            if self.platform not in ('ios', 'android'):
                return
            try:
                date = datetime.strptime(self.fields['version-status'].strip(), '%b %d, %Y').date()
            except ValueError:
                return  # Upcoming entries are not releases.
            self.entries.append((self.platform, self.fields['version-num'].strip(), date))


def release_summary(source=None):
    parser = ReleaseNotes()
    parser.feed(source if source is not None else (ROOT / 'changelog.html').read_text())
    entries = set(parser.entries)
    if not entries:
        raise ValueError('No dated platform releases found in the published changelog')
    dates = [date for _, _, date in entries]
    def readable(date):
        return f'{date:%B} {date.day}, {date.year}'
    ios = sum(platform == 'ios' for platform, _, _ in entries)
    android = sum(platform == 'android' for platform, _, _ in entries)
    text = (f'From {readable(min(dates))} to {readable(max(dates))}, '
            f"Sutra's published changelog records {len(entries)} dated platform releases: "
            f'{ios} for iOS and {android} for Android, including the initial platform launches.')
    return text

def render_comparisons(out, preview=False):
    content = json.loads(expand_facts((ROOT / 'content/comparisons.json').read_text()))
    product = json.loads((ROOT / 'content/product.json').read_text())
    template = expand_facts((ROOT / 'templates/comparison.html').read_text())
    cadence = release_summary()
    slugs = [page['slug'] for page in content['pages']]
    if set(slugs) != set(HEADINGS) or len(slugs) != len(set(slugs)):
        raise ValueError('Expected exactly the three approved comparison pages')
    out.mkdir(parents=True, exist_ok=True)
    for page in content['pages']:
        slug = page['slug']
        url = f'{BASE}/{slug}.html'
        def cited(value):
            result = esc(value)
            for key in page['sources']:
                result = result.replace('[' + key + ']', '<a class="citation" href="#source-' + key + '">[' + key + ']</a>')
            return result
        benefits = ''.join('<article><h3>' + esc(title) + '</h3><p>' + cited(body) + '</p></article>' for title, body in page['benefits'])
        fit_summary = ''.join('<article><h3>' + esc(title) + '</h3><p>' + cited(body) + '</p></article>' for title, body in page['fit_summary'])
        heads = ''.join('<th scope="col">' + esc(x) + '</th>' for x in page['columns'])
        rows = ''.join('<tr><th scope="row">' + esc(row[0]) + '</th>' + ''.join('<td>' + cited(cell) + '</td>' for cell in row[1:]) + '</tr>' for row in page['rows'])
        sources = ''.join('<li id="source-' + key + '"><strong>[' + key + ']</strong> <a href="' + esc(content['sources'][key][1]) + '">' + esc(content['sources'][key][0]) + '</a></li>' for key in page['sources'])
        related = ''.join('<a class="related-card" href="' + esc(other['slug']) + '.html"><span>Read the comparison</span><strong>' + esc(HEADINGS[other['slug']]) + ' <span aria-hidden="true">&#8594;</span></strong></a>' for other in content['pages'] if other['slug'] != slug)
        crumbs = [{'@type':'ListItem','position':1,'name':'Home','item':BASE + '/'}]
        crumbs.append({'@type':'ListItem','position':2,'name':'Compare readers','item':BASE + '/compare-readers.html'})
        if slug != 'compare-readers':
            crumbs.append({'@type':'ListItem','position':3,'name':HEADINGS[slug],'item':url})
        breadcrumbs = '<span aria-hidden="true"> / </span>'.join('<a href="' + ('/' if c['position']==1 else 'compare-readers.html') + '">' + esc(c['name']) + '</a>' if i<len(crumbs)-1 else '<span aria-current="page">' + esc(c['name']) + '</span>' for i,c in enumerate(crumbs))
        webpage = {'@type':'WebPage','@id':url + '#webpage','url':url,'name':page['title'],'description':page['description'],'inLanguage':'en','dateModified':content['reviewed'],'publisher':{'@id':BASE + '/#organization'},'about':{'@id':BASE + '/#sutra-app'},'citation':[content['sources'][key][1] for key in page['sources']] + [BASE + '/changelog.html'],'breadcrumb':{'@id':url + '#breadcrumb'}}
        graph = [webpage, {'@type':'BreadcrumbList','@id':url + '#breadcrumb','itemListElement':crumbs}]
        if slug == 'compare-readers':
            compared = [s for s in slugs if s != slug]
            webpage['mainEntity'] = {'@id':url + '#comparisons'}
            graph.append({'@type':'ItemList','@id':url + '#comparisons','name':'Sutra reader comparisons','itemListElement':[{'@type':'ListItem','position':i+1,'name':HEADINGS[s],'url':BASE + '/' + s + '.html'} for i,s in enumerate(compared)]})
        metadata = ('<meta property="og:type" content="website"><meta property="og:site_name" content="Sutra">'
                    '<meta property="og:title" content="' + esc(page['title']) + '"><meta property="og:description" content="' + esc(page['description']) + '">'
                    '<meta property="og:image" content="' + BASE + '/assets/app-icon.png"><meta property="og:image:alt" content="Sutra app icon">'
                    '<meta name="twitter:card" content="summary">')
        if not preview:
            metadata += '<link rel="canonical" href="' + url + '"><meta property="og:url" content="' + url + '">'
            metadata += '<script type="application/ld+json">' + json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c') + '</script>'
        questions = [*QUESTIONS[slug], ('Does Sutra offer two-page reading on tablets?',
            '{{product.tablet_layout}} {{product.comic_spread_status}} Duo also has fold-aware layouts.')]
        faq = ''.join('<details><summary>' + esc(q) + '</summary><p>' + esc(expand_facts(a)) + '</p></details>' for q,a in questions)
        tokens = {**page,'release_cadence':cadence,'search_heading':HEADINGS[slug],'benefits':benefits,'fit_summary':fit_summary,'heads':heads,'rows':rows,'sources':sources,'related':related,'faq':faq,'breadcrumbs':breadcrumbs,'metadata':metadata,
                  'robots':'noindex,nofollow' if preview else 'index,follow,max-image-preview:large',
                  'banner':'<div class="draft">Editorial preview &middot; Not published &middot; Sources reviewed ' + esc(content['reviewed']) + '</div>' if preview else '',
                  'reviewed':content['reviewed'],'ios_store':product['stores']['ios']['url'],'android_store':product['stores']['android']['url']}
        raw = {'benefits','fit_summary','heads','rows','sources','related','faq','breadcrumbs','metadata','banner'}
        rendered = template
        for key,value in tokens.items():
            if isinstance(value,str):
                rendered = rendered.replace('{{' + key + '}}',value if key in raw else esc(value))
        if '{{' in rendered:
            raise ValueError('Unresolved token in ' + slug)
        rendered = rendered.replace('/_site/', '/_site/' if preview else '/')
        (out / (slug + '.html')).write_text(rendered)
    return slugs
