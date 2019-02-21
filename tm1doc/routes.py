import logging
import sys

from tm1doc import tm1doc
from flask import render_template, session, flash, redirect, url_for, request, jsonify
from tm1doc.Server import Server

from config import *

import requests_cache

requests_cache.install_cache('tm1_cache', expire_after=Config.get_cache_timeout())


def filter_technical_objects(object):
    if Config.get_ignore_technical_objects() and object.name.startswith('}'):
        return False
    else:
        return True


# default session things ... not ideal i suppose


context = {}

instances = []
for instance in Config.get_tm1_instances():
    tm1_instance = Server(instance['address'], instance['port'], instance['user'], instance['password'],
                          instance['ssl_verify'])
    instances.append(tm1_instance)
    print(tm1_instance.get_server_name())

context['instances'] = instances


@tm1doc.route('/foo')
def foo():
    tm1_server = instances[session['instance_id']]
    tm1_server.get_source_to_dimension_mapping()
    # for instance in instances:
    #    flash(instance.get_server_name())
    # return redirect(url_for('index'))


@tm1doc.route('/dimensions')
def dimensions():
    context['session'] = session
    try:
        tm1_server = instances[session['instance_id']]
    except KeyError:
        flash('Select an Instance')
        return redirect(url_for('index'))

    dimensions = tm1_server.get_source_to_dimension_mapping()

    #filtered_dimensions =

    #dimensions = filter(filter_technical_objects, dimensions.iteritems() )
    return render_template('dimensions.html', context=context, title='Dimensions',
                           dimensions=dimensions,
                           )


@tm1doc.route('/select_instance/<instance_name>')
def select_instance(instance_name):
    # find instance or default to the first

    session['instance_id'] = 0
    instance_was_found = False
    for id, instance in enumerate(instances):
        if instance.name == instance_name:
            session['instance_id'] = id
            instance_was_found = True
    if not instance_was_found:
        flash(f'Instance {instance_name} does not exist. Using {instances[0].name}')
    return redirect(url_for('overview'))


@tm1doc.route('/')
@tm1doc.route('/index')
def index():
    context['session'] = session
    return render_template('index.html', context=context, title='Overview')


@tm1doc.route('/overview')
def overview():
    context['session'] = session
    try:
        tm1_server = instances[session['instance_id']]
    except KeyError:
        flash('Select an Instance')
        return redirect(url_for('index'))
    return render_template('overview.html', context=context, title='Home',
                           cubes=filter(filter_technical_objects, tm1_server.cubes),
                           dimensions=filter(filter_technical_objects, tm1_server.dimensions),
                           processes=filter(filter_technical_objects, tm1_server.processes),
                           server=tm1_server.get_server_name(),
                           )


@tm1doc.route('/analysis')
def analysis():
    context['session'] = session
    try:
        tm1_server = instances[session['instance_id']]
    except KeyError:
        flash('Select an Instance')
        return redirect(url_for('index'))

    return render_template('analysis.html', context=context, title='Analysis',
                           flow=tm1_server.create_dataflow_graph())


@tm1doc.route('/refresh')
def refresh():
    context['session'] = session
    requests_cache.core.clear()
    flash(f'Cache cleared, or maybe not ...')
    return redirect(url_for('overview'))
