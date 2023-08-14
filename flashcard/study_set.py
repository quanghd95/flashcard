from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flashcard.auth import login_required
from flashcard.db import get_db

bp = Blueprint('study_set', __name__)

def get_study_set(id, check_author=True):
    study_set = get_db().execute(
        'SELECT st.id, title, description, level, st.created_at, author_id, username'
        ' FROM study_set st JOIN user u ON st.author_id = u.id'
        ' WHERE st.id = ?',
        (id,)
    ).fetchone()

    if study_set is None:
        abort(404, f"Study set id {id} doesn't exist.")

    return study_set

@bp.route('/')
def index():
    db = get_db()
    study_sets = db.execute(
        'SELECT st.id, title, description, st.created_at, author_id, username'
        ' FROM study_set st JOIN user u ON st.author_id = u.id'
        ' ORDER BY st.created_at DESC'
    ).fetchall()
    return render_template('study_set/index.html', study_sets=study_sets)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        level = request.form['level']
        error = None

        if not title:
            error = 'Title is required.'
        if not description:
            error = 'Description is required.'
        if not level:
            error = 'Level is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO study_set (title, description, author_id, level)'
                ' VALUES (?, ?, ?, ?)',
                (title, description, g.user['id'], level)
            )
            db.commit()
            return redirect(url_for('study_set.index'))

    return render_template('study_set/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    study_set = get_study_set(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        level = request.form['level']
        error = None

        if not title:
            error = 'Title is required.'
        if not description:
            error = 'Description is required.'
        if not level:
            error = 'Level is required.'


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE study_set SET title = ?, description = ?, level = ?'
                ' WHERE id = ?',
                (title, description, level, id)
            )
            db.commit()
            return redirect(url_for('study_set.index'))

    return render_template('study_set/update.html', study_set=study_set)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_study_set(id)
    db = get_db()
    db.execute('DELETE FROM study_set WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('study_set.index'))