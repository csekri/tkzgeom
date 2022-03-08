import Constant as c

class CurveStrategyable(Colourable):
    def __init__(self, item):
        self.item = item

    def tikzify_strategy(self):
        if self.item["line"]["strategy"]["type"] in [c.StrategyType.SEGMENTS, c.StrategyType.HOZVERT, c.StrategyType.VERTHOZ]:
            join_symbol = {c.StrategyType.SEGMENTS: '--', c.StrategyType.HOZVERT: '-|', c.StrategyType.VERTHOZ: '|-'}
            if self.item["line"]["strategy"]["rounded"] != 0.0:
                return f'rounded corners={self.item["line"]["strategy"]["rounded"]}',\
                join_symbol[self.item["line"]["strategy"]["type"]].join(self.item["definition"].values())
        if self.item["line"]["strategy"]["type"] == c.StrategyType.SMOOTH:
            if self.item["line"]["strategy"]["smooth_tension"] == c.StrategyDefault.SMOOTH_TENSION:
                return '', 'plot [smooth] coordinates {(%s)}' % (')('.join(self.item["definition"]))
            return '', 'plot [smooth, tension=%s] coordinates {(%s)}' % (self.item["line"]["strategy"]["smooth_tension"], ')('.join(self.item["definition"]))