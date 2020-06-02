import QCM


#
# Utilitary functions
#


def get_block(text, block_open_char, block_close_char):
    """
    Returns the first block of text marked by the specified characters.
    The returned block does not contain the opening and closing characters.
    The returned block contains all the sub-blocks.
    If no valid block is encountered the function returns an empty string.

    example :
    >>> get_block("test {content {sub} content}", '{', '}')
    >>> 'content {sub} content'

    :param block_close_char: The character opening a block
    :param block_open_char: The character closing a block
    :param text: The text in which to extract the block
    :return The first valid block, "" if none
    """

    depth = 0
    res = ""

    for n in range(len(text)):
        if text[n] == block_close_char:
            depth -= 1
        if depth > 0:
            res += text[n]
        if text[n] == block_open_char:
            depth += 1
        elif res != "" and depth == 0:
            break

    if depth > 0:
        return ""

    return res


def pattern_at(text, index, pattern):
    """
    Checks if the specified pattern is at the specified position in a string

    exemple :
    >>> pattern_at("test exemple", 5, "exemple")
    >>> True

    :param text The string to test.
    :param index The index at which the pattern is supposed to start in the string
    :param pattern The pattern to test
    :return A boolean answering the question
    """

    return pattern == text[index: index + len(pattern)]


#
# Parsing functions
#


def parse_reponses(r_lines):
    """
    Parses the answers of a QCM from LaTeX source code.
    The LaTeX code this function is built to parse is between the
    "\\begin{reponse} and "\\end{reponse}" tags

    :param r_lines The LaTeX code to parse
    :return A list of QCM.Reponse objects
    """

    reponses = []

    for n in range(len(r_lines)):
        if pattern_at(r_lines, n, "\\bonne"):
            reponses.append(QCM.Reponse(True, get_block(r_lines[n:], '{', '}')))
        elif pattern_at(r_lines, n, "\\mauvaise"):
            reponses.append(QCM.Reponse(False, get_block(r_lines[n:], '{', '}')))

    return reponses


def parse_qcm(q_lines):
    """
    Parses the body of a question written in LaTeX source code representing the body of ONE question
    the body must start with \\begin{question and ends with \\end{question

    :param q_lines: The LaTeX code to parse
    :return: The object QCM.Question that corresponds to the source code
    """

    lines_iter = iter(q_lines)
    q_type = None
    q_name = ""
    q_enonc = ""
    q_options = []
    q = None
    record_reponse = False
    r_lines = ""
    record_enonce = False

    for line in lines_iter:

        if line.strip().startswith("\\begin{reponses}"):
            record_enonce = False
            q = QCM.Question(q_type, q_name, q_options, q_enonc)
            record_reponse = True

        elif line.strip().startswith("\\end{reponses}"):
            record_reponse = False
            r_lines += line.strip()
            q.reponses = parse_reponses(r_lines)

        elif line.strip().startswith("\\begin{question"):
            q_decl = line.split('{')
            q_type = QCM.type_from_str(q_decl[1].strip('} \n'))
            q_name = q_decl[2].split('}')[0]
            record_enonce = True

        elif record_enonce and line.strip().startswith("\\AMC"):
            q_options.append(line.strip())

        elif record_enonce:
            q_enonc += line.strip() + "\n"

        elif record_reponse:
            r_lines += line.strip() + "\n"

    return q


#
# Main parsing function
# this is the main function that should be called to parse LaTeX
#


def parse_latex(latex):
    """
    Parses a LaTeX source code and returns a list of QCM.Questions objects representing the questions found,
    the source code can contain anything beside the questions, only the latter will pe parsed.

    :param latex: The source code to parse
    This can ba any type of text object (file, string, etc)
    as long as the default iterator iterates over the lines
    :return: The list of the questions found
    """

    qcms = []
    qcm_lines = []
    record = False

    for line in latex:

        # The starting tag of a question (needs to be on a separate line from the body)
        if line.strip().startswith("\\begin{question"):
            qcm_lines.append(line)
            record = True

        # The end tag of a question (needs to be on a separate line from the body)
        elif line.strip().startswith("\\end{question"):
            qcm_lines.append(line)
            record = False
            # Call to parse_qcm to parse the body of the question
            qcms.append(parse_qcm(qcm_lines))
            qcm_lines = []

        # The body of the question
        elif record:
            qcm_lines.append(line)

    return qcms
