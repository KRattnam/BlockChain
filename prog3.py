
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair


tokens = {}
tokens['app_id'] = '635afc22'
tokens['app_key'] = '37536ed9d01e58529382dd0c111ab5ba' #key from ipdb 
bdb = BigchainDB('https://test.ipdb.io', headers=tokens)

print("Welcome to blockChain")
input1=("Enter Cars Model no. :")
input2=("Enter Cars name :")

cars = { 'data': {'car': {'model_number': input1,'name': input2,},},}

choice1=input("Do you own this car alone?(Y|N)")

if(choice1=='Y' or choice1=='y' ):
	name=input("Enter your name: ")
	yourkey = generate_keypair()
	print("Key generated")
	prepared_creation_tx = bdb.transactions.prepare(operation='CREATE',signers=yourkey.public_key,asset=cars,)
	print('')
	print ("Created Transaction : ", prepared_creation_tx)
	fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=yourkey.private_key)
	print ("")
	print ("Fulfiled Transaction : ", fulfilled_creation_tx)
	print ("")
	sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)
	print("asset created and uploaded to blockchain")
	choice2=input("would you like to loan or sell the asset?(L?S)")

	#LOAN Asset
	if (choice2=='L' or choice2=='l'):
		car_token = {
	     'data': {
	         'token_for': {'car': {'model_number': input1,'name': input2,},},
		        },
		        'description': 'Time share token. Each token equals one hour of riding.',
		     },
		print('Token Generated')
		choice3=int(input("How many hours do you want to loan the car for?"))
		friend=input("Enter Loaners name : ")
		friendkey2=generate_keypair()
		#prepare for loan
		prepared_token_tx = bdb.transactions.prepare(
		    operation='CREATE',
		    signers=yourkey.public_key,
		    recipients=[([friendkey2.public_key], 10)],
 		    asset=bicycle_token,
		 )
		fulfilled_token_tx = bdb.transactions.fulfill(
		     prepared_token_tx, private_keys=yourkey.private_key)
		print("Signed Transaction with private key")
		sent_token_tx = bdb.transactions.send(fulfilled_token_tx)


	#sell asset
	elif (choice2=='S' or choice2=='s'):
		buyer=input("Enter your Customers name")
		buyerkey = generate_keypair()
		output_index = 0
		output = signed_car_creation_tx['outputs'][output_index]
		output = fulfilled_creation_tx['outputs'][output_index]

		transfer_input = {
		    'fulfillment': output['condition']['details'],
		    'fulfills': {
		        'output_index': output_index,
		        'transaction_id': fulfilled_creation_tx['id']
		    },
		    'owners_before': output['public_keys']
		}
		print("Preparing for Transaction")
		print("")
		prepared_transfer_tx = bdb.transactions.prepare(
		    operation='TRANSFER',
		    asset=transfer_asset,
		    inputs=transfer_input,
		    recipients=buyerkey.public_key,
		)

		fulfilled_transfer_tx = bdb.transactions.fulfill(
		    prepared_transfer_tx,
		    private_keys=yourkey.private_key,
		)
		print("")
		print("Transaction Completed uploading to Bigchaindb")
		sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)
	else : 
		print ("Wrong choice")



#Multiple Owner
else:
	name=input("Enter your name: ")
	name1=input("Enter your fiends name: ")
	yourkey = generate_keypair()
	friendkey = generate_keypair()
	print("Two keys Generated")
	print("Signing asset with both public key")
	print("You are the main signer")
	car_creation_tx = bdb.transactions.prepare(
		     operation='CREATE',
		     signers=yourkey.public_key,
		     recipients=(yourkey.public_key, friendkey.public_key),
		     asset=cars,
		 )
	signed_car_creation_tx = bdb.transactions.fulfill(
		     car_creation_tx,
		     private_keys=yourkey.private_key,
		 )
	sent_creation_tx = bdb.transactions.send(signed_car_creation_tx)
	print("asset created and uploaded to blockchain")
	choice2=input("would you like to loan or sell the asset?(L?S)")
	#multiple owner Loan 
	if (choice2=='L' or choice2=='l'):
		pass
	#multiple owner sell
	elif (choice2=='S' or choice2=='s'):
		buyer=input("Enter your Customers name")
		buyerkey = generate_keypair()
		output_index = 0
		output = signed_car_creation_tx['outputs'][output_index]
		input_ = {
		     'fulfillment': output['condition']['details'],
		     'fulfills': {
		         'output_index': output_index,
		         'transaction_id': signed_car_creation_tx['id'],
		     },
		     'owners_before': output['public_keys'],
		 }
		transfer_asset = {
		     'id': signed_car_creation_tx['id'],
		}
		print("Preparing Transaction")
		car_transfer_tx = bdb.transactions.prepare(
	    operation='TRANSFER',
	    asset=transfer_asset,
	    inputs=input_,
		)	
		print("Fullfilling Transaction using your and your friends key.")
		print("Sending it to bdchaindb")
		sent_car_transfer_tx = bdb.transactions.send(signed_car_transfer_tx)
	else:
		print("Invalid Choice")






 
		