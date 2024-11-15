from helper_functions import *
from getpass import getpass


def main_menu():
	# Show the main menu options
	try:
		print('========== Password Manager ==========')
		print('0. Exit')
		print('1. Existing User')
		print('2. New User')
		print('3. Remove User')

		# Take input and parse the result
		option = int(input('Option: '))
		
		if option == 0:
			exit(0)
		elif option == 1:
			user = log_in()
			existing_user_menu(user)
		elif option == 2:
			new_user_menu()
		elif option == 3:
			user = log_in()
			remove_user(user)
		else:
			print('Invalid Option')

	except Exception as e:
		print('Exception: ', e)
		exit(1)


def log_in():
	csv = pd.read_csv('src/data/masterpw.csv')
	username = input('Enter Username: ')

	if username not in csv['username'].values:
		print('User Not Found')
		return
	
	masterpw = getpass('Enter your master password: ')
	if verify_password(username, masterpw):
		return username


def existing_user_menu(user):
	# Menu for existing users to log in
	try:
		print('========== {user} ==========')
		print('0. Exit')
		print('1. See your passwords')
		print('2. Add a new password')
		option = int(input())
		if option == 0:
			exit(0)
		elif option == 1:
			see_passwords(user)
		elif option == 2:
			add_password(user)
		else:
			print('Invalid Option')

	except Exception as e:
		print('Exception: ', e)
		exit(1)


def new_user_menu():
	# Check for unique username
	username = input('Give a username: ')
	csv = pd.read_csv('src/data/masterpw.csv')
	if username in csv['username'].values:
		print('User already exists')
		return
	
	# Add a master password
	masterpw = getpass('Enter a master password: ')
	salt = base64.b64encode(generate_salt()).decode('utf-8')
	encrypted_master_key = generate_key_from_masterpw(masterpw, salt)
	new_row = {'username':username, 'salt':salt, 'encrypted_master_key':encrypted_master_key}
	csv.loc[len(csv)] = new_row
	csv.to_csv('src/data/masterpw.csv', index=False)

	print('Successful Entry')


def main():
	if not os.path.exists('src/data/user_passwords.csv'):
		file = open('src/data/user_passwords.csv', 'x')
		file.write('username,site_name,encrypted_password,initialization_vector')
		file.close()
	
	if not os.path.exists('src/data/masterpw.csv'):
		file = open('src/data/masterpw.csv', 'x')
		file.write('username,salt,encrypted_master_key')
		file.close()

	while True:
		main_menu()


if __name__ == '__main__':
	main()