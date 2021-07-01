from firebase_config import FirebaseConfig
import json
class Products:
   def get(self):
      _fire=FirebaseConfig()
      res = _fire.firebaseApp().get('/Shop/Product',None)
      return  json.dumps(res)