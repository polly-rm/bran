from django.contrib.sitemaps import Sitemap

from bran.base.models import SendEmail


class StaticSitemap(Sitemap):
    changefreq = "always"  # The homepage is updated frequently
    priority = 1.0  # High priority

    def items(self):
        return ['index']  # List the URL names for static pages

    def location(self, item):
        if item == 'index':
            return '/'  # URL for the homepage

    def get_urls(self, site=None, **kwargs):
        urls = super().get_urls(site=site, **kwargs)
        for url in urls:
            url['location'] = 'https://branlogistics.co.uk/'
        return urls


class SendEmailSitemap(Sitemap):
    changefreq = "monthly"  # Change frequency of the SendEmail entries
    priority = 0.5  # Lower priority than homepage

    def items(self):
        return SendEmail.objects.all()  # All SendEmail entries

    def lastmod(self, obj):
        return obj.updated_at  # Last updated time of the SendEmail entry
