import QCM


# This module implements a simple LaTeX parser to create QCM.Question objects from a LaTeX source code
# The functions in this module expect the LaTeX code to use the AMC package and the french keywords


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
    # We simply need to keep track of our depth and return as soon as we go back to 0
    # block_open_char raises the depth level and block_close_char decreases it
    for n in range(len(text)):
        # We leave a block -> we are one level higher
        if text[n] == block_close_char:
            depth -= 1

        # We are still in the main block, we need to record the content
        if depth > 0:
            res += text[n]

        # We encounter a new block, we are one level deeper
        if text[n] == block_open_char:
            depth += 1

        # We are back at depth == 0 with the content of the first block, we can exit now
        elif res != "" and depth == 0:
            break

    # If depth is still > 0 at this point, the main block was invalid and as such we return ""
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
    # Answers are written in this format "\bonne{enonce}" or "\mauvaise{enonce}
    # Because an answer can span one or mutiple lines we do not iterate over the lines
    # Instead we scan each character to see if we encounter a "\bonne"  or a "\mauvaise" tag
    # We then take the immediatly following block {...} as the answer enonce
    for n in range(len(r_lines)):
        if pattern_at(r_lines, n, "\\bonne"):
            reponses.append(QCM.Reponse(True, get_block(r_lines[n:], '{', '}')))
        elif pattern_at(r_lines, n, "\\mauvaise"):
            reponses.append(QCM.Reponse(False, get_block(r_lines[n:], '{', '}')))
    return reponses


def parse_qcm(q_lines, nb_questions):
    """
    Parses the body of a question written in LaTeX source code representing the body of ONE question
    the body must start with \\begin{question and ends with \\end{question

    :param q_lines: The LaTeX code to parse
    :return: The object QCM.Question that corresponds to the source code
    """

    # This iterator iterates on each line
    lines_iter = iter(q_lines)
    q_type = None
    q_name = ""
    q_enonc = ""
    q_options = []
    q = None
    # Boolean to know when we need are in the answer block
    record_reponse = False
    # Variable to store the answer block lines before parsing them separately
    r_lines = ""
    # Boolean to know when we are in the enonce block
    record_enonce = False

    for line in lines_iter:
        # Theses lines mark the beginning of the anwer block and the end of the enonce
        if line.strip().startswith("\\begin{reponses}"):
            record_enonce = False
            q = QCM.Question(q_type, "", q_name, q_options, q_enonc)
            if q_numberColumn != 1:
                q.numberColumn = q_numberColumn
            #print(type(q+"foizehfoizjfozes\n"))
            record_reponse = True

        # These lines mark the end of the answer block
        elif line.strip().startswith("\\end{reponses}"):
            record_reponse = False
            r_lines += line.strip()
            # We have all the answer lines -> we can parse them
            q.reponses = parse_reponses(r_lines)

        # This line is the beginning of the question and where we register the name and type
        elif line.strip().startswith("\\begin{question"):
            # We split the line into "\begin", "questionType}", "questionName}" ...
            q_decl = line.split('{')
            q_type = QCM.type_from_str(q_decl[1].strip('} \n'))
            # We use split and not strip to remove any trailing option we don't care about (such as bareme)
            q_name = q_decl[2].split('}')[0]
            
            q_numberColumn = 1
            
            # We test if the question already has a name, and give it a generic nam if that's not the case
            # The name may be the same as a question from the db.json, or from the .tex file that's parsed 
            if q_name.strip() == "" :
                q_name = "QUESTION" + str(nb_questions)

            # From now on, we start saving line as part of the enonce of the question
            record_enonce = True

            # The enonce might start on the first line 
            if len(q_decl[2].split('}')) == 2:
                q_enonc += q_decl[2].split('}')[1].strip() + " \n"

        # Any line starting woth \AMC is an amc option and needs to be stored separately
        elif record_enonce and line.strip().startswith("\\AMC"):
            q_options.append(line.strip())
            
        #A line starting with \\begin{multicols} has to be taken into account
        elif record_enonce and line.strip().startswith("\\begin{multicols}"):
            q_decl = line.split('{')
            q_numberColumn = q_decl[2].split('}')[0];
           
        

        # The lines between the \begin{question} tag and the \begin{reponses} tag are the enonce of the question
        elif record_enonce:
            q_enonc += line.strip() + " \n"

        # The lines between the \begin{reponses} and \end{repones} tag are stored and parsed separately
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
    nb_questions = 0

    for line in latex:

        # The starting tag of a question (needs to be on a separate line from the body)

        # # We manually add a name if the question doesn't have one
        # if line.strip().startswith("\\begin\{question\}\{\}") :
        #     line = line.strip()[0:17] + "TEST" + line.strip()[17:]
        #     qcm_lines.append(line)
        #     record = True

        # elif line.strip().startswith("\\begin\{questionmult\}\{\}"):
        #     line = line.strip()[0:21] + "TESTMULT" + line.strip()[21:]
        #     qcm_lines.append(line)
        #     record = True

        if line.strip().startswith("\\begin{question"):
            nb_questions += 1
            qcm_lines.append(line)
            record = True

        # The end tag of a question (needs to be on a separate line from the body)
        elif line.strip().startswith("\\end{question"):
            qcm_lines.append(line)
            record = False
            # Call to parse_qcm to parse the body of the question
            qcms.append(parse_qcm(qcm_lines, nb_questions))
            qcm_lines = []
            

        # The body of the question
        elif record:
            qcm_lines.append(line)

    return qcms
