# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from app.main.functions import sugarfunc, foodfunc, insfunc, fordoc, readdb, names, send_attention, kkallim, carblim, plotfunc
import pandas as pd
from flask import render_template, flash, redirect, url_for, request, g, current_app, jsonify, send_from_directory, \
    send_file
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm, SugarForm, FoodForm, InsulinForm
from app.models import User, Post, Message, Notification, SugarTable, InsulinTable, FoodDatatable
from flask_babel import _, get_locale
from app.auth import bp
import flask_excel as excel



@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('auth.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    if current_user.doctor is 0:  # new
        posts = current_user.posts.order_by(Post.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    if posts.has_next:
        next_url = url_for('auth.index', page=posts.next_num)
    else:
        next_url = None
    prev_url = url_for('auth.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    if current_user.doctor is 0:  # new
        posts = current_user.posts.order_by(Post.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('auth.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('auth.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>', methods=['GET', 'POST']) #### here
@login_required
def user(username):
    user_id = current_user.id
    formsug=SugarForm()
    formfood=FoodForm()
    formins = InsulinForm()
    docb = fordoc(user_id)
    pcntnote = names(docb)
    if current_user.doctor == 0:
        if request.method == 'POST':
            q = kkallim(user_id)
            c = carblim(user_id)
            qlim = current_user.kkal
            clim = current_user.carbohydrates_level
            if q <= qlim:
                send_attention('Значение потребленных ККал ниже базовой потребности')
            elif c <= clim:
                send_attention('Значение потребленных углеводов ниже базовой потребности')
            if request.form['submit'] == 'sugar':
                sugarfunc(formsug)
            elif request.form['submit'] == 'food':
                foodfunc(formfood)
            elif request.form['submit'] == 'insulin':
                insfunc(formins)
            return redirect(url_for('auth.user', username=username))



    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('auth.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('auth.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, formsug=formsug,
                           formfood=formfood, formins=formins, FIO=pcntnote)

@bp.route('/instable', methods=['GET', 'POST'])
@login_required
def instable():
    user_id = current_user.id
    df = readdb('select * from insulin_table')
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    dfc = dfl[['timestamp','eat','insulin','dose']]
    return render_template('instable.html', dfl=dfc)

@bp.route('/sugtable', methods=['GET', 'POST'])
@login_required
def sugtable():
    user_id = current_user.id
    df = readdb('select * from sugar_table')
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    dfc = dfl[['timestamp','eat','mol']]
    return render_template('sugtable.html', dfl=dfc)

@bp.route('/foodtable', methods=['GET', 'POST'])
@login_required
def foodtable():
    user_id = current_user.id
    df = readdb('select * from food_table')
    dfl = df.loc[lambda df: df['user_id'] == user_id, :]
    dfc = dfl[['timestamp','eating','food', 'kkal', 'carbohydrates']]
    return render_template('foodtable.html', dfl=dfc)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.weight = form.weight.data
        current_user.kkal = form.kkal.data
        current_user.sugarlevel = form.mol.data
        current_user.carbohydrates_level = form.carb.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('auth.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.weight.data =current_user.weight
        form.mol.data = current_user.sugarlevel
        form.kkal.data =current_user.kkal
        form.carb.data = current_user.carbohydrates_level
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('auth.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('auth.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('auth.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('auth.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('auth.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('auth.user', username=username))


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('auth.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    # user, total = User.search(g.search_form.q.data, page,
    #                            current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('auth.search', q=g.search_form.q.data, page=page + 1)  # \ #надо бы исправить
    # if total > page * current_app.config['POSTS_PER_PAGE'] else None
    # TypeError: '>' not supported between instances of 'dict' and 'int'
    prev_url = url_for('auth.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts, user=user,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('auth.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('auth.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('auth.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])




