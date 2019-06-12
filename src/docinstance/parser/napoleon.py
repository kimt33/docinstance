"""Napoleon parser."""
from docinstance.content.description import DocDescription, DocParagraph
from docinstance.content.section import (  # pylint: disable=E0611
    Attributes,
    DocSection,
    Examples,
    ExtendedSummary,
    Methods,
    Notes,
    OtherParameters,
    Parameters,
    Raises,
    References,
    Returns,
    SeeAlso,
    Summary,
    Warnings,
    Warns,
    Yields,
)
from docinstance.docstring import Docstring
from docinstance.utils import wrap, wrap_indent_subsequent
from sphinxcontrib.napoleon.docstring import GoogleDocstring, NumpyDocstring, _directive_regex


class GoogleDocstringDocinstance(GoogleDocstring):
    def _parse_attributes_section(self, section):
        fields = self._consume_fields()
        return [
            Attributes(
                [
                    DocDescription(field[0], types=field[1] if field[1] else None, descs=field[2])
                    for field in fields
                ]
            )
        ]

    def _parse_keyword_arguments_section(self, section):
        fields = self._consume_fields()
        return [
            DocSection(
                "keyword arguments",
                [
                    DocDescription(field[0], types=field[1] if field[1] else None, descs=field[2])
                    for field in fields
                ],
            )
        ]

    def _parse_other_parameters_section(self, section):
        fields = self._consume_fields()
        return [
            OtherParameters(
                [
                    DocDescription(field[0], types=field[1] if field[1] else None, descs=field[2])
                    for field in fields
                ]
            )
        ]

    def _parse_parameters_section(self, section):
        fields = self._consume_fields()
        return [
            Parameters(
                [
                    DocDescription(field[0], types=field[1] if field[1] else None, descs=field[2])
                    for field in fields
                ]
            )
        ]

    def _parse_returns_section(self, section):
        fields = self._consume_returns_section()
        return [
            Returns(
                [
                    DocDescription(field[1], descs=field[2])
                    if field[0] == ""
                    else DocDescription(field[0], types=field[1], descs=field[2])
                    for field in fields
                ]
            )
        ]

    def _parse_yields_section(self, section):
        fields = self._consume_returns_section()
        return [
            Yields(
                [
                    DocDescription(field[1], descs=field[2])
                    if field[0] == ""
                    else DocDescription(field[0], types=field[1], descs=field[2])
                    for field in fields
                ]
            )
        ]

    def _parse_methods_section(self, section):
        fields = self._consume_fields(parse_type=False)
        return [Methods([DocDescription(field[0], descs=field[2]) for field in fields])]

    def _parse_raises_section(self, section):
        fields = self._consume_fields(parse_type=False, prefer_type=True)
        return [Raises([DocDescription(field[1], descs=field[2]) for field in fields])]

    def _parse_see_also_section(self, section):
        # type (unicode) -> List[unicode]
        lines = self._consume_to_next_section()
        return [SeeAlso(lines)]

    def _parse_warns_section(self, section):
        fields = self._consume_fields()
        return [
            Warns(
                [
                    DocDescription(field[0], types=field[1] if field[1] else None, descs=field[2])
                    for field in fields
                ]
            )
        ]

    def _parse_generic_section(self, section, use_admonition):
        lines = self._strip_empty(self._consume_to_next_section())
        lines = self._dedent(lines)
        if use_admonition:
            lines = self._indent(lines, 3)
        return [DocSection(section, [DocParagraph(line, num_newlines_end=1) for line in lines])]

    def _parse_examples_section(self, section):
        labels = {"example": "Example", "examples": "Examples"}
        use_admonition = self._config.napoleon_use_admonition_for_examples
        label = labels.get(section.lower(), section)
        return self._parse_generic_section(label, use_admonition)

    def _parse_notes_section(self, section):
        use_admonition = self._config.napoleon_use_admonition_for_notes
        return self._parse_generic_section("Notes", use_admonition)

    def _parse_references_section(self, section):
        use_admonition = self._config.napoleon_use_admonition_for_references
        return self._parse_generic_section("References", use_admonition)


