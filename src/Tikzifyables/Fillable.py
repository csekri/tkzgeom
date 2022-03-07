from Tikzifyables.Colourable.FillColourable import FillColourable
import Constant as c
class Fillable(FillColourable):
    def __init__(self, item):
        FillColourable.__init__(self, self.item)

    def tikzify_fill_pattern(self):
        stars = [c.PatternType.FIVEPOINTED_STARS, c.PatternType.SIXPOINTED_STARS]
        with_area = stars + [c.PatternType.DOTS_EXTRA]
        pattern_colour = '' if not self.tikzify_fill_colour() else 'pattern color=' + self.tikzify_fill_colour()
        options = []
        if self.item["fill"]["pattern"]["type"] == c.PatternType.NONE:
            return ''
        options.append(f'fill={self.tikzify_fill_colour()}')
        if self.item["fill"]["pattern"]["type"] == c.PatternType.SOLID:
            return ', '.join(options)
        if self.item["fill"]["pattern"]["type"] not in c.PATTERN_EXTRAS:
            options.append(f'pattern={self.item["fill"]["pattern"]["type"]}')
            options.append(pattern_colour)
            return ', '.join(options)
        else:
            pattern_options = []
            pattern_options.append(f'distance={self.item["fill"]["pattern"]["distance"]}')
            if self.item["fill"]["pattern"]["type"] in with_area:
                pattern_options.append(f'radius={self.item["fill"]["pattern"]["size"]}')
                if self.item["fill"]["pattern"]["type"] in stars:
                    pattern_options[-1] += ' ex'
            else:
                pattern_options.append(f'line width={self.item["fill"]["pattern"]["size"]}')
            if self.item["fill"]["pattern"]["rotation"] != 0.0:
                pattern_options.append(f'angle={self.item["fill"]["pattern"]["rotation"]}')
            if self.item["fill"]["pattern"]["xshift"] != 0.0:
                pattern_options.append(f'xshift={self.item["fill"]["pattern"]["xshift"]}')
            if self.item["fill"]["pattern"]["yshift"] != 0.0:
                pattern_options.append(f'yshift={self.item["fill"]["pattern"]["yshift"]}')
            if self.item["fill"]["pattern"]["type"] == c.PatternType.FIVEPOINTED_STARS:
                pattern_options.append('points=5')
            if self.item["fill"]["pattern"]["type"] == c.PatternType.SIXPOINTED_STARS:
                pattern_options.append('points=6')
            if self.item["fill"]["pattern"]["type"] in stars:
                return 'pattern={Stars[%s]}, %s' % (', '.join(pattern_options), pattern_colour)
            return 'pattern={%s[%s]}, %s' % (self.item["fill"]["pattern"]["type"], ', '.join(pattern_options), pattern_colour)
