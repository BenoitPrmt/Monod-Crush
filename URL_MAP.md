```
Endpoint               Methods    Rule
---------------------  ---------  ----------------------------------
admin.ajout_admin      GET        /admin/user/<username>/add
admin.checking         POST       /admin/post/<int:post_id>/checking
admin.delete           POST       /admin/post/<int:post_id>/delete
admin.panel            GET        /admin/
admin.supprimer_admin  GET        /admin/user/<username>/sup
auth.login             GET, POST  /auth/login
auth.logout            GET        /auth/logout
auth.register          GET, POST  /auth/register
blog.create            GET, POST  /post/new
blog.delete            POST       /post/<int:post_id>/delete
blog.edit              GET, POST  /post/<int:post_id>/edit
blog.index             GET        /
blog.like              POST       /post/<int:post_id>/like
blog.report            POST       /post/<int:post_id>/report
index                  GET        /
search.all_user        GET        /all_user
search.search_user     GET        /search
sitemap.robots         GET        /robots.txt
sitemap.sitemap        GET        /sitemap.xml
static                 GET        /static/<path:filename>
user.delete            POST       /user/<username>/delete
user.edit              GET        /user/<username>/edit
user.profile           GET        /user/<username>
user.update_user       POST       /user/<username>/edit
```
