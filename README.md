# terra-multisend

### To Install: 
1. Add a `config.json` file with two keys:

    a. `transaction_path` - should contain data to create a transaction. 
  ```
  {
    "recipients": [
        {
            "address": "terra1rn4xyx597t75hhzv6agtwp5pqssxwd2y7nfj2l",
            "amount": 1,
            "coin": "LUNA"
        },
        {
            "address": "terra1xdywt32qc328u390v9e8q76natxlypuh3vhq95",
            "amount": 1,
            "coin": "LUNA"
        },
        {
            "address": "terra13smeu7ax2fljrfwqnyyw9rsu8ftnwad9ls0fkk",
            "amount": 1,
            "coin": "LUNA"
        },
        {
            "address": "terra143zur75278h392ws3r75m53t96npvwllaptc7w",
            "amount": 1,
            "coin": "LUNA"
        }
    ],
    "senders": [
        {
            "address": "terra1fzgtvvf8a4vc82fnrxu9ly0cnsldmv80zj2a34",
            "amount": 4,
            "coin": "LUNA"
        }
    ]
}

```

    b. `mnemonic.txt` -- secret key DO NOT COMMIT THIS!!
  
  
2. Update `PATH` variable in `config.py` to point to the config.json file.
3. Run `python setup.py install`
