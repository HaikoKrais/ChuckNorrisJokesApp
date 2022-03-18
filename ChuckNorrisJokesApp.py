from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import ButtonBehavior
from kivy.utils import get_color_from_hex
from kivy.uix.behaviors import TouchRippleBehavior

class ChuckNorrisJokes(FloatLayout):
    '''Root Widget displaying the Card holding the joke and the buttons to load new jokes or to empty the current joke'''
    joke = StringProperty('')
    icon_url = 'https://upload.wikimedia.org/wikipedia/commons/3/3b/PlaceholderRoss.png?20200509222132'

    def __init__(self, **kwargs):
        super(ChuckNorrisJokes, self).__init__(**kwargs)
        self.color = App.get_running_app()._colors['background']

    def get_new_joke(self):
        request = UrlRequest(url='https://api.chucknorris.io/jokes/random', on_success=self.update_joke,
                             on_error=self.show_error)

    def update_joke(self, request, result):
        self.joke = result['value']

    def show_error(self, request, error):
        print(error)

    def reset_joke(self):
        self.joke = ''


class ContainedFlatButton(TouchRippleBehavior, ButtonBehavior, FloatLayout):

    def __init__(self, **kwargs):
        super(ContainedFlatButton, self).__init__(**kwargs)
        self.color = App.get_running_app()._colors['primary']

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            touch.grab(self)
            self.ripple_show(touch)
            return super(ContainedFlatButton, self).on_touch_down(touch)


    def on_touch_up(self, touch):
        touch.ungrab(self)
        self.ripple_fade()
        return super(ContainedFlatButton, self).on_touch_up(touch)

class OutlinedFlatButton(TouchRippleBehavior, ButtonBehavior, FloatLayout):

    def __init__(self, **kwargs):
        super(OutlinedFlatButton, self).__init__(**kwargs)
        self.color = App.get_running_app()._colors['primary']

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            touch.grab(self)
            self.ripple_color = App.get_running_app()._colors['primary']
            self.ripple_fade_to_alpha = 0,6
            self.ripple_show(touch)
            return super(OutlinedFlatButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        self.ripple_fade()
        return super(OutlinedFlatButton, self).on_touch_up(touch)

class Card(BoxLayout):

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        color = App.get_running_app()._colors['on_background']
        self.color =  color.copy()
        color[3] = 0.5
        self.outline_color = color

class ChuckNorrisJokesApp(App):
    colors = {'primary':'#6200EE',
              'background': '#FFFFFF',
              'on_primary':'#FFFFFF',
              'on_background':'#000000'}

    def __init__(self, **kwargs):
        super(ChuckNorrisJokesApp, self).__init__(**kwargs)
        self._colors = {}
        for key, value in self.colors.items():
            self._colors[key] = get_color_from_hex(value)

if __name__ == '__main__':
    ChuckNorrisJokesApp().run()
