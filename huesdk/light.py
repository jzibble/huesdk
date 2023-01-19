import json

from huesdk.generics import hexa_to_xy,rgb_to_xy


class Light:

    def __init__(self, sdk, light_id, **kwargs):
        """
        :param str light_id: id of the light
        """
        self.sdk = sdk

        self.id_ = light_id
        self.name = kwargs.get('name', None)

        if 'state' in kwargs:
            self.is_on = kwargs['state'].get('on', False)
            self.bri = kwargs['state'].get('bri', None)
            self.hue = kwargs['state'].get('hue', None)
            self.sat = kwargs['state'].get('sat', None)
            self.colormode = kwargs['state'].get('colormode', None)
            self.ct = kwargs['state'].get('ct', None)
            self.xy = kwargs['state'].get('xy', [])

    def _put(self, body):
        response = self.sdk.put(uri=f'/{self.sdk.username}/lights/{self.id_}', body=json.dumps(body))

    def _put_state(self, body):
        response = self.sdk.put(uri=f'/{self.sdk.username}/lights/{self.id_}/state', body=json.dumps(body))

    def on(self, transition=4):
        if self.is_on is False:
            self._put_state({"on": True, "transitiontime": transition})
            self.is_on = True

    def off(self, transition=4):
        if self.is_on is True:
            self._put_state({"on": False, "transitiontime": transition})
            self.is_on = False

    def set_brightness(self, value, transition=4):
        self._put_state({"bri": value, "transitiontime": transition})

    def set_saturation(self, value, transition=4):
        self._put_state({"sat": value, "transitiontime": transition})

    def set_color(self, hue=None, hexa=None, transition=4):
        if hue is not None:
            self._put_state({"hue": hue, "transitiontime": transition})
        elif hexa is not None:
            xy = hexa_to_xy(hexa)
            self._put_state({"xy": xy, "transitiontime": transition})

    def set_states(self, hue=None, bri=None, sat=None, xy=None, ct=None, colormode=None):
        states = {}
        if hue and hue != self.hue:
            states["hue"] = hue

        if sat and sat != self.sat:
            states["sat"] = sat
        
        if bri and bri != self.bri:
            states["bri"] = bri

        if xy:
            states["xy"] = xy

        if colormode and colormode != self.colormode:
            states["colormode"] = colormode

        if ct and ct != self.ct:
            states["ct"] = ct

        if states:
            self._put_state(states)

    def set_name(self, name):
        self._put({"name": name})
        self.name = name

    def set_colormode(self, colormode):
        self._put({"colormode": colormode})
        self.colormode = colormode
