import string

import QCM


def parse_QCM(q_lines):
    lines_iter = iter(q_lines)
    q_type = None
    q_name = ""
    q_enonc = ""
    q = None

    record_enonce = False

    for line in lines_iter:

        if line.startswith("\\element"):
            pass

        elif line.startswith("\\begin"):
            q_decl = line.split('{')
            q_type = QCM.type_from_str(q_decl[1].rstrip('} '))
            q_name = q_decl[2].rstrip('} ')

            record_enonce = True

        elif line.strip().startswith("\\bonne"):
            q.reponses.append(QCM.Reponse(True, line.split('{')[1].rstrip('} ')))

        elif line.strip().startswith("\\mauvaise"):
            q.reponses.append(QCM.Reponse(False, line.split('{')[1].rstrip('} ')))

        elif line.strip().startswith("\\begin{reponses}"):
            record_enonce = False
            q = QCM.Question(q_type, q_name, q_enonc, [])

        elif record_enonce:
            q_enonc += line.strip() + "\n"

    return q


if __name__ == "__main__":
    qtest = """\\element{gr1}{
    \\begin{questionmult}{DefConvexFunc}
      \\AMCnoCompleteMulti
      A function $f:\\RR^n\\to\\RR\\cup{+\\infty}$ (with $f(x)=+\\infty$ for $x\\notin \\dom f$) is convex if and only if:
      \\begin{reponses}
        \\bonne{$-f$ is concave.}
        \\mauvaise{$\\theta f(x) + (1-\\theta)f(y) \\leq f(\\theta x + (1-\\theta) y)$ for any $x,y$ and $\\theta\\in [0,1]$.}
        \\mauvaise{$\\theta f(x) + (1-\\theta)f(y) \\leq f(\\theta x + (1-\\theta) y)$ for any $x,y$ and $\\theta\\in \RR_+$.}
          \\bonne{$f(\\theta x + (1-\\theta) y) \\leq \\theta f(x) + (1-\\theta)f(y)$ for any $x,y$ and $\\theta\\in [0,1]$.}
      \\end{reponses}
    \\end{questionmult}
    }"""

    print(parse_QCM(qtest.splitlines()))