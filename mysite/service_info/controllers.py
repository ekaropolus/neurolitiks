from flask import render_template, url_for, flash, redirect
from mysite import db
from .forms import ServiceInfoForm
from .models import ServiceInfo
import pandas as pd


def config_services_info_controller():
    form = ServiceInfoForm()
    if form.validate_on_submit():
        service_info = ServiceInfo(service_name=form.service_name.data,
                                   service_icon=form.service_icon.data,
                                   service_abstract=form.service_abstract.data,
                                   service_description = form.service_description.data)
        db.session.add(service_info)
        db.session.commit()
        flash('Your service has been created! You are now able to show it', 'success')
        return redirect(url_for('main.index'))
    return render_template('service_info/service_info_form.html', title='Register', form=form)


def config_services_list_controller():
    sf = ServiceInfo.query.all()
    df = pd.read_sql_table('service_info', db.engine)
    return render_template('service_info/service_info_list.html', sf=sf, \
                           table_lemmas=[df.to_html(classes='table table-hover table-striped table-dark', table_id = "dtHorizontalVerticalExample")], \
                           title_lemmas=df.columns.values)

def config_services_grid_controller():
    sf = ServiceInfo.query.all()
    return render_template('service_info/service_info_grid.html', sf=sf)