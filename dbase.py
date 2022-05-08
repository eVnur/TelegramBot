import aiosqlite3

class User:
	async def Reg(userID,username):#Регистрация пользователя
		userData = userID,username,1000
		conn = await aiosqlite3.connect('dbase/users.db')
		cur = await conn.cursor()
		await cur.execute(f"SELECT * FROM tg_bot WHERE user_id={userID}")
		result = await cur.fetchone()
		if not result:
			answer = f"✅ {username} вы успешно зарегистрировались!"
			await cur.execute(f"INSERT INTO tg_bot VALUES(NULL,?,?,?);",userData)
			await conn.commit()
			await cur.close()
			await conn.close()
		else:
			answer = f"❌ {username} вы уже зарегистрированы!"
			await cur.close()
			await conn.close()
		return answer

	async def Info(userID):#Вывод информации о пользователя
		conn = await aiosqlite3.connect('dbase/users.db')
		cur = await conn.cursor()
		await cur.execute(f"SELECT * FROM tg_bot WHERE user_id={userID}")
		result = await cur.fetchone()
		if not result:
			answer = f"❌ Вы не зарегистрированы"
			await cur.close()
			await conn.close()
		else:
			answer = f"{'='*20}\n👤 Имя: {result[2]}\n💰 Деньги: {result[3]:,}$\n{'='*20}".replace(',',' ')
			await cur.close()
			await conn.close()
		return answer

	async def Del(userID,name):#Удаление профиля пользователя
		conn = await aiosqlite3.connect('dbase/users.db')
		cur = await conn.cursor()
		await cur.execute(f"SELECT * FROM tg_bot WHERE user_id={userID}")
		result = await cur.fetchone()
		if not result:
			answer = f"❌ {name} у вас нет профиля в базе данных!"
			await cur.close()
			await conn.close()
		else:
			answer = f"✅ {name} вы успешно удалили свой профиль!"
			await cur.execute(f"DELETE FROM tg_bot WHERE user_id={userID}")
			await conn.commit()
			await cur.close()
			await conn.close()
		return answer

	async def SetMoney(userID,value):#Установка денег для пользователя
		conn = await aiosqlite3.connect('dbase/users.db')
		cur = await conn.cursor()
		await cur.execute(f"SELECT * FROM tg_bot WHERE user_id={userID}")
		result = await cur.fetchone()
		await cur.execute(f"UPDATE tg_bot SET money=money+? WHERE id=?",(value,result[0]))
		await conn.commit()
		await cur.close()
		await conn.close()