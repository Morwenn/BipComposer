#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sfml

end_indicator = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'end-indicator.png'))
key_1 = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'key-1.png'))
key_2 = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'key-2.png'))
key_3 = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'key-3.png'))
key_4 = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'key-4.png'))
reader_background = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'reader-background.png'))
reader_head_down = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'reader-head-down.png'))
reader_head_up = sfml.Texture.from_file(os.path.join('bipcomposer', 'textures', 'reader-head-up.png'))
