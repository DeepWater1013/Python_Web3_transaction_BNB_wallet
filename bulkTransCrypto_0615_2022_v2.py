import string
from web3 import Web3
import time
import xml.etree.ElementTree as ET
import hone
from time import gmtime, strftime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pandas import read_csv
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition)
import mysql.connector
import csv

class BulkTransCrypto:
    def __init__(self):
        self.senderAddress = "0x0e41E533061f8ec22F3040237b257e5234975843"
        self.privateKey = '06f59167d0095fa0b586eef0244486dd1691f1d2b2999645a29f2d7cd8d00f67'
        self.gasLimit = 21000
        self.gasPrice = 10  # GWEI
        self.to_adrs = "0x138EB2CED1E7d03dff233Aa527723df7876Bee52"
        self.trans_amount = 0.005
        self.tx_list = []
        self.total_amount = 0.0
        self.bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"

        self.read_config()
        print(self.bsc)
        self.web3 = Web3(Web3.HTTPProvider(self.bsc))
        if self.web3.isConnected():
            print("Web3 connection is completed!  :)")
        else:
            print("Web3 connection is failed!     :(")
            quit()

    def read_config(self):
        myXMLtree = ET.parse('config.xml')
        self.limit_record = int(myXMLtree.find('limit_record').text.replace(' ', ''))

        x = myXMLtree.find('bsc_data')
        self.bsc = x.find('bsc').text.replace(' ', '')
        self.senderAddress = x.find(
            'senderAddress').text.replace(' ', '')
        self.privateKey = x.find('privateKey').text.replace(' ', '')
        self.gasLimit = int(x.find('gasLimit').text.replace(' ', ''))
        self.gasPrice = int(x.find('gasPrice').text.replace(' ', ''))
        
        
        
        x = myXMLtree.find('mail')
        self.emailFrom = x.find('emailFrom').text.replace(' ', '')
        self.emailTo = x.find('emailTo').text.replace(' ', '')
        self.sendGridAPIKey = x.find(
            'sendGridAPIKey').text.replace(' ', '')
        
        x = myXMLtree.find('sql_data')
        self.sql_host = x.find('host').text.replace(' ', '')
        self.sql_user = x.find('user').text.replace(' ', '')
        self.sql_pwd = x.find('password').text.replace(' ', '')
        self.sql_dbname = x.find('database').text.replace(' ', '')
        
        
    def read_payment_list(self):
        self.mydb = mysql.connector.connect(
        host=self.sql_host,
        user=self.sql_user,
        password=self.sql_pwd,
        database=self.sql_dbname
        )

        mycursor = self.mydb.cursor()
        
        _sql = f"SELECT `users`.`bnb_wallet`, `users`.`name`, `payments`.*, `payments`.`sum` / `course`.`price` AS `sum_bnb` FROM `payments` LEFT JOIN `purchases` ON (`payments`.`purchase_id` = `purchases`.`id`) LEFT JOIN `users` ON (`purchases`.`user_id` = `users`.`id`), (SELECT `price` FROM `courses` WHERE `currency` = 'BNB') AS `course` WHERE paid = 0 AND wrong_wallet = 0 LIMIT {self.limit_record}"
        mycursor.execute(_sql)
        
        
        columns = [col[0] for col in mycursor.description]
        self.tx_list = [dict(zip(columns, row)) for row in mycursor.fetchall()]
        # print(self.tx_list)
        
    def update_db(self):
        mycursor = self.mydb.cursor()
        for _item in self.tx_list:
            mycursor.execute(f"UPDATE payments SET paid = {_item['paid']} ,  wrong_wallet = {_item['wrong_wallet']}, transaction_id = '{_item['transaction_id']}' WHERE id = {_item['id']}")
            self.mydb.commit()
            
            
    def make_result_csv(self):
        # make result csv file
        with open("result.csv","w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['bnb_wallet', 'sum_bnb'])
            
            for _item in self.tx_list:
                if _item['wrong_wallet']:
                    continue
                csv_writer.writerow([_item['bnb_wallet'],_item['sum_bnb']])
            
    def send_email(self, _subject, _content, _attach):
        message = Mail(
            from_email=self.emailFrom,
            to_emails=self.emailTo,
            subject=_subject,
            html_content=_content)  # '<strong>and easy to do anywhere, even with Python</strong>'

        if _attach:
            with open('result.csv', 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()
            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName('result.csv'),
                FileType('application/csv'),
                Disposition('attachment')
            )
            message.attachment = attachedFile
        try:
            sg = SendGridAPIClient(self.sendGridAPIKey)
            sg.send(message)
        except Exception as e:
            print(e.message)
            
    def send_success_email(self):
        # Send email to admin
        _time = strftime("%d/%m/%Y", gmtime())
        text = f'<strong>Hello,<br>This is the full successful payment transaction for the day {_time}</strong>'
        self.send_email("Payment successful", text, True)
        
    def run_bulk_transaction(self):
        # make the bulk transaction.
        for _item in self.tx_list:
            if _item['wrong_wallet']:
                _item['paid'] = 0
                continue
            
            _item['transaction_id'] = self.send_crypto(self.senderAddress, _item['bnb_wallet'], float(_item['sum_bnb']))
            
            _item['paid'] = 1
        
    def check_validation_wallet(self):
        total_amount = 0.0
        for _item in self.tx_list:
            _item['bnb_wallet'] = Web3.toChecksumAddress(_item['bnb_wallet'])
            try:
                self.web3.eth.get_balance(_item['bnb_wallet'])
                _item['wrong_wallet'] = 0
            except:
                print("Found Invalid bnb_wallet: ", "---"+_item['bnb_wallet']+"----")
                _item['wrong_wallet'] = 1
                continue
            
            total_amount += float(_item['sum_bnb'])

        source_balance = self.web3.fromWei(self.web3.eth.get_balance(self.senderAddress), 'ether')
        
        self.index = 0
        print("source wallet total : ", source_balance)
        print("total transaction value : ", total_amount)
        
        if(source_balance < total_amount):
            self.send_email("Source wallet missing BNB's",
                            f'<strong>Source wallet balance is {source_balance} BNB you need to have a total of {total_amount} BNB to cover the full payment for today.</strong>', False)
            quit()
            
    def send_crypto(self, _src_addrs, _dest_addrs, _amount):
        
        print("----"*20)
        self.index +=1
        print("trans_no: ", self.index)
        print("from_address :", _src_addrs)
        print("to_address:", _dest_addrs)
        print("trans_amount:", _amount)
        # print(type(_amount))

        _nonce = self.web3.eth.getTransactionCount(_src_addrs)
        my_balance = self.web3.fromWei(self.web3.eth.get_balance(_src_addrs), 'ether')
        print("Current balance of Sender : ", my_balance, "BNB")

        my_balance = self.web3.fromWei(self.web3.eth.get_balance(_dest_addrs), 'ether')
        print("Current balance of Reciever : ", my_balance, "BNB")

        tx = {
            'nonce': _nonce,
            'to': _dest_addrs,
            'value': self.web3.toWei(_amount, 'ether'),
            'gas': self.gasLimit,
            'gasPrice': self.web3.toWei(self.gasPrice, 'gwei')
        }

        signed_tx = self.web3.eth.account.signTransaction(tx, private_key=self.privateKey)
        # print(signed_tx.rawTransaction)
        # print(signed_tx.hash)
        # print(signed_tx.r)
        # print(signed_tx.s)
        # print(signed_tx.v)
        
        try:
            result = str(self.web3.eth.sendRawTransaction(signed_tx.rawTransaction).hex())
        except ValueError as err:
            print(err)
            return "error"

        time.sleep(10)
        
        return result
        
        


    def run(self):
        self.read_payment_list()
        
        self.check_validation_wallet()
        self.run_bulk_transaction()
            
        self.update_db()
        self.make_result_csv()
        self.send_success_email()
        



my_bulkTrans = BulkTransCrypto()
my_bulkTrans.run()