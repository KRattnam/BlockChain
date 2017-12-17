
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

tokens = {}
tokens['app_id'] = 'app_id'
tokens['app_key'] = 'app_key' //key from ipdb 
bdb = BigchainDB('https://test.ipdb.io', headers=tokens)
bicycle = { 'data': {'bicycle': {'serial_number': 'abcd1234','manufacturer': 'bkfab',},},}
metadata = {'planet': 'earth'}
alice, bob = generate_keypair(), generate_keypair()
prepared_creation_tx = bdb.transactions.prepare(operation='CREATE',signers=alice.public_key,asset=bicycle,)
print ("Created Transaction : ", prepared_creation_tx)
fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=alice.private_key)
print ("Fulfiled Transaction : ", fulfilled_creation_tx)
sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)
txid = fulfilled_creation_tx['id']
if (sent_creation_tx == fulfilled_creation_tx):
	print ("Transaction Succesful, Transaction ID : ", txid)

else : 
	print ("Transaction Failed")


print ("Would You Like to transfer this to BOB?")
choice = input("Y/N?")
if (choice=='Y'):
	creation_tx = fulfilled_creation_tx
	asset_id = creation_tx['id']
	transfer_asset = {
 	   'id': asset_id
		}
	output_index = 0
	output = fulfilled_creation_tx['outputs'][output_index]

	transfer_input = {
    		'fulfillment': output['condition']['details'],
    		'fulfills': {
        		'output_index': output_index,
        		'transaction_id': fulfilled_creation_tx['id']
   			 },
    		'owners_before': output['public_keys']
			}

	prepared_transfer_tx = bdb.transactions.prepare(
   		 operation='TRANSFER',
    		asset=transfer_asset,
    		inputs=transfer_input,
   	 	recipients=bob.public_key,
		)

	fulfilled_transfer_tx = bdb.transactions.fulfill(
    		prepared_transfer_tx,
    		private_keys=alice.private_key,
		)

	sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)

print("Is Bob the owner?",
    sent_transfer_tx['outputs'][0]['public_keys'][0] == bob.public_key)

print("Was Alice the previous owner?",
    fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == alice.public_key)
