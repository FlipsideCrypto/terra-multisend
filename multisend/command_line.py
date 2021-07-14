import json
import click

from terra_sdk.client.lcd import LCDClient
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank.msgs import MultiSendIO, MsgMultiSend

from .decorators import pass_config

@click.group()
def cli():
    pass
    
class TerraClient():

    LUNA_CONVERSION = 10**6

    def __init__(self, chain_id='testnet', mnemonic=None):
        if chain_id == 'testnet':
            self.terra = LCDClient("https://tequila-lcd.terra.dev", "tequila-0004")
        else:
            self.terra = LCDClient("https://lcd.terra.dev", "columbus-4")

        self.key = MnemonicKey(mnemonic=mnemonic) if mnemonic else None
        self.wallet = self.terra.wallet(self.key) if mnemonic else None

    def initialize_wallet(self, mnemonic):
        self.key = MnemonicKey(mnemonic=mnemonic)
        self.wallet = self.terra.wallet(self.key)


    @staticmethod
    def validate_data(inputs, outputs):
        """ Ensure amounts requested to send are the same 
        as the expected received amounts.
        """
        coin = inputs[0]['coin']
        input_amount = 0
        output_amount = 0
        
        for input in inputs:
            if input['coin'] != coin:
                raise Exception("Mismatch token types")
            input_amount += input['amount']

        for output in outputs:
            if output['coin'] != coin:
                raise Exception("Mismatch token types")
            output_amount += output['amount']

        if input_amount != output_amount:
            raise Exception(f"Mismatched token amounts input amount: {input_amount} || output amount: {output_amount}")

        return True


    def construct_message(self, inputs, outputs):
        """
            inputs (dict) -> {address, amount, coin}
            outputs (dict) --> {address, amount, coin}
        """
        TerraClient.validate_data(inputs, outputs)
        
        inputs = [
            MultiSendIO(
                address=payload['address'],
                coins=f"{payload['amount']*self.LUNA_CONVERSION}uluna",
            )
            for payload in inputs
        ]

        outputs = [
            MultiSendIO(
                address=output['address'],
                coins=f"{output['amount']*self.LUNA_CONVERSION}uluna",
            )
            for output in outputs
        ]

        return MsgMultiSend(inputs=inputs, outputs=outputs)


    def construct_transaction(self, inputs, outputs, memo="Flipside Bounties"):
        msg = self.construct_message(inputs, outputs)
        tx = self.wallet.create_and_sign_tx(
            msgs=[msg],
            fee=StdFee("200000", "120000uluna"),
            memo=memo)
        return tx


    def estimate_fee(self, inputs, outputs):
        tx = self.construct_transaction(inputs, outputs)
        return self.terra.tx.estimate_fee(tx, gas_adjustment="1.8", fee_denoms=["uluna"])


    def broadcast_transaction(self, tx):
        return self.terra.tx.broadcast(tx)

    @classmethod
    def parse_tx_json(self, path):
        with open(path, 'r') as f:
            data = json.loads(f.read())
            if ['senders, recipients'] == data.keys():
                raise Exception('Required keys not found.')
            return data

    @classmethod
    def parse_mnemonic(self, path):
        with open(path, 'r') as f:
            mnemonic = f.readline()
            return mnemonic

    @staticmethod
    def parse_config(config):
        t = TerraClient
        return t.parse_tx_json(config['transaction_path']), t.parse_mnemonic(config['mnemonic_path'])

@click.command()
@pass_config
def validate(config):
    t = TerraClient
    print(config)
    data = t.parse_tx_json(config['transaction_path'])
    print("Validated!" if t.validate_data(data['senders'], data['recipients']) else "Somethings wrong")


@click.command()
@click.option('--memo', help='[Optional] Memo for transactions', required=False)
@pass_config
def mock_transaction(config, memo=None):
    cls = TerraClient
    data, mnemonic = cls.parse_config(config)
    terra = cls(mnemonic=mnemonic)
    tx = terra.construct_transaction(data['senders'], data['recipients'])
    print(tx.to_json())


@click.command()
@click.option('--memo', help='[Optional] Memo for transactions', required=False)
@pass_config
def broadcast_transaction(config, memo=None):
    cls = TerraClient
    data, mnemonic = cls.parse_config(config)
    terra = cls(mnemonic=mnemonic)
    tx = terra.construct_transaction(data['senders'], data['recipients'])
    resp = terra.broadcast_transaction(tx)
    print(resp.to_json())


cli.add_command(validate)
cli.add_command(mock_transaction)
cli.add_command(broadcast_transaction)

def main():
    cli()