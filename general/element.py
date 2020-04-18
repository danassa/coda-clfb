

class Element:

    def __init__(self, is_paragraph, block):
        self.is_paragraph = is_paragraph
        self.block = block

    def chars_count(self):
        chars = 0
        if self.is_paragraph:
            chars = len(self.block.text)
        else:
            for r in self.block.rows:
                for c in r.cells:
                    chars = chars + len(c.text)
        return chars

    def delete(self):
        if self.is_paragraph:
            p = self.block._element
            p.getparent().remove(p)
            p._p = p._element = None
        else:
            self.block._element.getparent().remove(self.block._element)

