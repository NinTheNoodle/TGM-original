from tgm.drivers import get_engine, get_audio


audio = get_audio()
renderer = get_engine()


def run(setup):
    audio.init_audio()
    renderer.init_renderer()
    setup()
    renderer.run()
