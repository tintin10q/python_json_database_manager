

```python

User wants to get a passport. 
    Do we know the user?
    if yes:
        Check if the user send a proof(passport, key or whatever)
        If no proof was send:
            send_Pls_send_proof()
            STOP
        if proof type is not supported:
            send_back_proof_is_not_supported()
            STOP
        valid = Validate_the_proof_against_the_given_name(proof, name)
        if not valid:
            Send_back_a_fuck_off()
            STOP
        if valid:
            is_this_user_verified?
                If not:
                    Send back a pls_verify_message()
                    Send a token the user has to return to you
                    STOP
                If verified:
                    passport = Create_passport(time, StandartClaims):
                        Log the request of a passport
                        Check if time is valid:
                        #If the time is not valid:
                        #    send_back_invalid_time()
                        #    STOP
                        Log that a passport was send back with time()
                        return Password(StandartClaims, time)
                    send_back_passport(passport)
                    STOP
    if not:
        Do we already know the required acount setup information?
           If not:
                def Create user():
                ask_for_information():  # Like name etc                 
                
                Is the information valid?
                    if not:
                        send_back_invalid_information_pls_try_again()
                        STOP
                    if yes:
                        Is there a proof for a role in the information?i
                            if no:
                                give user basic role
                                send_out_invalid_role
                            if yes:
                                Is the proof valid?
                                    if no:
                                        give the basic role
                                        && or ||
                                        send_out_invalid_role_proof() STOP
                                    if yes:
                                        give_the_user_the_role_he_wanted()
                      
                log_user_created()
                create_user_in_a_perminent_storage() 
                passport = create_passport()
                send_back passport
                send_back user_created!
           



A user wants to get verified.
    ``` The user recieved a message with a token
    if the user returns the token they can get verified
    ```
        if token is valid()
            if yes:
                validate_user_in_perminent_storage()
                send back your validated now
            if no:
                send back sorry token is not valid fuck off 
       
                    
                    
           
How to autenticate someones with a passport:

    1. Decrypt the passport
    2. Get the claims from the password
    3. Decrypt the claims               
    4. Validate the claim
    is claim valid?
      if yes:
        Perform request action
        stop()
      if no:
        send_back_non_valid_claims_fuck_off()
        Stop
        



`````
