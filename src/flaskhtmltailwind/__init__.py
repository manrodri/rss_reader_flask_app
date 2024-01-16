from flask import Flask, render_template
import jinja_partials
import feedparser


feed = {
    "title": "The Teclado blog",
    "href": "https://blog.teclado.com/rss/",
    "show_images": True,
    "entries": {
        
    }
}

def create_app():
    app = Flask(__name__)
    jinja_partials.register_extensions(app)
    
    @app.route('/feed/')
    def render_feed():
        feed_url = feed['href']
        parsed_feed = feedparser.parse(feed_url)
        
        for entry in parsed_feed.entries:
            if entry.link not in feed['entries']:
                feed['entries'][entry.link] = entry
        return render_template('feed.html', feed=feed, entries=feed['entries'].values())
    
    return app