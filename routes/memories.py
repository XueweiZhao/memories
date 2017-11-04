import markdown
import os
from flask import abort, Blueprint, Markup, redirect, render_template, request, url_for
from utils.calendar import get_calendar_data, NotValidDateError, validate_date
from utils.files import MemoryFile

blueprint = Blueprint('memories', __name__)


@blueprint.route('/memories/<int:year>/')
@blueprint.route('/memories/<int:year>/<int:month>/')
def calendar(year, month=1):
    try:
        validate_date(year, month)
    except NotValidDateError:
        abort(404)

    month_label, month_list, month_file_list = get_calendar_data(year, month)
    return render_template(
        'memories/calendar.jinja',
        year=year,
        month=month,
        month_label=month_label,
        month_list=month_list,
        month_file_list=month_file_list,
    )


@blueprint.route('/memories/calendar/', methods=['POST'])
def calendar_go():
    form_data = request.form
    year = form_data.get('year')
    month = form_data.get('month')
    return redirect(url_for('memories.calendar', year=year, month=month))


@blueprint.route('/memories/<int:year>/<int:month>/<int:day>/')
def memory(year, month, day):
    content = MemoryFile(year, month, day).get_content()
    content = Markup(markdown.markdown(content))
    return render_template(
        'memories/day.jinja',
        year=year,
        month=month,
        day=day,
        content=content,
    )


@blueprint.route('/memories/<int:year>/<int:month>/<int:day>/edit/')
def edit(year, month, day):
    raw_content = MemoryFile(year, month, day).get_preview_content()
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
    MemoryFile(year, month, day).write_preview(content)
    return redirect(url_for('memories.edit', year=year, month=month, day=day))


@blueprint.route('/memories/<int:year>/<int:month>/<int:day>/save/', methods=['POST'])
def save(year, month, day):
    MemoryFile(year, month, day).save_preview()
    return redirect(url_for('memories.memory', year=year, month=month, day=day))
