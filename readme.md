Overview

This project includes a front end built with Svelte and TailwindCSS, and a back-end API built with Python Flask. We aimed to implement Pera Wallet identification and IPFS integration.

The goal was to have a front end that allows taking a contract that we mint as an NFT on the blockchain. Just before minting it, our objective in the back end was to encrypt it. The user would have a decryption key. 
The contract would thus be encrypted on the blockchain, and on the platform, they could access their decrypted files via “my NFT's.”

This aims to have a contract that cannot be modified and is recorded on the Algorand blockchain.

We have completed the front end and back end without encryption; however, the connection between the back end and front end is hardcoded. Nevertheless, you can view the respective codes and what we have initiated.

We have learned a lot about the blockchain ecosystem and Algorand.

Getting Started

Front End

1.	Navigate to the front folder.
2.	Install dependencies and start the development server:

  	    bun i
        bun dev --host
  
4.	Access the front end via the network address in your browser.

Back End

1.	Navigate to the back end folder.
2.	Start the Flask API:

  	    python3 app.py

Note: The back end is not connected to the front end at this time.