class NumpyDocstringDocinstance(NumpyDocstring, GoogleDocstringDocinstance):
    # _parse_admonition = GoogleDocstringDocinstance._parse_admonition
    # _parse_generic_section = GoogleDocstringDocinstance._parse_generic_section
    # _parse_attributes_section = GoogleDocstringDocinstance._parse_attributes_section
    # _parse_examples_section = GoogleDocstringDocinstance._parse_examples_section
    # _parse_keyword_arguments_section = GoogleDocstringDocinstance._parse_keyword_arguments_section
    # _parse_methods_section = GoogleDocstringDocinstance._parse_methods_section
    # _parse_notes_section = GoogleDocstringDocinstance._parse_notes_section
    # _parse_other_parameters_section = GoogleDocstringDocinstance._parse_other_parameters_section
    # _parse_parameters_section = GoogleDocstringDocinstance._parse_parameters_section
    # _parse_returns_section = GoogleDocstringDocinstance._parse_returns_section
    # _parse_raises_section = GoogleDocstringDocinstance._parse_raises_section
    # _parse_references_section = GoogleDocstringDocinstance._parse_references_section
    # _parse_see_also_section = GoogleDocstringDocinstance._parse_see_also_section
    # _parse_warns_section = GoogleDocstringDocinstance._parse_warns_section
    # _parse_yields_section = GoogleDocstringDocinstance._parse_yields_section
    def _parse_see_also_section(self, section):
        # type: (unicode) -> List[unicode]
        lines = self._consume_to_next_section()
        try:
            return self._parse_numpydoc_see_also_section(lines)
        except ValueError:
            lines = self._strip_empty(lines)
            lines = self._dedent(lines)
            return [SeeAlso(lines)]

    def _parse_numpydoc_see_also_section(self, content):  # type: (List[unicode]) -> List[unicode]
        """
        Derived from the NumpyDoc implementation of _parse_see_also.

        See Also
        --------
        func_name : Descriptive text
            continued text
        another_func_name : Descriptive text
        func_name1, func_name2, :meth:`func_name`, func_name3

        """
        items = []

        def parse_item_name(text):
            # type: (unicode) -> Tuple[unicode, unicode]
            """Match ':role:`name`' or 'name'"""
            m = self._name_rgx.match(text)  # type: ignore
            if m:
                g = m.groups()
                if g[1] is None:
                    return g[3], None
                else:
                    return g[2], g[1]
            raise ValueError("%s is not a item name" % text)

        def push_item(name, rest):
            # type: (unicode, List[unicode]) -> None
            if not name:
                return
            name, role = parse_item_name(name)
            items.append((name, list(rest), role))
            del rest[:]

        current_func = None
        rest = []  # type: List[unicode]

        for line in content:
            if not line.strip():
                continue

            m = self._name_rgx.match(line)  # type: ignore
            if m and line[m.end() :].strip().startswith(":"):
                push_item(current_func, rest)
                current_func, line = line[: m.end()], line[m.end() :]
                rest = [line.split(":", 1)[1].strip()]
                if not rest[0]:
                    rest = []
            elif not line.startswith(" "):
                push_item(current_func, rest)
                current_func = None
                if "," in line:
                    for func in line.split(","):
                        if func.strip():
                            push_item(func, [])
                elif line.strip():
                    current_func = line
            elif current_func is not None:
                rest.append(line.strip())
        push_item(current_func, rest)

        if not items:
            return []

        roles = {
            "method": "meth",
            "meth": "meth",
            "function": "func",
            "func": "func",
            "class": "class",
            "exception": "exc",
            "exc": "exc",
            "object": "obj",
            "obj": "obj",
            "module": "mod",
            "mod": "mod",
            "data": "data",
            "constant": "const",
            "const": "const",
            "attribute": "attr",
            "attr": "attr",
        }  # type: Dict[unicode, unicode]
        if self._what is None:
            func_role = "obj"  # type: unicode
        else:
            func_role = roles.get(self._what, "")
        lines = []  # type: List[unicode]
        for func, desc, role in items:
            if not role and func_role:
                role = func_role

            lines.append(DocSeeAlsoEntryNumpy(func, role, desc))

        return [SeeAlso(lines)]


class DocSeeAlsoEntryNumpy(DocDescription):
    def __init__(self, name, role, desc):
        super().__init__(name, types=role, descs=desc)
        if len(self.descs) > 1:
            raise ValueError
        if len(self.types) > 1:
            raise ValueError

    def make_docstring_numpy(self, width, indent_level, tabsize):
        if not self.descs:
            lines = wrap(self.name, width=width, indent_level=indent_level, tabsize=tabsize)
        elif self.types:
            lines = wrap(
                "{0} : {1}".format(self.name, self.descs[0]),
                width=width,
                indent_level=indent_level,
                tabsize=tabsize,
            )
        return "\n".join(lines) + "\n"

    def make_docstring_rst(self, width, indent_level, tabsize):
        role = self.types
        func = self.name
        desc = self.descs[0]

        if role:
            link = ":%s:`%s`".format(role, func)
        else:
            link = "`%s`_".format(func)

        output = "\n".join(wrap(link, width=width, indent_level=indent_level, tabsize=tabsize))
        output += "\n"
        output += "\n".join(wrap(desc[0], width=width, indent_level=indent_level, tabsize=tabsize))
        output += "\n"

        return output


def parse_numpy(docstring, contains_quotes=False):
    """Parse a docstring in Numpy format using Napoleon into Docstring instance."""
    parsed_content = [i for i in NumpyDocstringDocinstance(docstring)._parsed_lines if i]
    if isinstance(parsed_content[0], str):
        parsed_content[0] = Summary(parsed_content[0])
    # check for any other strings
    string_contents = [True if isinstance(i, str) else False for i in parsed_content]
    if any(string_contents):
        start_ind = string_contents.index(True)
        end_ind = len(string_contents) - string_contents[::-1].index(True) - 1
        if not all(string_contents[start_ind : end_ind + 1]):
            raise ValueError
        parsed_content = (
            parsed_content[:start_ind]
            + [ExtendedSummary(parsed_content[start_ind : end_ind + 1])]
            + parsed_content[end_ind + 1 :]
        )
    return Docstring(parsed_content)


def parse_google(docstring, contains_quotes=False):
    """Parse a docstring in Google format using Napoleon into Docstring instance."""
    return GoogleDocstringDocinstance(docstring)._parsed_lines
