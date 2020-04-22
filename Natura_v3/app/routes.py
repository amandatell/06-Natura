from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, DeleteUserForm
from flask_login import current_user, login_user
from app.models import User, Post, categories, places, place_has_cat
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from app.rating import save_user_rating, average_rating
from app.image_upload import image_upload
import os


global drop_down_cats
drop_down_cats = db.session.query(categories)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html', drop_down_cats=drop_down_cats)


# to my page
@app.route('/myaccount',methods=['GET', 'POST'])
@login_required
def myaccount():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Din post är skickat!')
        return redirect(url_for('myaccount'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('myaccount', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('myaccount', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('myaccount.html', drop_down_cats=drop_down_cats, title='Mitt Konto', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

#the login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ogiltig username eller password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
         
        return redirect(next_page)
    return render_template('login.html', drop_down_cats=drop_down_cats, title='Loga In', form=form)
    

# log out function
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# registering function
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Grattis, Du är medlem nu!')
        return redirect(url_for('login'))
    return render_template('register.html', drop_down_cats=drop_down_cats, title='Skappa Konto', form=form)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteUserForm()
    if form.validate_on_submit():
        delete_user = User.query.filter_by(username=form.username.data).first()

        db.session.delete(delete_user)
        db.session.commit()
        flash('Ditt konto har raderats. Hoppas att vi ses igen.', 'success')
        return redirect(url_for('logout'))
    else:
        flash('Ogiltig username eller password')

    return render_template('delete.html', form=form)


# the profile page of user
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', drop_down_cats=drop_down_cats, user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, loggedin=True)
# records the last seen time /date of user
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# edit profile page of the user
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Dina ändringar har sparats.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', drop_down_cats=drop_down_cats, title='Edit Profile',
                           form=form, loggedin=True)

# function for following other users posts
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Användaren {} hittades inte.'.format(username))
        return redirect(url_for('myaccount'))
    if user == current_user:
        flash('Du kan inte följa dig själv!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('Du följer {}!'.format(username))
    return redirect(url_for('user', username=username))

# to unfollow a user
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Användaren {} hittades inte.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('Du kan inte sluta följa dig själv!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Du följer inte {}.'.format(username))
    return redirect(url_for('user', username=username))

# the page that shows all the posts of users
@app.route('/posts')
@login_required
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('posts', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("myaccount.html", drop_down_cats=drop_down_cats, title='Posts', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)


 # user sends request for changing password
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Kontrollera din e-post för instruktioner för att återställa ditt lösenord')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', drop_down_cats=drop_down_cats,
                           title='Reset Password', form=form)


# user connects through a token to change password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ditt lösenord har blivit återställt.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', drop_down_cats=drop_down_cats, form=form)

# the page that holds category of places
@app.route('/<category>')
def category(category):
    places_cat = db.session.query(places.name, places.id).join(place_has_cat).join(categories).filter(categories.name==category)
    return render_template('category.html', drop_down_cats=drop_down_cats, category=category, places=places_cat)

 # page related to each place
@app.route('/<category>/<name>/<placeid>', methods=['GET', 'POST'])
def place(category, name, placeid):
    places_from_db = db.session.query(places.description, places.source).filter(places.name==name)
    if request.args.get('rating'):
        user_rating = request.args.get('rating')
        save_user_rating(user_rating, name)
    files = image_upload(placeid)
    return render_template('place.html', drop_down_cats=drop_down_cats, info=places_from_db, name=name, files=files, category=category, placeid=placeid)
    
# the info page
@app.route('/info')
def info():
    return render_template('info.html', drop_down_cats=drop_down_cats)
    
# the contacts page
@app.route('/contact')
def contact():
    return render_template('contact.html', drop_down_cats=drop_down_cats)
    
# the gallery page
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():

    return render_template('gallery.html', drop_down_cats=drop_down_cats)


