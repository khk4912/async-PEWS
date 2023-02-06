class Utils:
    @staticmethod
    def fn_parseY(loc: float) -> float:
        return (38.9 - loc) * 138.4

    @staticmethod
    def fn_parseX(loc: float) -> float:
        return (loc - 124.5) * 113

    @staticmethod
    def lpad(s: str, l: int) -> str:
        return s.rjust(l, "0")
