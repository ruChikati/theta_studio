import time

import pygame

pygame.joystick.init()

EVENTTYPES = (
    QUIT,
    KEYDOWN,
    KEYUP,
    KEYDOWN2,
    KEYUP2,
    MOUSEMOVE,
    MOUSEWHEEL,
    MOUSEDOWN,
    MOUSEUP,
    WINDOWMOTION,
    VIDEORESIZE,
    DROPFILE,
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYHATMOTION,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    CONTROLLERADDED,
    CONTROLLERREMOVED,
    FINGERMOTION,
    FINGERUP,
    FINGERDOWN,
    FINGERUP2,
    FINGERDOWN2,
    MOUSEUP2,
    MOUSEDOWN2,
    WINDOWMOVED,
    KEYHOLD,
    MOUSEHOLD,
    NONEEVENT,
) = [i for i in range(30)]
_max_type = len(EVENTTYPES)
TYPENAMES = [
    "QUIT",
    "KEYDOWN",
    "KEYUP",
    "KEYDOWN2",
    "KEYUP2",
    "MOUSEMOVE",
    "MOUSEWHEEL",
    "MOUSEDOWN",
    "MOUSEUP",
    "WINDOWMOTION",
    "VIDEORESIZE",
    "DROPFILE",
    "JOYAXISMOTION",
    "JOYBALLMOTION",
    "JOYHATMOTION",
    "JOYBUTTONDOWN",
    "JOYBUTTONUP",
    "CONTROLLERADDED",
    "CONTROLLERREMOVED",
    "FINGERMOTION",
    "FINGERUP",
    "FINGERDOWN",
    "FINGERUP2",
    "FINGERDOWN2",
    "MOUSEUP2",
    "MOUSEDOWN2",
    "WINDOWMOVED",
    "NONEEVENT",
]
KEYS = (
    BACKSPACE,
    TAB,
    CLEAR,
    RETURN,
    PAUSE,
    ESCAPE,
    SPACE,
    EXCLAIM,
    DOUBLEQUOTE,
    HASH,
    DOLLAR,
    AMPERSAND,
    QUOTE,
    LEFTPAREN,
    RIGHTPAREN,
    ASTERISK,
    PLUS,
    COMMA,
    MINUS,
    PERIOD,
    SLASH,
    ZERO,
    ONE,
    TWO,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
    COLON,
    SEMICOLON,
    LESS,
    EQUALS,
    GREATER,
    QUESTION,
    AT,
    LEFTBRACKET,
    BACKSLASH,
    RIGHTBRACKET,
    CARET,
    UNDERSCORE,
    BACKQUOTE,
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    J,
    K,
    L,
    M,
    N,
    O,
    P,
    Q,
    R,
    S,
    T,
    U,
    V,
    W,
    X,
    Y,
    Z,
    DELETE,
    KP_ZERO,
    KP_ONE,
    KP_TWO,
    KP_THREE,
    KP_FOUR,
    KP_FIVE,
    KP_SIX,
    KP_SEVEN,
    KP_EIGHT,
    KP_NINE,
    KP_PERIOD,
    KP_DIVIDE,
    KP_MULTIPLY,
    KP_MINUS,
    KP_PLUS,
    KP_ENTER,
    KP_EQUALS,
    UP,
    DOWN,
    RIGHT,
    LEFT,
    INSERT,
    HOME,
    END,
    PAGEUP,
    PAGEDOWN,
    F1,
    F2,
    F3,
    F4,
    F5,
    F6,
    F7,
    F8,
    F9,
    F10,
    F11,
    F12,
    F13,
    F14,
    F15,
    NUMLOCK,
    CAPSLOCK,
    SCROLLLOCK,
    RSHIFT,
    LSHIFT,
    RCTRL,
    LCTRL,
    RALT,
    LALT,
    RMETA,
    LMETA,
    LSUPER,
    RSUPER,
    MODE,
    HELP,
    PRINT,
    SYSREQ,
    BREAK,
    MENU,
    POWER,
    EURO,
) = (
    pygame.K_BACKSPACE,
    pygame.K_TAB,
    pygame.K_CLEAR,
    pygame.K_RETURN,
    pygame.K_PAUSE,
    pygame.K_ESCAPE,
    pygame.K_SPACE,
    pygame.K_EXCLAIM,
    pygame.K_QUOTEDBL,
    pygame.K_HASH,
    pygame.K_DOLLAR,
    pygame.K_AMPERSAND,
    pygame.K_QUOTE,
    pygame.K_LEFTPAREN,
    pygame.K_RIGHTPAREN,
    pygame.K_ASTERISK,
    pygame.K_PLUS,
    pygame.K_COMMA,
    pygame.K_MINUS,
    pygame.K_PERIOD,
    pygame.K_SLASH,
    pygame.K_0,
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
    pygame.K_COLON,
    pygame.K_SEMICOLON,
    pygame.K_LESS,
    pygame.K_EQUALS,
    pygame.K_GREATER,
    pygame.K_QUESTION,
    pygame.K_AT,
    pygame.K_LEFTBRACKET,
    pygame.K_BACKSLASH,
    pygame.K_RIGHTBRACKET,
    pygame.K_CARET,
    pygame.K_UNDERSCORE,
    pygame.K_BACKQUOTE,
    pygame.K_a,
    pygame.K_b,
    pygame.K_c,
    pygame.K_d,
    pygame.K_e,
    pygame.K_f,
    pygame.K_g,
    pygame.K_h,
    pygame.K_i,
    pygame.K_j,
    pygame.K_k,
    pygame.K_l,
    pygame.K_m,
    pygame.K_n,
    pygame.K_o,
    pygame.K_p,
    pygame.K_q,
    pygame.K_r,
    pygame.K_s,
    pygame.K_t,
    pygame.K_u,
    pygame.K_v,
    pygame.K_w,
    pygame.K_x,
    pygame.K_y,
    pygame.K_z,
    pygame.K_DELETE,
    pygame.K_KP0,
    pygame.K_KP1,
    pygame.K_KP2,
    pygame.K_KP3,
    pygame.K_KP4,
    pygame.K_KP5,
    pygame.K_KP6,
    pygame.K_KP7,
    pygame.K_KP8,
    pygame.K_KP9,
    pygame.K_KP_PERIOD,
    pygame.K_KP_DIVIDE,
    pygame.K_KP_MULTIPLY,
    pygame.K_KP_MINUS,
    pygame.K_KP_PLUS,
    pygame.K_KP_ENTER,
    pygame.K_KP_EQUALS,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_RIGHT,
    pygame.K_LEFT,
    pygame.K_INSERT,
    pygame.K_HOME,
    pygame.K_END,
    pygame.K_PAGEUP,
    pygame.K_PAGEDOWN,
    pygame.K_F1,
    pygame.K_F2,
    pygame.K_F3,
    pygame.K_F4,
    pygame.K_F5,
    pygame.K_F6,
    pygame.K_F7,
    pygame.K_F8,
    pygame.K_F9,
    pygame.K_F10,
    pygame.K_F11,
    pygame.K_F12,
    pygame.K_F13,
    pygame.K_F14,
    pygame.K_F15,
    pygame.K_NUMLOCK,
    pygame.K_CAPSLOCK,
    pygame.K_SCROLLOCK,
    pygame.K_RSHIFT,
    pygame.K_LSHIFT,
    pygame.K_RCTRL,
    pygame.K_LCTRL,
    pygame.K_RALT,
    pygame.K_LALT,
    pygame.K_RMETA,
    pygame.K_LMETA,
    pygame.K_LSUPER,
    pygame.K_RSUPER,
    pygame.K_MODE,
    pygame.K_HELP,
    pygame.K_PRINT,
    pygame.K_SYSREQ,
    pygame.K_BREAK,
    pygame.K_MENU,
    pygame.K_POWER,
    pygame.K_EURO,
)
MODS = (
    MOD_NONE,
    MOD_LSHIFT,
    MOD_RSHIFT,
    MOD_SHIFT,
    MOD_LCTRL,
    MOD_RCTRL,
    MOD_CTRL,
    MOD_LALT,
    MOD_RALT,
    MOD_ALT,
    MOD_LMETA,
    MOD_RMETA,
    MOD_META,
    MOD_CAPSLOCK,
    MOD_NUMLOCK,
    MOD_MODE,
) = (
    pygame.KMOD_NONE,
    pygame.KMOD_LSHIFT,
    pygame.KMOD_RSHIFT,
    pygame.KMOD_SHIFT,
    pygame.KMOD_LCTRL,
    pygame.KMOD_RCTRL,
    pygame.KMOD_CTRL,
    pygame.KMOD_LALT,
    pygame.KMOD_RALT,
    pygame.KMOD_ALT,
    pygame.KMOD_LMETA,
    pygame.KMOD_RMETA,
    pygame.KMOD_META,
    pygame.KMOD_CAPS,
    pygame.KMOD_NUM,
    pygame.KMOD_MODE,
)

