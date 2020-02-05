def markdown_parser(my_text):
    """
    Converts a string into a question, a list of answer options, and a question_type.
    """
    if my_text.count(":")!=1:
        print("Cannot parse, there's an error in the format")
        return {"is_format_ok":False}
    single_option = 0
    multiple_option = 0
    if (" * " in my_text) or ("\n* " in my_text):
        single_option = 1
        split_char = "*"
    if (" v " in my_text) or ("\nv " in my_text):
        multiple_option = 1
        split_char = "v"
    # If both False or both True, simultaneoulsy, there's an error
    if single_option==multiple_option:
        print("Cannot parse, there's an error in the format")
        return {"is_format_ok":False}
    question_str, answer_str = my_text.split(":")
    question = question_str.strip()
    answer_list = [_.strip() for _ in answer_str.split(split_char)[1:]]
    question_type = single_option*"single"+multiple_option*"multiple"
    return {"is_format_ok":True, "question":question, "answers":answer_list, "type":question_type}

if __name__=="__main__":
    # Bad formatting
    print(markdown_parser("Mi Pregunta  "))
    print(markdown_parser("Mi Pregunta   :  Opcion 1      Opcion 2    "))
    print(markdown_parser("Mi Pregunta   *  Opcion 1  *    Opcion 2    "))
    # Single
    print(markdown_parser("Mi Pregunta   : * Opcion 1     * Opcion 2    "))
    print(markdown_parser("¿Cuál es tu animal favorito?   : *    Perro     *     Gato    "))
    print(markdown_parser("""¿Cuál es tu animal favorito?   :
     *    Perro     
*     Gato    """))
    # Multiple
    print(markdown_parser("Mi Pregunta   : v Opcion 1     v Opcion 2    "))
    print(markdown_parser("¿Cuál es tu animal favorito?   : v    Perro     v     Gato    "))
    print(markdown_parser("""¿Cuál es tu animal favorito?   :
     v    Perro     
v     Gato    """))
    # Mixed
    print(markdown_parser("Mi Pregunta   : v Opcion 1     * Opcion 2    "))
    print(markdown_parser("¿Cuál es tu animal favorito?   : *    Perro     v     Gato    "))
    print(markdown_parser("""¿Cuál es tu animal favorito?   :
     v    Perro     
*     Gato    """))