from tgm.system import GameObject, sys_event


class RenderContext(GameObject):
    @sys_event
    def render(self):
        self.parent.tags.select(
            GameObject[sys_event.render],
            stop=GameObject[RenderContext] - GameObject[self],
            abort=self
        ).render()