LAG_TIME = 0.8  # amount of time in between two accepted keystrokes to count as KEY2/MOUSE2/FINGER2, in seconds


def custom_event_type() -> int:
    global _max_type
    _max_type += 1
    return _max_type - 1


class Event:
    def __init__(self, type: int, attributes: dict | None = None, **kwargs):
        self.attr = {}
        self.attr.update(attributes if attributes is not None else {})
        self.attr.update(kwargs)
        self.type = type

    def __getitem__(self, item):
        return self.attr[item]

    def __eq__(self, other):
        return (self.attr, self.type) == (other.attr, other.type)

    def __repr__(self):
        return f"Event({TYPENAMES[self.type]}), {self.attr}"

    def __getattr__(self, item):
        return self.attr[item]


class Input:
    def __init__(self, cache_length=128):
        self.controllers = []
        self.cache = [[], []]  # time, event
        self.length = cache_length
        self.posted_events = []
        self._held_keys = {"keys": [], "mouse": []}
        self._hold_start = {"keys": {}, "mouse": {}}
        self.mx = 0
        self.my = 0
        self.m_pos = (self.mx, self.my)

    def post(self, event: Event):
        self.posted_events.append(event)

    def get(self) -> list[Event]:
        self.controllers = [
            pygame.joystick.Joystick(c) for c in range(pygame.joystick.get_count())
        ]
        self.m_pos = self.mx, self.my = pygame.mouse.get_pos()

        return_list = []
        cur_time = time.time()
        while len(self.cache[0]) >= self.length:
            del self.cache[1][0]
            del self.cache[0][0]
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    if len(
                        [
                            cache_event
                            for t, cache_event in zip(self.cache[0], self.cache[1])
                            if t >= cur_time - LAG_TIME
                            and cache_event
                            == Event(
                                KEYDOWN,
                                {
                                    "key": event.key,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                },
                            )
                        ]
                    ):
                        return_list.append(
                            Event(
                                KEYDOWN2,
                                {
                                    "key": event.key,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                KEYDOWN2,
                                {
                                    "key": event.key,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                        return_list.append(
                            Event(
                                KEYDOWN,
                                {
                                    "key": event.key,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                KEYDOWN,
                                {
                                    "key": event.key,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                        if event.key not in self._held_keys["keys"]:
                            self._held_keys["keys"].append(event.key)
                            self._hold_start["keys"][
                                event.key
                            ] = cur_time  # must always set this!!!
                    else:
                        return_list.append(
                            Event(
                                KEYDOWN,
                                {
                                    "key": event.key,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                KEYDOWN,
                                {
                                    "key": event.key,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                        if event.key not in self._held_keys["keys"]:
                            self._held_keys["keys"].append(event.key)
                            self._hold_start["keys"][event.key] = cur_time
                case pygame.MOUSEBUTTONDOWN:
                    if len(
                        [
                            cache_event
                            for t, cache_event in zip(self.cache[0], self.cache[1])
                            if t >= cur_time - LAG_TIME
                            and cache_event
                            == Event(
                                MOUSEDOWN, {"pos": event.pos, "button": event.button}
                            )
                        ]
                    ):
                        return_list.append(
                            Event(
                                MOUSEDOWN2, {"pos": event.pos, "button": event.button}
                            )
                        )
                        self.cache[1].append(
                            Event(
                                MOUSEDOWN2, {"pos": event.pos, "button": event.button}
                            )
                        )
                        self.cache[0].append(cur_time)
                        return_list.append(
                            Event(MOUSEDOWN, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[1].append(
                            Event(MOUSEDOWN, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[0].append(cur_time)
                        if event.button not in self._held_keys["mouse"]:
                            self._held_keys["mouse"].append(event.button)
                            self._hold_start["mouse"][event.button] = cur_time
                    else:
                        return_list.append(
                            Event(MOUSEDOWN, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[1].append(
                            Event(MOUSEDOWN, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[0].append(cur_time)
                        if event.button not in self._held_keys["mouse"]:
                            self._held_keys["mouse"].append(event.button)
                            self._hold_start["mouse"][event.button] = cur_time
                case pygame.MOUSEBUTTONUP:
                    if len(
                        [
                            cache_event
                            for t, cache_event in zip(self.cache[0], self.cache[1])
                            if t >= cur_time - LAG_TIME
                            and cache_event
                            == Event(
                                MOUSEUP, {"pos": event.pos, "button": event.button}
                            )
                        ]
                    ):
                        return_list.append(
                            Event(MOUSEUP2, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[1].append(
                            Event(MOUSEUP2, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[0].append(cur_time)
                        return_list.append(
                            Event(MOUSEUP, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[1].append(
                            Event(MOUSEUP, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[0].append(cur_time)
                        self._held_keys["mouse"].remove(event.button)
                    else:
                        return_list.append(
                            Event(MOUSEUP, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[1].append(
                            Event(MOUSEUP, {"pos": event.pos, "button": event.button})
                        )
                        self.cache[0].append(cur_time)
                        self._held_keys["mouse"].remove(event.button)
                case pygame.KEYUP:
                    if len(
                        [
                            cache_event
                            for t, cache_event in zip(self.cache[0], self.cache[1])
                            if t >= cur_time - LAG_TIME
                            and cache_event
                            == Event(KEYUP, {"key": event.key, "mod": event.mod})
                        ]
                    ):
                        return_list.append(
                            Event(KEYUP2, {"key": event.key, "mod": event.mod})
                        )
                        self.cache[1].append(
                            Event(KEYUP2, {"key": event.key, "mod": event.mod})
                        )
                        self.cache[0].append(cur_time)
                        return_list.append(
                            Event(KEYUP, {"key": event.key, "mod": event.mod})
                        )
                        self.cache[1].append(
                            Event(KEYUP, {"key": event.key, "mod": event.mod})
                        )
                        self.cache[0].append(cur_time)
                        self._held_keys["keys"].remove(event.key)
                    else:
                        return_list.append(
                            Event(KEYUP, {"key": event.key, "mod": event.mod})
                        )
                        self.cache[1].append(
                            Event(KEYUP, {"key": event.key, "mod": event.mod})
                        )
                        self.cache[0].append(cur_time)
                        self._held_keys["keys"].remove(event.key)
                case pygame.QUIT:
                    return_list.append(Event(QUIT))
                    self.cache[1].append(Event(QUIT))
                    self.cache[0].append(cur_time)
                case pygame.MOUSEMOTION:
                    return_list.append(
                        Event(
                            MOUSEMOVE,
                            {
                                "pos": event.pos,
                                "buttons": event.buttons,
                                "rel": event.rel,
                            },
                        )
                    )
                    self.cache[1].append(
                        Event(
                            MOUSEMOVE,
                            {
                                "pos": event.pos,
                                "buttons": event.buttons,
                                "rel": event.rel,
                            },
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.JOYAXISMOTION:
                    return_list.append(
                        Event(
                            JOYAXISMOTION,
                            {
                                "instance_id": event.instance_id,
                                "axis": event.axis,
                                "value": event.value,
                            },
                        )
                    )
                    self.cache[1].append(
                        Event(
                            JOYAXISMOTION,
                            {
                                "instance_id": event.instance_id,
                                "axis": event.axis,
                                "value": event.value,
                            },
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.JOYBALLMOTION:
                    return_list.append(
                        Event(
                            JOYBALLMOTION,
                            {
                                "instance_id": event.instance_id,
                                "ball": event.ball,
                                "rel": event.rel,
                            },
                        )
                    )
                    self.cache[1].append(
                        Event(
                            JOYBALLMOTION,
                            {
                                "instance_id": event.instance_id,
                                "ball": event.ball,
                                "rel": event.rel,
                            },
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.JOYHATMOTION:
                    return_list.append(
                        Event(
                            JOYHATMOTION,
                            {
                                "instance_id": event.instance_id,
                                "hat": event.hat,
                                "value": event.value,
                            },
                        )
                    )
                    self.cache[1].append(
                        Event(
                            JOYHATMOTION,
                            {
                                "instance_id": event.instance_id,
                                "hat": event.hat,
                                "value": event.value,
                            },
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.JOYBUTTONUP:
                    return_list.append(
                        Event(
                            JOYBUTTONUP,
                            {"instance_id": event.instance_id, "button": event.button},
                        )
                    )
                    self.cache[1].append(
                        Event(
                            JOYBUTTONUP,
                            {"instance_id": event.instance_id, "button": event.button},
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.JOYBUTTONDOWN:
                    return_list.append(
                        Event(
                            JOYBUTTONDOWN,
                            {"instance_id": event.instance_id, "button": event.button},
                        )
                    )
                    self.cache[1].append(
                        Event(
                            JOYBUTTONDOWN,
                            {"instance_id": event.instance_id, "button": event.button},
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.MOUSEWHEEL:
                    return_list.append(
                        Event(
                            MOUSEWHEEL,
                            {"flipped": event.flipped, "x": event.x, "y": event.y},
                        )
                    )
                    self.cache[1].append(
                        Event(
                            MOUSEWHEEL,
                            {"flipped": event.flipped, "x": event.x, "y": event.y},
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.JOYDEVICEADDED:
                    return_list.append(
                        Event(CONTROLLERADDED, {"device_id": event.device_id})
                    )
                    self.controllers = [
                        pygame.joystick.Joystick(c)
                        for c in range(pygame.joystick.get_count())
                    ]
                    self.cache[1].append(
                        Event(CONTROLLERADDED, {"device_id": event.device_id})
                    )
                    self.cache[0].append(cur_time)
                case pygame.JOYDEVICEREMOVED:
                    return_list.append(
                        Event(CONTROLLERREMOVED, {"device_id": event.device_id})
                    )
                    self.controllers = [
                        pygame.joystick.Joystick(c)
                        for c in range(pygame.joystick.get_count())
                    ]
                    self.cache[1].append(
                        Event(CONTROLLERREMOVED, {"device_id": event.device_id})
                    )
                    self.cache[0].append(cur_time)
                case pygame.WINDOWMOVED:
                    return_list.append(Event(WINDOWMOVED, {"x": event.x, "y": event.y}))
                    self.cache[1].append(
                        Event(WINDOWMOVED, {"x": event.x, "y": event.y})
                    )
                    self.cache[0].append(cur_time)
                case pygame.VIDEORESIZE:
                    return_list.append(
                        Event(
                            VIDEORESIZE,
                            {"size": event.size, "w": event.w, "h": event.h},
                        )
                    )
                    self.cache[1].append(
                        Event(
                            VIDEORESIZE,
                            {"size": event.size, "w": event.w, "h": event.h},
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.DROPFILE:
                    return_list.append(Event(DROPFILE, {"file": event.file}))
                    self.cache[1].append(Event(DROPFILE, {"file": event.file}))
                    self.cache[0].append(cur_time)
                case pygame.FINGERMOTION:
                    return_list.append(
                        Event(
                            FINGERMOTION,
                            {
                                "touch_id": event.touch_id,
                                "finger_id": event.finger_id,
                                "x": event.x,
                                "y": event.y,
                                "dx": event.dx,
                                "dy": event.dy,
                            },
                        )
                    )
                    self.cache[1].append(
                        Event(
                            FINGERMOTION,
                            {
                                "touch_id": event.touch_id,
                                "finger_id": event.finger_id,
                                "x": event.x,
                                "y": event.y,
                                "dx": event.dx,
                                "dy": event.dy,
                            },
                        )
                    )
                    self.cache[0].append(cur_time)
                case pygame.FINGERUP:
                    if len(
                        [
                            cache_event
                            for t, cache_event in zip(self.cache[0], self.cache[1])
                            if t >= cur_time - LAG_TIME
                            and cache_event
                            == Event(
                                FINGERUP,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        ]
                    ):
                        return_list.append(
                            Event(
                                FINGERUP2,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                FINGERUP2,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                        return_list.append(
                            Event(
                                FINGERUP,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                FINGERUP,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                    else:
                        return_list.append(
                            Event(
                                FINGERUP,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                FINGERUP,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                case pygame.FINGERDOWN:
                    if len(
                        [
                            cache_event
                            for t, cache_event in zip(self.cache[0], self.cache[1])
                            if t >= cur_time - LAG_TIME
                            and cache_event
                            == Event(
                                FINGERDOWN,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        ]
                    ):
                        return_list.append(
                            Event(
                                FINGERDOWN2,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                FINGERDOWN2,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                        return_list.append(
                            Event(
                                FINGERDOWN,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                FINGERDOWN,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)
                    else:
                        return_list.append(
                            Event(
                                FINGERDOWN,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[1].append(
                            Event(
                                FINGERDOWN,
                                {
                                    "touch_id": event.touch_id,
                                    "finger_id": event.finger_id,
                                    "x": event.x,
                                    "y": event.y,
                                    "dx": event.dx,
                                    "dy": event.dy,
                                },
                            )
                        )
                        self.cache[0].append(cur_time)

        for key in self._held_keys["keys"]:
            self.posted_events.append(
                Event(
                    KEYHOLD,
                    {"key": key, "time": cur_time - self._hold_start["keys"][key]},
                )
            )
        for button in self._held_keys["mouse"]:
            self.posted_events.append(
                Event(
                    MOUSEHOLD,
                    {
                        "button": button,
                        "time": cur_time - self._hold_start["mouse"][button],
                    },
                )
            )
        for event in self.posted_events:
            return_list.append(event)
        self.posted_events *= 0
        return return_list

    def get_mpos(self) -> tuple[int, int]:
        return self.mx, self.my
