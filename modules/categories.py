from firebase_config import FirebaseConfig
import json
class Categories:
   def get(self):
      _fire=FirebaseConfig()
      res = _fire.firebaseApp().get('/Shop/Category',None)
      return  json.dumps(res)
