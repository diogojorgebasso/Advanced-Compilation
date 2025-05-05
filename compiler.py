from lark import Lark

cpt = iter(range(1000))

g = Lark(r"""
    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9]*/
    NUMBER: /[1-9][0-9]*/ | "0"
    OPBIN: /[+\-*\/>]/
    liste_var :                                                                    -> vide                            
        | IDENTIFIER ("," IDENTIFIER)*                                             -> vars
    expression: IDENTIFIER                                                         -> var
        | expression OPBIN expression                                              -> opbin
        | NUMBER                                                                   -> number
    commande : commande (";" commande)* (";")?                                     -> sequence
        | IDENTIFIER "=" expression                                                -> affectation
        | "while" "(" expression ")" "{" commande "}"                              -> while
        | "if" "(" expression ")" "{" commande "}" ("else" "{" commande "}")?      -> ifelse
        | "print" "(" expression ")"                                               -> print        
        | "skip"                                                                   -> skip                                         
    program : "main" "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}" -> program
    %import common.WS
    %ignore WS""", start="program")

op2asm = {'+' : 'add rax, rbx', '-' : 'sub rax, rbx'}

def pp_expression(e):
    if e.data in ("var", "number") : 
        return f"{e.children[0].value}"
    e_left = e.children[0]
    e_op = e.children[1]
    e_right = e.children[2]
    return f"{pp_expression(e_left)} {e_op.value} {pp_expression(e_right)}"

def pp_commande(c):
    if c.data=="affectation":
        return f"{c.children[0]} = {pp_expression(c.children[1])}"
    elif c.data == "skip": 
        return "skip"
    elif c.data == "print":
        return f"printf({pp_expression(c.children[0])})"
    elif c.data == "while":
        exp = c.children[0]
        body = c.children[1]
        return f"while ( {pp_expression(exp)} ) \n {{{pp_commande(body)}}}"
    elif c.data == "sequence":
        d = c.children[0]
        tail = c.children[1]
        return f"{pp_commande(d)}; \n{pp_commande(tail)}"
    
def pp_program(p):
    args = p.children[0]
    body = p.children[1]
    return f"main({args}) {pp_commande(body)}"

def asm_exp(e):
    if e.data == "var":
        return f"mov rax, [{e.children[0].value}]"
    if e.data == "number":
        return f"mov rax, {e.children[0].value}"
    e_left = e.children[0]
    e_op = e.children[1]
    e_right = e.children[2]
    asm_left = asm_exp(e_left)
    asm_right = asm_exp(e_right)
    return f"""
        {asm_left}
        push rax
        {asm_right}
        mov rbx, rax
        {op2asm[e_op.value]}
        """

def asm_cmd(c):
    if c.data=="affectation":
        var = c.children[0]
        exp = c.children[1]
        return f"""{asm_exp(exp)}
mov [{var.value}], rax"""
    elif c.data == "skip": 
        return "nop"
    elif c.data == "print":
        # add o fmt na seção .data
        return f"""
{asm_exp(c.children[0])}
mov rsi, rax
xor rax, rax
mov rdi, fmt
call printf""" 
    elif c.data == "while":
        exp = c.children[0]
        body = c.children[1]
        idx = next(cpt)
        return f"""
loop{idx}:
    {asm_exp(exp)}
    cmp rax, 0
    jz end{idx}
    {asm_cmd(body)}
jmp loop{idx}
    end{idx}:
        nop
        """
    elif c.data == "sequence":
        d = c.children[0]
        tail = c.children[1]
        return f"{asm_cmd(d)}; \n{asm_cmd(tail)}"

def asm_prg(p):
    with open("module.asm") as f:
        prog_asm = f.read()
    ret = asm_exp(p.children[2])
    prog_asm = prog_asm.replace("RETOUR", ret)
    init_vars = ""
    decl_vars = ""
    for idx, c in enumerate(p.children[0].children):
        init_vars += f"""
mov rbx, [argv]
mov rdi, [rbx + {8*(idx+1)}]
call atoi
mov [{c.value}], rax"""
        decl_vars += f"{c.value} : dq 0\n"
    prog_asm = prog_asm.replace("DECL_VARS", decl_vars)
    prog_asm = prog_asm.replace("INIT_VARS", init_vars)
    asm_c = asm_cmd(p.children[1])
    prog_asm = prog_asm.replace("COMMANDE", asm_c)
    return prog_asm

if __name__ == "__main__":
    with open("simple.c") as f:
        code = f.read()
    ast = g.parse(code)
    print(asm_prg(ast))
