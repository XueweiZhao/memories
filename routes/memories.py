import markdown
import os
from flask import abort, Blueprint, Markup, redirect, render_template, request, url_for
from utils.calendar import get_calendar_data, NotValidDateError, validate_date
from utils.files import get_file, get_preview_file

blueprint = Blueprint('memories', __name__)


@blueprint.route('/memories/<int:year>/')
@blueprint.route('/memories/<int:year>/<int:month>/')
def calendar(year, month=1):
    try:
        validate_date(year, month)
    except NotValidDateError:
        abort(404)

    month_label, month_list = get_calendar_data(year, month)
    return render_template(
        'memories/calendar.jinja',
        year=year,
        month=month,
        month_label=month_label,
        month_list=month_list,
    )


@blueprint.route('/memories/calendar/', methods=['POST'])
def calendar_go():
    form_data = request.form
    year = form_data.get('year')
    month = form_data.get('month')
    return redirect(url_for('memories.calendar', year=year, month=month))


@blueprint.route('/memories/<int:year>/<int:month>/<int:day>/')
def memory(year, month, day):
    filename = '{}-{}-{}'.format(year, month, day)
    content = Markup(markdown.markdown(get_file(filename)))
    return render_template(
        'memories/day.jinja',
        year=year,
        month=month,
        day=day,
        content=content,
    )


@blueprint.route('/memories/<int:year>/<int:month>/<int:day>/edit/')
def edit(year, month, day):
    filename = '{}-{}-{}'.format(year, month, day)
    raw_content = get_preview_file(filename)
    content = Markup(markdown.markdown(raw_content))
    return render_template(
        'memories/edit.jinja',
        year=year,
        month=month,
        day=day,
        raw_content=raw_content,
        content=content,
    )


@blueprint.route('/memories/<int:year>/<int:month>/<int:day>/edit/', methods=['POST'])
def edit_post(year, month, day):
    content = request.form.get('content', '')
    out_filename = 'templates/memories/{}-{}-{}-preview.md'.format(year, month, day)

    dir_name = os.path.dirname(out_filename) or '.'
    if dir_name:
        try:
            os.makedirs(dir_name)
        except OSError:  # Already exists
            pass

    out_file = open(out_filename, 'w+')
    out_file.write(content)
    out_file.close()
    return redirect(url_for('memories.edit', year=year, month=month, day=day))
