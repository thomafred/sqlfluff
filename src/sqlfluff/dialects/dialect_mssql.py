"""The Microsoft SQL dialect"""

from ..parser import (
    OneOf, Ref, Sequence, Bracketed, Anything, BaseSegment, NamedSegment, Delimited, GreedyUntil,
    StartsWith, Indent, Dedent
)

from ..dialects import dialect_ansi
from .dialect_ansi import ansi_dialect

mssql_dialect = ansi_dialect.copy_as('mssql')

mssql_dialect.add(
    BracketedIdentifierStatement=Bracketed(Ref('NakedIdentifierSegment'), square=True)
)

mssql_dialect.replace(
    SingleIdentifierGrammar=OneOf(
        Ref('NakedIdentifierSegment'),
        Ref('QuotedIdentifierSegment'),
        Ref('BracketedIdentifierStatement')
    )
)

@mssql_dialect.segment(replace=True)
class ObjectReferenceSegment(dialect_ansi.ObjectReferenceSegment):
    """A reference to an object."""
    type = 'object_reference'
    # match grammar (don't allow whitespace)
    match_grammar = Delimited(
        Ref('SingleIdentifierGrammar'),
        delimiter=OneOf(
            Ref('DotSegment'),
            Sequence(
                Ref('DotSegment')
            )
        ),
        terminator=OneOf(
            Ref('_NonCodeSegment'), Ref('CommaSegment'),
            Ref('CastOperatorSegment'),
            Ref('StartBracketSegment'), Ref('BinaryOperatorGramar'), Ref('ColonSegment'),
            Ref('SemicolonSegment')
        ),
        code_only=False
    )
