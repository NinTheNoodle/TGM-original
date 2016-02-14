from tgm.drivers import get_engine


engine = get_engine()


def run(setup):
    app = engine.App()
    setup()
    app.run()
