Overview

This project features a front end built with Svelte and TailwindCSS, and a back end API built with Python Flask. We aimed to implement Pera Wallet identification and IPFS integration. While the Should_work branch is close to functional, it has an issue with the Pera Wallet connection. Currently, transactions are hardcoded with a mnemonic phrase (not secure).

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
