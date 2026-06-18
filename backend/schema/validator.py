from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Optional
from datetime import datetime, date
import re

class user(BaseModel):  #for creating account

    id: Annotated[str, Field(..., title='user id', examples=["UIDXX"])]
    pwd: Annotated[str, Field(..., title='user password', min_length=8, max_length=8, description='8 characters long') ]
    name: Annotated[str, Field(..., title='user name', min_length=1, max_length=25, description='max lenght 25') ]
    mail_id: Annotated[str, Field(..., title='user mail id') ]
    balance: Annotated[float, Field(defualt = 0.0, ge = 0, le=100000, title='user account balance', description='max 1,00,000') ]
    dob: Annotated[Optional[date], Field(defualt = None, title='date of birth', description='YYYY-MM-DD') ]

    @field_validator('id')
    @classmethod
    def id_val(cls, value):
        pat = re.compile(r'\AUID\d\d\Z')  #UID\d\d
        if not pat.search(value):
            raise ValueError('User Id should be of type UIDXX (eg. UID01)')
        return value
    
    @field_validator('name')
    @classmethod
    def name_val(cls, value):
        if not value.strip():
            raise ValueError('Name cannot be empty')
        return value
    
    @field_validator('mail_id')
    @classmethod
    def email_validator(cls, value):
        pat = re.compile(r'\A\w+@\w+\.\w+\Z')  # example@gmail.com
        if not  pat.search(value):
            raise ValueError('Not a valid email ID')
        
        return value
    
    @field_validator('pwd')
    @classmethod
    def pas_val(cls, value):
        pat = re.compile(r'\A(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%&!*]).+\Z')
        if not  pat.search(value):
            raise ValueError('password should have:\n at least one captial letter,\n at least one digit,\n at least one special symbol @,#,$,%,&,!,*')
        
        return value
    
    @field_validator('dob')
    @classmethod
    def dob_must_be_in_past(cls, v: Optional[date]) -> Optional[date]:
        # Skip validation if no date was provided
        if v is None:
            return v
            
        if v >= date.today():
            raise ValueError('Date of birth must be in the past')
        return v

    @computed_field
    @property
    def age(self) -> Optional[int] :
        if self.dob is None:
            return None
        now = datetime.now().date()
        dob = self.dob
        ag = (now - dob).days // 365
        return ag
    

class id_pwd(BaseModel):  #for login purpose

    id: Annotated[str, Field(..., title='user id', examples=["UIDXX"])]
    pwd: Annotated[str, Field(..., title='user password', min_length=8, max_length=8, description='8 characters long') ]


class update_model(BaseModel): #for updating user data

    name: Annotated[Optional[str], Field(default=None, min_length=1, max_length=25, title='user name', description='max lenght 25') ]
    mail_id: Annotated[Optional[str], Field(default=None, title='user mail id')]
    balance: Annotated[Optional[float], Field(default=None, ge = 0, le=100000, title='user account balance', description='max 1,00,000') ]
    dob: Annotated[Optional[date], Field(default=None, title='date of birth', description='YYYY-MM-DD') ]

    @field_validator('name')
    @classmethod
    def name_val(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if not value.strip():  #empty string
            raise ValueError('Name cannot be empty')
        return value


    @field_validator('dob')
    @classmethod
    def dob_must_be_in_past(cls, v: Optional[date]) -> Optional[date]:
        # Skip validation if no date was provided
        if v is None:
            return v
            
        if v >= date.today():
            raise ValueError('Date of birth must be in the past')
        return v
    
    @computed_field
    @property
    def age(self) -> Optional[int] :
        if self.dob is None:
            return None
        now = datetime.now().date()
        dob = self.dob
        ag = (now - dob).days // 365
        return ag

    @field_validator('mail_id')
    @classmethod
    def email_validator(cls, value):
        if value is None:
            return None
        pat = re.compile(r'\A\w+@\w+\.\w+\Z')
        if not pat.search(value):
            raise ValueError('Not a valid email ID')
        
        return value
    