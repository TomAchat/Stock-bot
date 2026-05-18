# 🤖 Bot de surveillance de stock → Telegram

Vérifie la disponibilité de produits sur n'importe quel site toutes les 10 minutes
et t'envoie une notification Telegram instantanée dès qu'un article est dispo.

---

## 📋 Fonctionnalités

- ✅ Surveillance de 10+ sites simultanément
- ✅ Notification Telegram instantanée
- ✅ Anti-spam : alerte une seule fois par remise en stock
- ✅ Hébergement 100% gratuit (Railway ou Render)
- ✅ Vérification toutes les 10 minutes

---

## 🚀 Installation en 5 étapes

### Étape 1 — Créer ton bot Telegram

1. Ouvre Telegram et cherche **@BotFather**
2. Envoie `/newbot`
3. Donne un nom à ton bot (ex: `MonBotStock`)
4. Donne un username (ex: `mon_bot_stock_bot`)
5. **Copie le token** qui ressemble à : `123456789:AABBccDDee...`

### Étape 2 — Récupérer ton Chat ID

1. Cherche **@userinfobot** sur Telegram
2. Envoie `/start`
3. **Copie ton ID** (un nombre, ex: `987654321`)

### Étape 3 — Configurer les produits

Édite `products.json` et ajoute tes produits. Trois méthodes possibles :

#### Méthode A — Sélecteur CSS (la plus précise)
```json
{
  "id": "produit-unique-id",
  "name": "Nom du produit",
  "url": "https://www.site.com/produit",
  "selector": ".availability-message",
  "unavailable_keywords": ["rupture", "indisponible"]
}
```
→ Comment trouver le sélecteur : clic droit sur la zone de dispo → "Inspecter" → copie le sélecteur CSS

#### Méthode B — Texte d'indisponibilité (le plus simple)
```json
{
  "id": "produit-unique-id",
  "name": "Nom du produit",
  "url": "https://www.site.com/produit",
  "unavailable_text": "Actuellement indisponible"
}
```
→ Colle le texte exact qui apparaît quand le produit est en rupture

#### Méthode C — Texte de disponibilité
```json
{
  "id": "produit-unique-id",
  "name": "Nom du produit",
  "url": "https://www.site.com/produit",
  "available_text": "Ajouter au panier"
}
```

### Étape 4 — Déployer sur Railway (gratuit)

1. Crée un compte sur [railway.app](https://railway.app) (gratuit)
2. Clique **New Project → Deploy from GitHub**
3. Upload ton dossier ou connecte ton repo GitHub
4. Va dans **Variables** et ajoute :
   ```
   TELEGRAM_TOKEN   = ton_token_botfather
   TELEGRAM_CHAT_ID = ton_chat_id
   ```
5. Dans **Settings → Start Command** : `python main.py`
6. **Deploy** → le bot tourne 24/7 !

### Étape 4 (alternative) — Déployer sur Render (gratuit)

1. Crée un compte sur [render.com](https://render.com)
2. **New → Web Service** (ou Background Worker)
3. Connecte ton repo GitHub
4. Paramètres :
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `python main.py`
5. Ajoute les variables d'environnement `TELEGRAM_TOKEN` et `TELEGRAM_CHAT_ID`
6. **Create Service**

### Étape 5 — Tester en local (optionnel)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Définir les variables (Linux/Mac)
export TELEGRAM_TOKEN="ton_token"
export TELEGRAM_CHAT_ID="ton_chat_id"

# Lancer le bot
python main.py
```

---

## 📁 Structure du projet

```
stock_bot/
├── main.py          # Point d'entrée + planificateur
├── scraper.py       # Vérifie la dispo sur les sites
├── notifier.py      # Envoie les alertes Telegram
├── database.py      # Stocke les états (SQLite)
├── products.json    # Liste de tes produits à surveiller
├── requirements.txt # Dépendances Python
└── README.md        # Ce fichier
```

---

## 🔧 Dépannage

**Le bot ne détecte pas la disponibilité ?**
→ Certains sites utilisent JavaScript pour charger le stock. Dans ce cas,
  utilise la méthode `unavailable_text` avec le texte visible sur la page HTML brute.

**Erreur 403 / blocage ?**
→ Le site bloque les bots. Tu peux ajouter un délai entre les requêtes
  ou utiliser un proxy gratuit (ex: ScraperAPI free tier).

**Je ne reçois pas les notifications ?**
→ Vérifie que tu as envoyé un message à ton bot d'abord (il faut initier la conversation).

---

## ⚠️ Note légale

Vérifie les CGU des sites avant de scraper. Certains sites interdisent le scraping
automatisé dans leurs conditions d'utilisation.
