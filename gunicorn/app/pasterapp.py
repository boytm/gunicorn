# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

import configparser

from gunicorn.app.wsgiapp import WSGIApplication


class PasterApplication(WSGIApplication):
    def init(self, parser, opts, args):
        if len(args) != 1:
            parser.error("No configuration source specified.")

        opts.paste = args.pop()

        return super().init(parser, opts, args)


class PasterServerApplication(WSGIApplication):
    def __init__(self, app, global_conf, local_conf):
        super().__init__()
        self.callable = app
        for k, v in normalize_config(global_conf, local_conf).items():
            self.cfg.set(k, v)

    def load_config(self):
        pass


def has_logging_config(config_file):
    parser = configparser.ConfigParser()
    parser.read([config_file])
    return parser.has_section('loggers')


def normalize_config(global_conf, local_conf):
    config = local_conf.copy()
    config_file = global_conf['__file__']

    host = config.pop('host', '')
    port = config.pop('port', '')
    if host and port:
        config['bind'] = '%s:%s' % (host, port)
    elif host:
        config['bind'] = host.split(',')

    listen = config.pop('listen', '')
    if listen:
        config['bind'] = listen

    if has_logging_config(config_file):
        config.setdefault('logconfig', config_file)

    return config


def serve(app, global_conf, **local_conf):
    """\
    A paste server runner.

    Example configuration:

        [server:main]
        use = egg:gunicorn#main
        host = 127.0.0.1
        port = 5000
    """
    PasterServerApplication(app, global_conf, local_conf).run()
