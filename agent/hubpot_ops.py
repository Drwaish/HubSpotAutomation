'''HubSpot API Operations implemeted here '''
import os
from typing import Dict
import logging
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate,SimplePublicObjectInput

from hubspot.crm.contacts import ApiException, PublicObjectSearchRequest
from hubspot.crm.deals import SimplePublicObjectInput, SimplePublicObjectInputForCreate, PublicObjectSearchRequest
from hubspot.crm.contacts.exceptions import ApiException


load_dotenv()
logging.basicConfig(level="INFO")
logger  = logging.getLogger()

class HubSpotOperations:
    def __init__(self):
        logger.info(f"API KEY {os.getenv("HubSpotAPI")}")
        self.api_client = HubSpot(access_token=os.getenv("HubSpotAPI"))

    def add_contact(self, properties : Dict[str:str])->bool:
        """
        Add new contact to CRM 

        Parameters
        ----------
        properties
            Dictionary of credentials with "email", "firstname", "lastname"
         
        Return
        ------
        str
        
        Example:
        properties = {
                "email": "email@example.com",
                "firstname": "Zain", //optional
                "lastname": "Khan" //Optional
                }    

        """

        try:
            # properties = {"email": email}
            # if first_name:
            #     properties["firstname"]= first_name
            # elif last_name:
            #     properties["lastname"]= last_name
    

            simple_public_object_input_for_create = SimplePublicObjectInputForCreate(
                properties=properties
            )
            api_response = self.api_client.crm.contacts.basic_api.create(
                
                simple_public_object_input_for_create=simple_public_object_input_for_create
            )
            return True

        except ApiException as e:
            logger.info(f"Exception when creating contact:{e}")
            return False
            
    def update_contact_by_email(self,email:str, properties: Dict[str,str])->bool:
        """
        Update a HubSpot contact's properties based on the given email.
        Paramers
        ---------
        email (str)
            The email of the contact to update.
        properties (dict)
            The properties to update.

        Returns
        ------
            The API response or error message.
        
        Example:
        properties = {
                "email": "email@example.com",
                "firstname": "Zain", //optional
                "lastname": "Khan" //Optional
                }    
        
        """
        try:
            # Search for contact by email
            search_request = PublicObjectSearchRequest(
                filter_groups=[{
                    "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
                }],
                properties=["email"]
            )
            search_response = self.api_client.crm.contacts.search_api.do_search(public_object_search_request=search_request)
            results = search_response.results
            if not results:
                return f"No contact found with email: {email}"
            contact_id = results[0].id
            # Update contact
            logger.info(f"Contact ID : {contact_id}")
            simple_public_object_input = SimplePublicObjectInput(properties=properties)
            api_response = self.api_client.crm.contacts.basic_api.update(
                contact_id=contact_id,
                simple_public_object_input=simple_public_object_input
            )
            return True
        except ApiException as e:
            logger.info(f"Exception when updating contact: {e}")
            return False
        
    def create_deal_by_name(self,deal_name:str, properties : Dict[str,str])->bool:
        """
        create a new deal by dealname .
        Parameters
        ----------
        deal_name (str)
            The name of the deal to search for or create.
        properties (dict)
            The properties to update or set for the deal.
        
        Returns
        -------
            The API response or error message.

        Example
        properties = {
        "amount": "3000",
        "dealstage": "appointmentscheduled",
        }
        """
        try:
            properties_with_name = properties.copy()
            properties_with_name["dealname"] = deal_name
            simple_public_object_input_for_create = SimplePublicObjectInputForCreate(properties=properties_with_name)
            api_response = self.api_client.crm.deals.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input_for_create
            )
            return True
        except Exception as e:
            logger.info(f"Exception when creating deal: {e}")
            return False

    def update_deal_by_name(self,deal_name, properties)->bool:
        """
        Search for a deal by dealname and update it.

        Parameters:
        ----------
        deal_name (str)
            The name of the deal to search for or create.
        properties (dict)
             The properties to update or set for the deal.
        
        Returns
        -------
            The API response or error message.

        Example
        properties = {
           "amount": "3000",
           "dealstage": "appointmentscheduled",
         }
        """
        try:
            # Search for deal by dealname
            search_request = PublicObjectSearchRequest(
                filter_groups=[{
                    "filters": [{"propertyName": "dealname", "operator": "EQ", "value": deal_name}]
                }],
                properties=["dealname"]
            )
            search_response = self.api_client.crm.deals.search_api.do_search(public_object_search_request=search_request)
            results = search_response.results
            if results:
                deal_id = results[0].id
                simple_public_object_input = SimplePublicObjectInput(properties=properties)
                api_response = self.api_client.crm.deals.basic_api.update(
                    deal_id=deal_id,
                    simple_public_object_input=simple_public_object_input
                )
                return True
            
        except Exception as e:
            return f"Exception when updating deal: {e}" 
            return False

if __name__=="__main__":
    hubspot_operations = HubSpotOperations()
    # properties = {
    # "email": "email@example.com",
    # "firstname": "Zain",
    # "lastname": "Khan"
    # }    
    # print(update_contact_by_email(email = "email@example.com", properties = properties))
    deal_properties = {
    "amount": "3000",
    "dealstage": "appointmentscheduled",
    }
    print(hubspot_operations.update_deal_by_name("Test Deal", deal_properties))

