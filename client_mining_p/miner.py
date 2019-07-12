import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    proof = 0
    
    def valid_proof(last_proof, proof):
        """
        Validates the Proof:  Does hash(last_proof, proof) contain 4
        leading zeroes?
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] == "000000"
    
    while True:
        # TODO: Get the last proof from the server and look for a new one
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.

        lp_res = requests.get(url=f'{node}/last_proof')
        last_proof = lp_res.json().get("last_proof")
        print(last_proof)
        if(proof > 0):
            proof += 1

        while valid_proof(last_proof, proof) is False:
            proof += 1
        res = requests.post(url=f'{node}/mine', json={"proof": proof, "recipient": "AJ"})
        valid = res.json().get("message")
        if(not valid):
            print(f"Rejected proof: {proof}")
        else:
            coins_mined += 1
            print(f"Valid proof: {proof}, total coins: {coins_mined}")

