import Constant as c


class CurveStrategyable():
    def __init__(self, item):
        self.item = item

    def tikzify_strategy(self, is_linestring):
        is_loop = self.item["line"]["strategy"]["loop"]
        connect_to = '.center' if (not is_linestring) or self.item["line"]["connect_to"] == c.LineConnectTo.NODE_CENTRE else ''
        if is_linestring:
            loop = '' if not is_loop else f', loop, min distance={self.item["line"]["strategy"]["loop_size"]}cm'
        o_angle = self.item["line"]["strategy"]["out_angle"]
        i_angle = self.item["line"]["strategy"]["in_angle"]
        join_symbol = {
            c.StrategyType.SEGMENTS: f'{connect_to})--(',
            c.StrategyType.HOZVERT: f'{connect_to})-|(',
            c.StrategyType.VERTHOZ: f'{connect_to})|-(',
            c.StrategyType.IO_ANGLE: f'{connect_to}) to[out={o_angle}, in={i_angle}{loop}] (' if is_linestring else f'.center) to[out={o_angle}, in={i_angle}] (',
            c.StrategyType.BENDED_LEFT: f'{connect_to}) to[bend left={self.item["line"]["strategy"]["bend_angle"]}] (',
            c.StrategyType.BENDED_RIGHT: f'{connect_to}) to[bend right={self.item["line"]["strategy"]["bend_angle"]}] (',
            c.StrategyType.SMOOTH: '.center)('
        }
        if self.item["line"]["strategy"]["type"] in [c.StrategyType.SEGMENTS, c.StrategyType.HOZVERT, c.StrategyType.VERTHOZ]:
            if self.item["line"]["strategy"]["rounded_corners"] != 0.0:
                return f'rounded corners={self.item["line"]["strategy"]["rounded_corners"]}',\
                '(' + join_symbol[self.item["line"]["strategy"]["type"]].join(self.item["definition"]) + f'{connect_to})'
            return '', '(' + join_symbol[self.item["line"]["strategy"]["type"]].join(self.item["definition"]) + f'{connect_to})'
        if self.item["line"]["strategy"]["type"] == c.StrategyType.SMOOTH:
            smooth_option = 'smooth' if is_linestring else 'smooth cycle'
            if self.item["line"]["strategy"]["smooth_tension"] == c.StrategyDefault().SMOOTH_TENSION:
                return '', 'plot [%s] coordinates {(%s%s)}' % (smooth_option, join_symbol[c.StrategyType.SMOOTH].join(self.item["definition"]), connect_to)
            return '', 'plot [%s, tension=%s] coordinates {(%s%s)}' % (smooth_option, self.item["line"]["strategy"]["smooth_tension"], join_symbol[c.StrategyType.SMOOTH].join(self.item["definition"]), connect_to)

        # remains i/o angle, bend left and bend right
        return '', '(' + join_symbol[self.item["line"]["strategy"]["type"]].join(self.item["definition"]) + f'{connect_to})'