import sys, re, datetime
import random, pyodbc


#Random password generator

class Password:
 limit_min=9
 limit_max=16
 chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
 number = '0123456789'
 special_chars = '|!$&/()=?^[]+,;.:-_'
 def __init__(self, username, password):
	self.username = username
	self.old_password = password
	self.new_password = password
 def genPassword(self):
 	tail = ''
 	pwds = self.chars + self.number + self.special_chars
 	if(self.new_password == self.old_password):
 		for x in range(random.randint(self.limit_min, self.limit_max)):
 			tail += random.choice(pwds)
 		print("New password saved: " + tail)
 		self.new_password = tail
 	elif ( (str( raw_input("Password allready set.. do you want to reset it? (N default)") )).upper() == 'Y' ):
 		self.new_password = self.old_password
 		self.genPassword()


#Case use:
#	randomize user's password on different database and other services if python's API supports.
#	why? because much but less IT company dosn't use Active Directory services
# 	instead they save and share between them a file with clear credentials
#	
#	so in this strange scenario perhaps a "best" practices could be to change every months password credential 
#	and so we can invalidate an old version of that file with clear credetials.


class Strategy:
 driver = 'None'
 query = 'None'
 def setArgs(self):
	pass

class Postgres_strategy(Strategy):
 driver ='DRIVER={PostgreSQL Unicode}'
 def setArgs(self):
 	self.query = "ALTER USER "+self.args[0]+" WITH PASSWORD '"+self.args[1]+"';"

class Mysql_strategy(Strategy):
 driver = 'DRIVER={MySQL ODBC 3.51 Driver}'
 def setArgs(self):
	self.query = "SET PASSWORD FOR '"+self.args[0]+"'@'"+self.args[1]+"' = PASSWORD('"+self.args[2]+"'); FLUSH PRIVILEGES;"

class SQL_ODBC(Password):
 def __init__(self, username, password, server, database, port):
 	Password.__init__(self, username, password)
	self.server = "SERVER="+server
	self.database =  "DATABASE="+database
 	self.port = "PORT="+port
 def setStrategy(self, sqltype):
 	self.sqltype = sqltype
 def test(self):
  try:
  	cdn = pyodbc.connect(self.toString)
  	cdn.close()
  	return True
  except _ :
  	print("Some issue connecting to db")
  	return False	
 def changePassword(self):
  if(self.test()):
 	cdn = pyodbc.connect(self.toString())
 	ptr = cnd.cursor()
 	self.genPassword()
 	self.sqltype.args = []
 	self.sqltype.args += [self.username]
	self.sqltype.args += [self.database]
 	self.sqltype.args += [self.new_password]
 	try:
 		ptr.execute(self.sqltype.query)
 		cdn.close()
 		return True
 	except _ :
 		print("Some issue setting new password")
 		cdn.close()
 		return False
 def toString(self):
 	return driver+"; "+self.server+"; "+self.port+"; "+self.database+"; UID="+self.username+"; PASSWORD="+self.new_password+";"


class Factory():
	options = {
		"POSTGRES" : lambda : self.retz.setStrategy( Postgres_strategy() ),
		"POSTGRESQL" : lambda : self.retz.setStrategy( Postgres_strategy() ),
		"MYSQL" : lambda : self.retz.setStrategy( Mysql_strategy(Strategy) )
	}
	def getClass(self, args):
		retz = SQL_ODBC(args[1], args[2], args[3], args[4], args[5])
		self.options[ args[0].upper() ]
		return retz


def main(args):
	db_list = open( args[0], "r") 	#"file.txt"
	db_output = open( "db_output.txt", "w")
	factory_state = Factory()
	for entry_i in db_list:			#"postgres server.net port_i database_name username password"
		strz = entry_i.split("\t")
		if len(strz) > 4 :
			retz = factory_state.getClass(strz)
			if( retz.changePassword() ):
				strz[5] = retz.new_password
		db_output.write( " ".join(strz))
	db_list.close()
	db_output.close()

if __name__ == "__main__":
	main(sys.argv[1:])
