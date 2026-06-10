# 🤖 TikTok Bot - Advanced Automated TikTok Commenting Bot

Un bot TikTok entièrement automatisé écrit en Python avec contrôle Discord, compatible avec **Termux sur Android/Linux**.

## ✨ Fonctionnalités

### 🎯 Core Features
- ✅ **Connexion automatique** au compte TikTok (login/session)
- ✅ **Surveillance multi-hashtags** (#fyp #viral #challenge etc.)
- ✅ **Web scraping** pour trouver les vidéos récentes
- ✅ **Commentaires aléatoires** avec templates personnalisables
- ✅ **Anti-ban**: délais aléatoires (30-180s), rotation user-agent, proxies optionnels
- ✅ **Rate limiting**: max 5-10 actions/heure configurable
- ✅ **Gestion automatique** du rate limit TikTok

### 🎮 Commandes Discord
- `/start` - Démarrer le bot
- `/stop` - Arrêter le bot
- `/status` - État du bot et statistiques
- `/addhashtag #hashtag` - Ajouter un hashtag
- `/addcomment "texte"` - Ajouter un template de commentaire
- `/comment #hashtag1 #hashtag2 "comment1" "comment2"` - Configuration complète
- `/help` - Aide sur les commandes

### 🔧 Configuration
- Configuration persistante en **JSON**
- Logging complet dans **bot.log**
- Fichier `.env` sécurisé pour les credentials
- Support des proxies optionnels
- Threading/Asyncio pour fonctionnement en arrière-plan

## 📋 Installation (Termux/Linux)

### 1️⃣ Prérequis
```bash
# Sur Termux:
pkg update
pkg install python
pkg install git

# Sur Linux:
sudo apt update
sudo apt install python3 python3-pip
```

### 2️⃣ Cloner le repo
```bash
git clone https://github.com/chauferra90k-cmyk/tiktok-bot.git
cd tiktok-bot
```

### 3️⃣ Installer les dépendances
```bash
chmod +x setup.sh
bash setup.sh
```

Ou manuellement:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4️⃣ Configuration
```bash
# Copier le template .env
cp .env.example .env

# Éditer avec tes credentials
nano .env
```

**Remplir:**
```env
DISCORD_TOKEN=ton_token_discord_ici
TIKTOK_USERNAME=ton_username_tiktok
TIKTOK_PASSWORD=ton_password_tiktok
DEBUG=false
HEADLESS=true
MAX_COMMENTS_PER_HOUR=10
RATE_LIMIT_DELAY_MIN=30
RATE_LIMIT_DELAY_MAX=180
```

### 5️⃣ Lancer le bot
```bash
source venv/bin/activate
python3 discord_bot.py
```

**Ou via le launcher:**
```bash
bash run.sh
```

## 🎮 Utilisation

### Dans Discord

**1. Configuration simple:**
```
/comment #fyp #viral "Amazing! 🔥" "Love this! ❤️"
```

**2. Démarrer:**
```
/start
```

**3. Vérifier l'état:**
```
/status
```

**4. Ajouter des hashtags/commentaires individuellement:**
```
/addhashtag #challenge
/addcomment "Top content! 👍"
```

**5. Arrêter:**
```
/stop
```

## 📊 Architecture

### `tiktok_bot.py`
Moteur principal du bot:
- `ConfigManager`: Gestion de la config JSON
- `TikTokAPI`: Interface avec TikTok (scraping + commentaires)
- `TikTokBot`: Boucle principale async

### `discord_bot.py`
Interface Discord:
- Commandes pour contrôler le bot
- Affichage des statistiques
- Configuration dynamique

### `config.json`
Stockage persistant:
- Hashtags à surveiller
- Templates de commentaires
- Statistiques (total comments, this hour)
- État du bot

### `bot.log`
Logging complet des actions

## 🔐 Sécurité

### Pratiques de sécurité
- ✅ Credentials dans `.env` (jamais commités)
- ✅ `.gitignore` pour les fichiers sensibles
- ✅ Pas de hardcoding de tokens/passwords
- ✅ User-agent rotation pour éviter les blocages
- ✅ Délais aléatoires pour sembler naturel

### Anti-Detection
- 🔄 Rotation user-agent aléatoire
- ⏱️ Délais variés (30-180s) entre actions
- 🌐 Support proxies optionnels
- 📊 Rate limiting respectueux

## ⚙️ Configuration Avancée

### Rate Limiting
```env
MAX_COMMENTS_PER_HOUR=10          # Max commentaires/heure
RATE_LIMIT_DELAY_MIN=30           # Délai min entre actions (secondes)
RATE_LIMIT_DELAY_MAX=180          # Délai max (3 minutes)
```

### Debug
```env
DEBUG=true                          # Logs verbose
HEADLESS=false                      # Afficher le navigateur
```

## 📝 Logging

Tous les événements sont logués dans `bot.log`:
```
2024-01-15 10:30:45 - tiktok_bot - INFO - Posting comment on video: abc123
2024-01-15 10:31:22 - tiktok_bot - INFO - Successfully posted comment
2024-01-15 10:32:15 - discord_bot - INFO - Status command executed
```

## 🐛 Dépannage

### ❌ "DISCORD_TOKEN not found"
```bash
# Vérifier que .env existe et contient le token
cat .env
```

### ❌ "Failed to initialize TikTok API"
- Vérifier les credentials TikTok
- Essayer de te connecter manuellement à TikTok
- Vérifier la connexion internet

### ❌ "Bot is not responding"
- Vérifier les logs: `tail -f bot.log`
- Relancer le bot
- Vérifier que Discord bot a les bonnes permissions

### ⚠️ "Rate limit exceeded"
- Le bot a atteint son quota horaire
- Augmenter `MAX_COMMENTS_PER_HOUR` si besoin
- Attendre l'heure suivante

## 🚀 Utilisation en Arrière-Plan (Termux)

```bash
# Lancer en arrière-plan
nohup python3 discord_bot.py > bot.log 2>&1 &

# Voir les logs
tail -f bot.log

# Lister les processus Python
ps aux | grep python

# Arrêter le bot
pkill -f "discord_bot.py"
```

## 📦 Dépendances

- `discord.py` - Bot Discord
- `python-dotenv` - Gestion des .env
- `aiohttp` - Requêtes HTTP async
- `TikTokApi` - API TikTok (optionnel)
- `playwright` - Web automation (optionnel)

## ⚖️ Avertissements Légaux

⚠️ **IMPORTANT - Responsabilité**

- Ce bot est à usage **éducatif et personnel** uniquement
- Respecte les **Conditions d'Utilisation de TikTok**
- TikTok peut bannir les comptes qui utilisent des bots
- L'utilisation peut violer les **conditions d'utilisation**
- Utilise responsablement et à tes risques
- L'auteur ne assume aucune responsabilité pour les bannissements

## 🔄 Mise à Jour

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📞 Support

Pour les problèmes:
1. Vérifier les logs: `tail -f bot.log`
2. Consulter la documentation: `README.md`
3. Créer une issue sur GitHub

## 📜 Licence

MIT License - Voir `LICENSE` pour plus de détails

---

**Fait avec ❤️ pour la communauté TikTok**
