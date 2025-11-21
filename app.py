import sqlite3
import datetime

class GestionStock:
    def __init__(self, db_name="stock.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.creer_tables()

    def creer_tables(self):
        # Table des produits
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prix REAL NOT NULL,
                quantite INTEGER NOT NULL
            )
        ''')
        # Table des ventes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produit_id INTEGER,
                quantite INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(produit_id) REFERENCES produits(id)
            )
        ''')
        self.conn.commit()

    def ajouter_produit(self, nom, prix, quantite):
        try:
            self.cursor.execute("INSERT INTO produits (nom, prix, quantite) VALUES (?, ?, ?)", (nom, prix, quantite))
            self.conn.commit()
            print(f"✅ Produit '{nom}' ajouté avec succès.")
        except Exception as e:
            print(f"❌ Erreur: {e}")

    def afficher_stock(self):
        print("\n--- 📦 ÉTAT DU STOCK ---")
        self.cursor.execute("SELECT * FROM produits")
        produits = self.cursor.fetchall()
        print(f"{'ID':<5} {'Nom':<20} {'Prix':<10} {'Quantité':<10}")
        print("-" * 50)
        for p in produits:
            print(f"{p[0]:<5} {p[1]:<20} {p[2]:<10} {p[3]:<10}")
        print("-" * 50)

    def vendre_produit(self, produit_id, quantite_vendu):
        # Vérifier le stock actuel
        self.cursor.execute("SELECT quantite, nom FROM produits WHERE id = ?", (produit_id,))
        resultat = self.cursor.fetchone()
        
        if resultat:
            stock_actuel, nom = resultat
            if stock_actuel >= quantite_vendu:
                # Mettre à jour le stock
                nouveau_stock = stock_actuel - quantite_vendu
                self.cursor.execute("UPDATE produits SET quantite = ? WHERE id = ?", (nouveau_stock, produit_id))
                # Enregistrer la vente
                self.cursor.execute("INSERT INTO ventes (produit_id, quantite) VALUES (?, ?)", (produit_id, quantite_vendu))
                self.conn.commit()
                print(f"💰 Vente confirmée : {quantite_vendu} x {nom}")
            else:
                print(f"⚠️ Stock insuffisant ! Seulement {stock_actuel} disponibles.")
        else:
            print("❌ Produit introuvable.")

# --- Interface Utilisateur (Console) ---
app = GestionStock()

while True:
    print("\n1. Ajouter Produit | 2. Voir Stock | 3. Enregistrer Vente | 4. Quitter")
    choix = input("Choix : ")

    if choix == "1":
        nom = input("Nom du produit : ")
        prix = float(input("Prix : "))
        qty = int(input("Quantité initiale : "))
        app.ajouter_produit(nom, prix, qty)
    elif choix == "2":
        app.afficher_stock()
    elif choix == "3":
        pid = int(input("ID du produit à vendre : "))
        qty = int(input("Quantité vendue : "))
        app.vendre_produit(pid, qty)
    elif choix == "4":
        print("Au revoir !")
        break
