from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
from .forms import UpdateProfile,PitchForm,CommentForm
from ..models import User,Pitch,Comment
from flask_login import login_required, current_user
from .. import db,photos
import markdown2


# Views
# @app.route('/')
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''

#     message = 'Hello World'
#     return render_template('index.html',message = message)
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

#     # Getting popular movie
#     popular_movies = get_movies('popular')
#     upcoming_movie = get_movies('upcoming')
#     now_showing_movie = get_movies('now_playing')

    title = 'Home - Welcome to The best Movie Review Website Online'

    #     search_movie = request.args.get('movie_query')

    #     if search_movie:
    #         return redirect(url_for('search',movie_name=search_movie))
    #     else:
    return render_template('index.html', title = title )

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

# @main.route('/movies/<int:id>')
# def movies(movie_id):

#     '''
#     View movie page function that returns the movie details page and its data
#     '''
#     return render_template('movie.html',id = movie_id)
# @main.route('/movie/<int:id>')
# def movie(id):

#     '''
#     View movie page function that returns the movie details page and its data
#     '''
#     movie = get_movie(id)
#     title = f'{movie.title}'
#     reviews = Review.get_reviews(movie.id)

#     return render_template('movie.html',title = title,movie = movie,reviews = reviews)
# @main.route('/search/<movie_name>')
# def search(movie_name):
#     '''
#     View function to display the search results
#     '''
#     movie_name_list = movie_name.split(" ")
#     movie_name_format = "+".join(movie_name_list)
#     searched_movies = search_movie(movie_name_format)
#     title = f'search results for {movie_name}'
#     return render_template('search.html',movies = searched_movies)
# @main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
# @login_required
# def new_review(id):
#     form = ReviewForm()
#     movie = get_movie(id)

#     if form.validate_on_submit():
#         title = form.title.data
#         review = form.review.data
#         new_review = Review(movie_id=movie.id,movie_title=title,image_path=movie.poster,movie_review=review,user=current_user)
#         new_review.save_review()
#         return redirect(url_for('movie',id = movie.id ))

#     title = f'{movie.title} review'
#     return render_template('new_review.html',title = title, review_form=form, movie=movie)

@main.route('/user/<uname>/update/pic',methods = ['POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        return redirect(url_for('main.profile',uname=uname))

    return render_template('profile/update.html',form =form)

# @main.route('/review/<int:id>')
# def single_review(id):
#     review=Review.query.get(id)
#     if review is None:
#         abort(404)
#     format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
#     return render_template('review.html',review = review,format_review=format_review)

@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data

        # Updated pitch instance
        new_pitch = Pitch(pitch_title=title,pitch_content=pitch,category=category,user=current_user,upvote=0,downvote=0)

        # Save pitch method
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('new_pitch.html',title = title,pitch_form=pitch_form )


@main.route('/pitches/studentPitch')
def studentPitch():

    pitches = Pitch.get_pitches('students')

    return render_template("studentPitch.html", pitches = pitches)


@main.route('/pitches/coursesPitch')
def coursesPitch():

    pitches = Pitch.get_pitches('courses')

    return render_template("coursesPitch.html", pitches = pitches)


@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    if request.args.get("upvote"):
        pitch.upvotes = pitch.upvotes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("downvote"):
        pitch.downvotes = pitch.downvotes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()


    comments = Comment.get_comments(pitch)

    return render_template("pitches.html", pitch = pitch, comment_form = comment_form, comments = comments)

@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/user.html", user=user,pitches=pitches,pitches_count=pitches_count)



    