import QCM


def get_block(text, block_open_char, block_close_char):
    """Renvoie le premier bloc de texte délimité par les caractères spécifiés
    Le bloc renvoyé ne contient pas les caractères délimitant mais contient les sous-blocs
    Si aucun bloc valide n'est rencontré la fonction renvoie une chaîne vide.

    example :
    >>> get_block("test {content {2} content}", '{', '}')
    >>> 'content {2} content'

    :param block_close_char: le caractère marquant l'ouverture d'un bloc
    :param block_open_char: le caractère marquant la fermeture d'un bloc
    :param text: le texte dans lequel chercher
    :return le premier bloc valide trouvé si il existe, "" sinon
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
    """Vérifie si le motif est à la position dan le texte

    exemple :
    >>> pattern_at("test exemple", 5, "exemple")
    >>> True

    :param text le texte à vérifier
    :param index l'index du caractère de début du motif dans le texte
    :param pattern le motif
    :return un booléen indiquant si le motif est effectivement dans le texte à l'endroit spécifié
    """

    return pattern == text[index : index + len(pattern)]


def parse_reponses(r_lines):
    """Parse les réponses d'une QCM à partir du code LaTeX
     et renvoie une liste d'objets QCM.Reponse.
     Le code LaTeX à parser doit commencer par "\\begin{reponse}
     et finir par "\\end{reponse}"

    :param r_lines le code LaTeX à parser
    :return la liste des réponses trouvées
    """

    reponses = []

    for n in range(len(r_lines)):
        if pattern_at(r_lines, n, "\\bonne"):
            reponses.append(QCM.Reponse(True, get_block(r_lines[n:], '{', '}')))
        elif pattern_at(r_lines, n, "\\mauvaise"):
            reponses.append(QCM.Reponse(False, get_block(r_lines[n:], '{', '}')))

    return reponses


def parse_qcm(q_lines):
    """Parse une question à partir d'un code LaTeX

    :param q_lines: Le code LaTeX représentant UNE question
    doit commencer par \\begin{question et finir par \\end{question
    :return: l'instance de QCM.Question représentant la question
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

        if line.startswith("\\element"):
            pass

        elif line.strip().startswith("\\begin{reponses}"):
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


def parse_latex(latex):
    """Parse un code LaTeX fourni en argument et renvoie les QCM trouvées
    le code LaTeX peut contenir autre chose que des QCM, seules les QCM seront reconnues et
    le reste sera ignoré

    :param latex: Le code LaTeX à parser
    le code peut être un objet quelconque do moment qu'il se comporte comme du texte
    et qu'il est possible d'itérer sur les lignes.
    :return: La liste contenant les questions trouvées dans le code LaTeX
    """

    qcms = []
    qcm_lines = []
    record = False

    for line in latex:

        if line.strip().startswith("\\begin{question"):
            qcm_lines.append(line)
            record = True

        elif line.strip().startswith("\\end{question"):
            qcm_lines.append(line)
            record = False
            qcms.append(parse_qcm(qcm_lines))
            qcm_lines = []

        elif record:
            qcm_lines.append(line)

    return qcms

