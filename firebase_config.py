from firebase import firebase
class FirebaseConfig:
    firebase = firebase.FirebaseApplication("https://haruko-37c48-default-rtdb.firebaseio.com", None)
    def firebaseApp(self):
        return self.firebase


