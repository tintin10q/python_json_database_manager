

        
        # This happens somewhere else register usecase
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


def
