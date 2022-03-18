Endpoint            Methods    Rule
------------------  ---------  --------------------------
admin.panel         GET        /admin/
auth.login          GET, POST  /auth/login
auth.logout         GET        /auth/logout
auth.post_register  POST       /auth/register
auth.register       GET        /auth/register
blog.create         GET, POST  /post/new
blog.delete         POST       /post/<int:post_id>/delete
blog.edit           GET, POST  /post/<int:post_id>/edit
blog.index          GET        /
index               GET        /
static              GET        /static/<path:filename>
user.edit           GET, POST  /user/<username>/edit
user.profile        GET        /user/<username>
