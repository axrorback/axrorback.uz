from django.contrib.syndication.views import Feed
from .models import Post

class LatestPostFeed(Feed):
    title = 'Ahrorjon Ibrohimjonov axrorback Blog web page'
    link = '/rss/'
    description = 'axrorback AhrorjonIbrohimjonov Blog Page Posts'


    def items(self):
        return Post.objects.filter(is_published=True).order_by('-created')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:300]

    def item_link(self, item):
        return item.get_absolute_url()