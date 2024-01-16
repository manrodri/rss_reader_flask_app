from flask import Flask, render_template
import jinja_partials
import feedparser


feeds = {
    "https://blog.teclado.com/rss/":  {
    "title": "The Teclado blog",
    "href": "https://blog.teclado.com/rss/",
    "show_images": True,
    "entries": {   
    }
},
    "https://www.joshwcomeau.com/rss.xml": {
        "title": "Josh Comeau",
        "href":  "https://www.joshwcomeau.com/rss.xml",
        "show_images": False,
        "entries": {}
    }
}


def create_app():
    app = Flask(__name__)
    jinja_partials.register_extensions(app)
    
    @app.route('/')
    @app.route('/feed/<path:feed_url>')
    def render_feed(feed_url:str = None):
        for url, feed_ in feeds.items():
            parsed_feed = feedparser.parse(url)
            for entry in parsed_feed.entries:
                if entry.link not in feed_['entries']:
                    feed_['entries'][entry.link] = entry
        
        if feed_url is None:
            feed = list(feeds.values())[0]
        else:
            feed = feeds[feed_url]
        return render_template('feed.html', feed=feed, entries=feed['entries'].values(), feeds=feeds)
    
    return app