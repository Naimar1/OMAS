from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,PostForm,CommentForm
from ..models import User,Post,Comment
from flask_login import login_required, current_user
from .. import db,photos
import markdown2
from datetime import datetime


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to our Blog site'

    return render_template('index.html', title = title )

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update', methods = ['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname = user.username))

@main.route('/user/<uname>/update/pic', methods = ['POST'])
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile', uname = uname))

    return render_template('profile/update.html', form = form)



@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    post_form = PostForm()
    new_post= None
    if post_form.validate_on_submit():
        title = post_form.title.data
        post = post_form.text.data
        
        users = User.query.all()
        # Updated post instance
        new_post = Post(post_title=title,post_content=post,user=current_user)

        # Save post method
        new_post.save_post()
        return redirect(url_for('.index'))

    title = 'New post'
    return render_template('new_post.html',title = title,post_form=post_form, new_post=new_post)

@main.route('/posts')
def all_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    title = 'Blog-Post'

    return render_template('posts.html', title=title, posts=posts)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    form = CommentForm()
    post = Post.get_post(id)

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment, user=current_user, post=post.id)

        new_comment.save_comment()

    comments = Comment.get_comments(post)

    title = f'{post.post_title}'
    return render_template('post.html', title=title, post=post, form=form, comments=comments)


@main.route('/delete_comment/<id>/<post_id>', methods=['GET', 'POST'])
def delete_comment(id, post_id):
    comment = Comment.query.filter_by(id=id).first()

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.post', id=post_id))


@main.route('/delete_post/<id>', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.all_posts'))


# @main.route('/subscribe/<id>')
# def subscribe(id):
#     user = User.query.filter_by(id=id).first()

#     user.subscription = True

#     db.session.commit()

#     return redirect(url_for('main.index'))


@main.route('/post/update/<id>', methods=['GET', 'POST'])
def update_post(id):
    form = PostForm()

    post = Post.query.filter_by(id=id).first()

    form.title.data = post.post_title
    form.text.data = post.post_content

    if form.validate_on_submit():
        post_title = form.title.data
        post_content = form.text.data

        post.title = post_title
        post.text = post_content

        db.session.commit()

        return redirect(url_for('main.post', id=post.id))

    return render_template('update.html', form=form)




