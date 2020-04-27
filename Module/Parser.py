import QCM


def parse_qcm(q_lines):
    lines_iter = iter(q_lines)
    q_type = None
    q_name = ""
    q_enonc = ""
    q = None

    record_enonce = False

    for line in lines_iter:

        if line.startswith("\\element"):
            pass

        elif line.strip().startswith("\\begin{reponses}"):
            record_enonce = False
            q = QCM.Question(q_type, q_name, q_enonc)

        elif line.strip().startswith("\\begin{question"):
            q_decl = line.split('{')
            q_type = QCM.type_from_str(q_decl[1].strip('} \n'))
            q_name = q_decl[2].split('}')[0]

            record_enonce = True

        elif line.strip().startswith("\\bonne"):
            q.reponses.append(QCM.Reponse(True, line.split('{')[1].strip('} \n')))

        elif line.strip().startswith("\\mauvaise"):
            q.reponses.append(QCM.Reponse(False, line.split('{')[1].strip('} \n')))

        elif record_enonce:
            q_enonc += line.strip() + "\n"

    return q


def parse_latex(latex):
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
