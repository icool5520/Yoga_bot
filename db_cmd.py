import sqlite3


def create_tables():
	db_file = "db.db"
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS users(
						user_id INTEGER PRIMARY KEY NOT NULL,
						state TEXT NOT NULL,
						data TEXT NOT NULL)""")
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS admins(
						user_id INTEGER PRIMARY KEY NOT NULL,
						state TEXT NOT NULL,
						data TEXT)""")
	with conn:
		cur.execute(f"""CREATE TABLE IF NOT EXISTS videos(
						id INTEGER PRIMARY KEY NOT NULL,
						file_name TEXT NOT NULL,
						file_id TEXT,
						thumb_url TEXT)""")




def check_user_id(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if not data:
			cur.close()
			add_user(_user_id)
		else:
			cur.close()
	except Exception as ex:
		print("check_user_id", ex)
	finally:
		if conn is not None:
			conn.close()

def check_user_is_admin(_user_id):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM admins WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if data is not None:
			cur.close()
			check = True
		else:
			cur.close()
	except Exception as ex:
		print("check_user_is_admin", ex)
	finally:
		if conn is not None:
			conn.close()
		return check


def add_user(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""INSERT INTO users(user_id, state, data) VALUES(?, ?, ?);"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		mass = {'paid':'False'}
		cur.execute(sql, (_user_id,'', str(mass)))
		conn.commit()
		cur.close()
	except Exception as ex:
		print('add_user:', ex)
	finally:
		if conn is not None:
			conn.close()


def up_user_state(_user_id, _state):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE users SET state="{_state}" WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_user_state:', ex)
	finally:
		if conn is not None:
			conn.close()


def get_user_state(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT state FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_user_state:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data[0]


def get_data(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT data FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_data:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data[0]


def up_data(_user_id, _data):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE users SET data="{_data}" WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_data:', ex)
	finally:
		if conn is not None:
			conn.close()


def get_courses():
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM videos"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		lst_courses = []
		#lst_categor = list(set(lst_categor))
		#lst_courses.sort()
		cur.close()
	except Exception as ex:
		print('get_courses:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_videofile_id(_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT file_id FROM videos WHERE id={_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_videofile_id:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data[0]


def get_lessons_files_names():
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT file_name FROM videos"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
	except Exception as ex:
		print('get_lessons_files_names:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data
'''
def check_user_is_admin(_user_id):
	db_file = "db.db"
	conn = None
	check = False
	try:
		sql = f"""SELECT * FROM admins WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		if data is not None:
			cur.close()
			check = True
		else:
			cur.close()
	except Exception as ex:
		print("check_user_is_admin", ex)
	finally:
		if conn is not None:
			conn.close()
		return check


def get_categors():
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT categors FROM products"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		lst_categor = []
		for i in data:
			lst_categor.append(i[0])
		lst_categor = list(set(lst_categor))
		lst_categor.sort()
		cur.close()
	except Exception as ex:
		print('get_categors:', ex)
	finally:
		if conn is not None:
			conn.close()
		return lst_categor


def get_cart_not_confirmed(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM cart WHERE user_id = {_user_id} AND status='not_confirmed'"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_cart_not_confirmed:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_cart_confirmed():
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM cart WHERE status='confirmed'"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
	except Exception as ex:
		print('get_cart_confirmed:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_cart_by_id(_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM cart WHERE id={_id} AND status='confirmed'"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_cart_by_id:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def set_cart(_user_id, _lst_id_product, _amount):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""INSERT INTO cart(user_id,list_buy,amount,status) VALUES(?,?,?,?)"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql, (_user_id, _lst_id_product, _amount, 'not_confirmed'))
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_cart:', ex)
	finally:
		if conn is not None:
			conn.close()

def up_cart(_user_id, _lst_id_product, _amount):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE cart SET list_buy="{_lst_id_product}",
								   amount={_amount} 
								   WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_cart:', ex)
	finally:
		if conn is not None:
			conn.close()

def up_cart_order_status_by_uid(_user_id, _ststus):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE cart SET status="{_ststus}" WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_cart_order_status_by_uid:', ex)
	finally:
		if conn is not None:
			conn.close()


def up_cart_order_status_by_id(_id_order, _ststus):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE cart SET status="{_ststus}" WHERE id={_id_order}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_cart_order_status_by_id:', ex)
	finally:
		if conn is not None:
			conn.close()


def delete_order_cart(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""DELETE FROM cart WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('delete_order_cart:', ex)
	finally:
		if conn is not None:
			conn.close()



def get_products(_categor):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM products WHERE categors='{_categor}'"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		lst_product = []
		for i in data:
			lst_product.append(i)
		lst_product = list(set(lst_product))
		lst_product.sort()
		cur.close()
	except Exception as ex:
		print('get_products:', ex)
	finally:
		if conn is not None:
			conn.close()
		return lst_product


def get_info_product(_id_product):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM products WHERE id={_id_product}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_info_product:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def get_info_product_cart(_id_product):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT * FROM products WHERE id IN {_id_product};"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
	except Exception as ex:
		print('get_info_product_cart:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data


def up_data(_user_id, _data):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""UPDATE users SET data="{_data}" WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur.close()
	except Exception as ex:
		print('up_data:', ex)
	finally:
		if conn is not None:
			conn.close()


def get_data(_user_id):
	db_file = "db.db"
	conn = None
	try:
		sql = f"""SELECT data FROM users WHERE user_id={_user_id}"""
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchone()
		cur.close()
	except Exception as ex:
		print('get_data:', ex)
	finally:
		if conn is not None:
			conn.close()
		return data[0]







'''
create_tables()
