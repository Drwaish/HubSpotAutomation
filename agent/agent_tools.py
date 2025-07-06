import os
import json
from langchain.agents import  tool

from agent.hubspot_ops import HubSpotOperations
from agent.google_email import GmailClient

class AgentTools:
    def __init__(self):
        self.hubops = HubSpotOperations()
        self.gmail_client = GmailClient()
        
    @tool
    def update_contacts(email: str, updated_email: str = None, updated_first_name : str = None, updated_last_name : str = None ) -> str:
        """
        User wants to update the contact in CRM.

        Parameters
        ----------
        email
            User's email  for fetching old entry.
        updated_email
          User want to update emails
        updated_first_name 
            User wants to update the first name
        updated_last_name 
            User wants to update the last name

        Return 
        ------
        str

        """
        try:
            if updated_email:
                properties = {"email": updated_email}
            elif first_name:
                properties["firstname"]= updated_first_name
            elif last_name:
                properties["lastname"]= updated_last_name

            contact_updated = self.hubops.update_contact_by_email(email = email, properties = properties)
            if contact_updated:
                return "Contact is updated successfully"
            return "Contact not updated successfully due to some reasons"
        except Exception as e:
            return f"Exception when updating contact: {e}"


    @tool
    def create_contact(email: str, first_name : str = None, last_name : str = None) -> str:
        
        """
        User wants to update the contact in CRM.

        Parameters
        ----------
        email
            User's email  for fetching old entry.
       
        first_name  (optional)
            User's first name

        last_name (optional)
            User's last name

        Return 
        ------
        str

        """        
        try:
            properties = {"email": email}
            if first_name:
                properties["firstname"]= first_name
            elif last_name:
                properties["lastname"]= last_name

            contact_added = self.hubops.add_contact(properties = properties)
            
            if contact_added:
                return "Contact is added"
        
            return "Contact not added due to some reasons. " 
        except ApiException as e:
            return f"Exception when creating contact: {e}"

    @tool
    def create_deal(self, dealname: str, amount : str = None, dealstage : str = None ):
        """
        Create a deal in CRM
        
        Parameters
        ----------
        dealname(str)
            Deal name aganst data is store in CRM.
        amount (str) [Optional]
            Amount of deal like 3000, 2000 , 4000
        dealstage (str)[Optional]
            Deal stage now like appointmentscheduled

        Return
        ------
        str
        """
        try:
        properties = {}
            if amount:
                properties['amount'] = amount
            
            elif dealstage:
                properties['dealstage'] =dealstage
            
            deal_created = self.hubops.create_deal_by_name(deal_name = dealname,properties = properties)
            if deal_created:
                return "Deal has been created"
            return "Deal can't created due to some reasons"

        except Exception as e:
            return f"Exception when creating deal: {e}"
    
     @tool
    
    def create_deal(self, dealname: str, updated_amount : str = None, updated_dealstage : str = None ):
        """
        Create a deal in CRM
        
        Parameters
        ----------
        dealname(str)
            Deal name aganst data is store in CRM.
        updated_amount (str) [Optional]
            Amount of deal like 3000, 2000 , 4000
        updated_dealstage (str)[Optional]
            Deal stage now like appointmentscheduled

        Return
        ------
        str
        """
        try:
        properties = {}
            if amount:
                properties['amount'] = updated_amount
            
            elif dealstage:
                properties['dealstage'] =updated_dealstage
            
            deal_updated = self.hubops.create_deal_by_name(deal_name = dealname,properties = properties)
            if deal_updated:
                return "Deal has been updated"
            return "Deal can't updated due to some reasons"

        except Exception as e:
            return f"Exception when updating deal: {e}"

            
    @tool
    def send_email(self, recepients : str, subject : str, email_body: str):
        """
        Send the confirmation to recepients about actions.

        Parameters
        ----------
        recepients
            Whm emails needs to send.

        subject
            Email subject for recepient.

        email_body
            Text of the body
        """
        try:
            resp = gmail_client.send_email(to = recepients,subject=subject, message_text = email_body )
            if not resp:
                return "Error in sending email"
            return "Email sending successfully"
        except Exception as e
            logger.info(f"Facing error in sending email {str(e)}")

