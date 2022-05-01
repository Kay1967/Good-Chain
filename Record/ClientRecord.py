from Helper.EncryptionHelper import EncryptionHelper
from Domain.Address import Address
from Domain.Client import Client

class ClientRecord:
    def __init__(self, encryptedClientTuple):
        clientTuple = EncryptionHelper.GetDecryptedTuple(encryptedClientTuple)

        self.fullname = clientTuple[0]
        self.streetname = clientTuple[1]
        self.housenumber = clientTuple[2]
        self.zipcode = clientTuple[3]
        self.city = clientTuple[4]
        self.emailaddress = clientTuple[5]
        self.mobilephone = clientTuple[6]

    def ToClientDomain(self):
        address = Address()
        address.streetname = self.streetname
        address.housenumber = self.housenumber
        address.zipcode = self.zipcode
        address.city = self.city
        return Client(self.fullname, self.emailaddress, self.mobilephone, address)     
    