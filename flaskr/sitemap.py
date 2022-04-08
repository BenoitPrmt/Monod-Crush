from flask import current_app, Blueprint, request, render_template, Response

from flaskr.db import get_db
from flaskr.models import User

bp = Blueprint("sitemap", __name__)


@bp.route("/sitemap.xml")
def sitemap() -> Response:
    """
        Route to dynamically generate a sitemap of your website/application.
        lastmod and priority tags omitted on static pages.
        lastmod included on dynamic content such as blog posts.
    """

    app = current_app  # grab flask app instance
    exclude_routes = ["static", "admin", "sitemap", "post", "sitemap.xml"]  # routes to exclude4
    # TODO: remove logout
    host_url = request.host_url[:-1]

    # Static routes with static content
    static_urls = set()
    for rule in app.url_map.iter_rules():
        if rule.rule.split("/")[1] not in exclude_routes and len(rule.arguments) == 0 and "GET" in rule.methods:
            static_urls.add(host_url + rule.rule)

    # Dynamic routes with dynamic content
    dynamic_urls = set()
    exclude_users = ["admin"]

    usernames = User.get_all_username()
    for username in usernames:
        if username not in exclude_users:
            dynamic_urls.add(host_url + "/user/" + username)

    xml_sitemap = render_template("sitemap/sitemap.xml", static_urls=static_urls, dynamic_urls=dynamic_urls, )

    # convert xml

    return Response(xml_sitemap, mimetype='text/xml')


@bp.route("/robots.txt")
def robots() -> Response:
    """
        Route to dynamically generate a robots.txt file.
        Disallow all routes that are not static.
    """

    page = """
user-agent: *
disallow: /static/
disallow: /admin/
disallow: /post/

sitemap: https://monodcrush/sitemap.xml"""

    return Response(page, mimetype='text/plain')
