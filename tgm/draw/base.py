from tgm.system import Entity, sys_event


class RenderContext(Entity):
    @sys_event
    def render(self):
        self.parent.tags.select(
            Entity[sys_event.render],
            stop=Entity[RenderContext] - Entity[self],
            abort=self
        ).render()
