# utils_db.py
import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreDB, cls).__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        cred = credentials.Certificate('credentials.json')
        firebase_admin.initialize_app(cred)
        cls._db = firestore.client()

    @classmethod
    def fetch_prefix(cls, bot, ctx):
        doc_ref = cls._db.collection("guilds").document(str(ctx.guild.id))
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict().get("prefix")
        return "!"

    @classmethod
    def create_guild(cls, guild_id):
        doc_ref = cls._db.collection("guilds").document(str(guild_id))
        doc_ref.set({"prefix": "!"})

    @classmethod
    def fetch_guild(cls, guild_id):
        doc_ref = cls._db.collection("guilds").document(str(guild_id))
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    @classmethod
    def ping(cls):
        print("Pong!")

    @property
    def client(self):
        return self._db


# Función para obtener la instancia de la base de datos
def get_db():
    return FirestoreDB()
