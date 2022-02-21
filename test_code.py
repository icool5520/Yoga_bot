# import db_cmd
# import ast
#
# data = db_cmd.get_data(186919165)
# print(data)
# new_data = dict(ast.literal_eval(data))
# print(new_data)
# new_data['paid'] = "True"
# print(new_data)
# db_cmd.up_data(186919165, str(new_data))