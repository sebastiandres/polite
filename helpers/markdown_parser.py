def markdown_parser(my_text):
    """
    Creates a dict, by parsing the string my_text. 
    The dict has only keys (is_format_ok, markownd_str) if the 
    string my_text has format errors. 
    If the format is ok, it also has the question_str, 
    options_str from 1 to 5 (drops any additional option), 
    and the question_type (radio for single answer, checkbox for multiple answer).
    """
    if my_text.count(":")!=1:
        print("Cannot parse, there's an error in the format")
        return {"is_format_ok":False, "markdown_str":my_text}
    single_option = 0
    multiple_option = 0
    if ("* " in my_text) or ("\n* " in my_text):
        single_option = 1
        split_char = "*"
    if ("^ " in my_text) or ("\nv " in my_text):
        multiple_option = 1
        split_char = "^"
    # If both False or both True, simultaneoulsy, there's an error
    if single_option==multiple_option:
        print("Cannot parse, there's an error in the format")
        return {"is_format_ok":False, "markdown_str":my_text}
    question_str, answer_str = my_text.split(":")
    question = question_str.strip()
    answer_list = [_.strip() for _ in answer_str.split(split_char)[1:6]] # Skip the empty string, reach to the fifth existing one
    answer_list = answer_list + ["" for _ in range(5-len(answer_list))] # Fill with empty ones if needed
    question_type = single_option*"radio"+multiple_option*"checkbox" # This is the html convention
    # Create the dict
    md_dict = {}
    md_dict["is_format_ok"] = True
    md_dict["markdown_str"] = my_text
    md_dict["type_str"] = question_type
    md_dict["question_str"] = question
    md_dict["option_1_str"] = answer_list[0]
    md_dict["option_2_str"] = answer_list[1]
    md_dict["option_3_str"] = answer_list[2]
    md_dict["option_4_str"] = answer_list[3]
    md_dict["option_5_str"] = answer_list[4]
    return md_dict
    

if __name__=="__main__":
    # Bad formatting
    print(markdown_parser("Mi Pregunta  "))
    print(markdown_parser("Mi Pregunta   :  Opcion 1      Opcion 2    "))
    print(markdown_parser("Mi Pregunta   *  Opcion 1  *    Opcion 2    "))
    # Single
    print(markdown_parser("Mi Pregunta   : * Opcion 1     * Opcion 2    "))
    print(markdown_parser("¿Cuál es tu animal favorito?   : *    Perro     *     Gato    "))
    print(markdown_parser("Q: * A * B * C * D * E "))
    print(markdown_parser("Q: * A * B * C * D * E * F * G "))
    print(markdown_parser("""¿Cuál es tu animal favorito?   :
     *    Perro     
*     Gato    """))
    # Multiple
    print(markdown_parser("Mi Pregunta   : v Opcion 1     v Opcion 2    "))
    print(markdown_parser("¿Cuál es tu animal favorito?   : v    Perro     v     Gato    "))
    print(markdown_parser("Q: v A v B v C v D v E "))
    print(markdown_parser("Q: v A v B v C v D v E v F v G "))
    print(markdown_parser("""¿Cuál es tu animal favorito?   :
     v    Perro     
v     Gato    """))
    # Mixed
    print(markdown_parser("Mi Pregunta   : v Opcion 1     * Opcion 2    "))
    print(markdown_parser("¿Cuál es tu animal favorito?   : *    Perro     v     Gato    "))
    print(markdown_parser("""¿Cuál es tu animal favorito?   :
     v    Perro     
*     Gato    """))
    # Query example
    query_fmt = """
    INSERT INTO Surveys ( markdown_str, type_str, question_str, option_1_str, option_2_str, option_3_str, option_4_str, option_5_str ) 
    VALUES ('{markdown_str}', '{type_str}', '{question_str}', '{option_1_str}', '{option_2_str}', '{option_3_str}', '{option_4_str}', '{option_5_str}');
    """
    query = query_fmt.format(**markdown_parser("Q: * A * B * C * D * E * F * G "))
    print(query)
    query = query_fmt.format(**markdown_parser("Q: v A v B v C v D v E v F v G "))
    print(query)
