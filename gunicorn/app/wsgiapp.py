# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

from gunicorn.app.base import Application
from gunicorn import util


class WSGIApplication(Application):
    def init(self, parser, opts, args):
        config = {}

        if opts.paste:
            import plaster
            loader = plaster.get_loader(opts.paste, protocols=['wsgi'])
            config['default_proc_name'] = str(loader.uri)
            if 'loggers' in loader.get_sections():
                config['logconfig'] = loader.uri.path
            return config

        if not args:
            parser.error("No application module specified.")

        config['default_proc_name'] = args[0]

        return config

    def load(self):
        if self.cfg.paste:
            import plaster
            loader = plaster.get_loader(self.cfg.paste, protocols=['wsgi'])
            return loader.get_wsgi_app()

        return util.import_app(self.app_uri)


def run():
    """\
    The ``gunicorn`` command line runner for launching Gunicorn with
    generic WSGI applications.
    """
    from gunicorn.app.wsgiapp import WSGIApplication
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()


if __name__ == '__main__':
    run()
