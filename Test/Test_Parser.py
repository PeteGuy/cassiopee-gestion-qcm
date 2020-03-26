import Parser

if __name__ == "__main__":
    qtest = """\\element{gr1}{
    \\begin{questionmult}{DefConvexFunc}
      \\AMCnoCompleteMulti
      A function $f:\\RR^n\\to\\RR\\cup{+\\infty}$ (with $f(x)=+\\infty$ for $x\\notin \\dom f$) is convex if and only if:
      \\begin{reponses}
        \\bonne{$-f$ is concave.}
        \\mauvaise{$\\theta f(x) + (1-\\theta)f(y) \\leq f(\\theta x + (1-\\theta) y)$ for any $x,y$ and $\\theta\\in [0,1]$.}
        \\mauvaise{$\\theta f(x) + (1-\\theta)f(y) \\leq f(\\theta x + (1-\\theta) y)$ for any $x,y$ and $\\theta\\in \\RR_+$.}
        \\bonne{$f(\\theta x + (1-\\theta) y) \\leq \\theta f(x) + (1-\\theta)f(y)$ for any $x,y$ and $\\theta\\in [0,1]$.}
      \\end{reponses}
    \\end{questionmult}
    }"""

    qtest2 = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \\element{gr1}{
    \\begin{questionmult}{DefConvexSet}%\\bareme{b=20}    
      A set $C$ is convex if and only if
      \\begin{reponses}
        \\bonne{for any $x, y\\in C$ and any $\\theta\\in[0,1]$, we have $\\theta x+(1-\\theta)y \\in C$.}
        \\mauvaise{for any $x, y\\in C$ and any $\\theta\\in\\RR$, we have $\\theta x+(1-\\theta)y \\in C$.}
        \\mauvaise{for any $x, y\\in C$ and any $\\theta\\in\\RR_+$, we have $\\theta x+(1-\\theta)y \\in C$.}
      \\end{reponses}
    \\end{questionmult}
    }
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \\element{gr1}{
    \\begin{questionmult}{ExHalfSpace}    
      \\AMCnoCompleteMulti
      The set $\\{x\\in\\RR^n\\,|\\,a\\tr x \\leq b\\}$
      \\begin{reponses}
        \\bonne{is convex.}
        \\mauvaise{is affine.}
        \\mauvaise{is non convex.}
        \\mauvaise{is an ellipsoid.}
      \\end{reponses}
    \\end{questionmult}
    }
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \\element{gr1}{
    \\begin{questionmult}{DefConvexFunc}
      \\AMCnoCompleteMulti
      A function $f:\\RR^n\\to\\RR\\cup{+\\infty}$ (with $f(x)=+\\infty$ for $x\\notin \\dom f$) is convex if and only if:
      \\begin{reponses}
        \\bonne{$-f$ is concave.}
        \\mauvaise{$\\theta f(x) + (1-\\theta)f(y) \\leq f(\\theta x + (1-\\theta) y)$ for any $x,y$ and $\\theta\\in [0,1]$.}
        \\mauvaise{$\\theta f(x) + (1-\\theta)f(y) \\leq f(\\theta x + (1-\\theta) y)$ for any $x,y$ and $\\theta\\in \\RR_+$.}
        \\bonne{$f(\\theta x + (1-\\theta) y) \\leq \\theta f(x) + (1-\\theta)f(y)$ for any $x,y$ and $\\theta\\in [0,1]$.}
      \\end{reponses}
    \\end{questionmult}
    }
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \\element{gr1}{
    \\begin{question}{IsConvexOrNot1}
      The problem
      \\begin{gather*}
        \\begin{aligned}
          \\mini & 5x_1^2+6x_2^2 \\
          \\st
          & x_1-4 \\leq 0 \\
          & 25-x_1^2-x_2^2 \\leq 0
        \\end{aligned}
      \\end{gather*}
      \\begin{reponses}
        \\bonne{is not a convex optimization problem.}
        \\mauvaise{is a convex optimization problem.}
      \\end{reponses}
    \\end{question}
    }
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \\element{gr1}{
    \\begin{question}{IsConvexOrNot1bis}
      The problem
      \\begin{gather*}
        \\begin{aligned}
          \\mini & 5x_1^2+6x_2^2 \\
          \\st
          & x_1-4 \\leq 0 \\
          & 25+x_1^2+x_2^2 \\leq 0
        \\end{aligned}
      \\end{gather*}
      \\begin{reponses}
        \\mauvaise{is not a convex optimization problem.}
        \\bonne{is a convex optimization problem.}
      \\end{reponses}
    \\end{question}
    }
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

    for qcm in Parser.parse_latex(qtest2.splitlines()):
        print(qcm)