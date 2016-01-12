from tgm.drivers import get_renderer, get_controller, get_audio


controller = get_controller()
audio = get_audio()
renderer = get_renderer()


def run(setup):
    audio.init_audio()
    renderer.init_renderer()
    controller.init_controller()
    setup()
    controller.run()
