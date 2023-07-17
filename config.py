class Config:
 DEBUG = False
 DEVELOPMENT = False
 CSRF_ENABLED = True
 ASSETS_DEBUG = False

class ProductionConfig(Config):
 pass

class DevelopmentConfig(Config): 
 DEBUG = True
 DEVELOPMENT = True
 TEMPLATES_AUTO_RELOAD = True
 ASSETS_DEBUG = True



#  FLASK_DEBUG = 0
# FLASK_APP = wsgi.py
# FLASK_ENV = production

# ORIGIN = "6 Reinhart Way, Bridgewater, NJ"
# DESTINATION = "100 Sutphen Road, Piscataway, NJ"