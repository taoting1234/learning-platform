from app.parsers.search import search_parser

invitation_code_list_parser = search_parser.copy()
invitation_code_list_parser.add_argument("code", type=str)
invitation_code_list_parser.add_argument("user_id", type=int)
invitation_code_list_parser.add_argument("is_used", type=bool)
