from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
from .forms import UpdateProfile,PitchForm,CommentForm
from ..models import User,Pitch,Comment
from flask_login import login_required, current_user
from .. import db,photos
import markdown2


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to The best Movie Review Website Online'

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

    return render_template('profile/update.html', form = form)



@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data

        # Updated pitch instance
        new_pitch = Pitch(pitch_title=title,pitch_content=pitch,category=category,user=current_user,like=0,dislike=0)

        # Save pitch method
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('new_pitch.html',title = title,pitch_form=pitch_form, new_pitch=new_pitch)

@main.route('/user/<uname>/update/pic', methods = ['POST'])
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile', uname = uname))


@main.route('/pitches/studentPitch')
def studentPitch():

    pitches = Pitch.get_pitches('students')

    return render_template("category/studentPitch.html", pitches = pitches)


@main.route('/pitches/coursesPitch')
def coursesPitch():

    pitches = Pitch.get_pitches('courses')

    return render_template("category/coursesPitch.html", pitches = pitches)

@main.route('/pitch/<int:id>/<int:likes>', methods = ['GET','POST'])
def pitch_likes(id,likes):
    pitch = Pitch.get_pitch(id)
    print(likes)
    if request.args.get("like"):
        pitch.like = likes

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        pitch.dislike = pitch.dislike + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    return redirect(url_for('.pitch', id=pitch.id))

@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    if request.args.get("like"):
        pitch.like = pitch.like + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        pitch.dislike = pitch.dislike + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))
       
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.title.data
        commentm = comment_form.comment.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id = pitch.id, comment_writer=commentm)

        new_comment.save_comment()


    comments = Comment.get_comments(id)
    user = Comment.query.filter_by(pitch_id=pitch.id).first()
    # print(user.comment_writer)


    return render_template("pitches.html", pitch = pitch, comment_form = comment_form, comments = comments, user=user)



@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/user.html", user=user,pitches=pitches,pitches_count=pitches_count)



    