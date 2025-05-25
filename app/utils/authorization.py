from app.database.models.revoked_tokens import RevokedToken
from app.utils.logger import logger
from datetime import datetime

class authorization():


    def revoked_tokens(self, jti, expire_at):
       
        # Guarda el JTI en MongoDB con un campo "expireAt" para TTL
        #revoked_tokens.insert_one({"jti": jti, "expireAt": expire_at})
        
        data = {"jti": jti, "expireAt": expire_at}

        # Revoca el token
        revoked_token = RevokedToken(jti, expire_at)
        revoked_token.save()

        return True