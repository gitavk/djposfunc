from django.db.models import Func, F, Value
from django.db.models.functions import Lower


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


class Instr(Func):
    function = 'INSTR'

    def __init__(self, string, substring, insensitive=False, **extra):
        if not substring:
            raise ValueError('Empty substring not allowed')
        if not insensitive:
            expressions = F(string), Value(substring)
        else:
            expressions = Lower(string), Lower(Value(substring))
        super(Instr, self).__init__(*expressions)

    def as_postgresql(self, compiler, connection):
        return self.as_sql(compiler, connection, function='STRPOS')
