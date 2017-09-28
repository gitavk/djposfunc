from django.db.models import Func


class Position(Func):
    """
    Return start position of substring in the field.
    """
    function = 'POSITION'
    template = "%(function)s(LOWER('%(substring)s') in LOWER(%(expressions)s))"
    template_sqlite = "instr(lower(%(expressions)s), lower('%(substring)s'))"

    def __init__(self, expression, substring):
        super(Position, self).__init__(expression, substring=substring)

    def as_sqlite(self, compiler, connection):
        return self.as_sql(compiler, connection, template=self.template_sqlite)
