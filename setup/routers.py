class DjangoDBRouter:
    def db_for_read(self, model, **hints):
        # Direciona tudo não capturado pelo GameRouter para BD_Django [[7]]
        return "django_db"

    def db_for_write(self, model, **hints):
        return "django_db"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Permite migrações apenas no BD_Django para modelos não-Shaiya [[7]]
        if db == "django_db":
            return True
        return False


# setup/routers.py
class GameRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "asgard":
            # Modelos com db_table em PS_GameData.dbo.* vão para game_data
            if model._meta.db_table.startswith("PS_GameData.dbo."):
                return "game_data"
            # Modelos com db_table em PS_UserData.dbo.* vão para user_data
            elif model._meta.db_table.startswith("PS_UserData.dbo."):
                return "user_data"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "asgard":
            if model._meta.db_table.startswith("PS_GameData.dbo."):
                return "game_data"
            elif model._meta.db_table.startswith("PS_UserData.dbo."):
                return "user_data"
        return None

    def allow_migrate(self, db, app_label, **hints):
        # Permite migrações apenas no BD_Django (default)
        if app_label == "asgard":
            # Bloqueia migrações para modelos legados (managed=False)
            return False  # Modelos do Shaiya não são gerenciados pelo Django [[4]]
        return db == "default"


class DjangoDBRouter:
    def db_for_read(self, model, **hints):
        if model.__name__ == "CustomUser":
            return "default"  # Direciona para PS_UserData
        return None

    def db_for_write(self, model, **hints):
        if model.__name__ == "CustomUser":
            return "default"  # Direciona para PS_UserData
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == "customuser":  # Nome em minúsculo
            return db == "default"
        return None

# Crie este arquivo como routers.py no diretório do seu projeto (mesmo nível do settings.py)

class DatabaseRouter:
    """
    Router para direcionar operações de modelo para os bancos de dados corretos.
    """
    
    def db_for_read(self, model, **hints):
        """
        Determina qual banco de dados usar para leitura do modelo.
        """
        # Para o modelo de usuário custom, use o banco 'user_data'
        if model._meta.model_name == 'customuser':
            return 'user_data'
        
        # Se o modelo está no app 'accounts', use o banco 'user_data'
        if model._meta.app_label == 'accounts':
            return 'user_data'
        
        # Para outros modelos relacionados a dados de jogo
        if model._meta.app_label == 'game':
            return 'game_data'
            
        # Por padrão use o banco de dados default
        return 'default'
    
    def db_for_write(self, model, **hints):
        """
        Determina qual banco de dados usar para escrita do modelo.
        """
        # Para o modelo de usuário custom, use o banco 'user_data'
        if model._meta.model_name == 'customuser':
            return 'user_data'
        
        # Se o modelo está no app 'accounts', use o banco 'user_data'
        if model._meta.app_label == 'accounts':
            return 'user_data'
        
        # Para outros modelos relacionados a dados de jogo
        if model._meta.app_label == 'game':
            return 'game_data'
            
        # Por padrão use o banco de dados default
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relações entre objetos se ambos estiverem no mesmo banco de dados.
        """
        # Permite relações se ambos os modelos usarem o mesmo banco de dados
        db1 = self.db_for_write(obj1.__class__)
        db2 = self.db_for_write(obj2.__class__)
        
        if db1 and db2 and db1 == db2:
            return True
        
        # Ou permite se um dos bancos é o 'default'
        if db1 == 'default' or db2 == 'default':
            return True
            
        return False
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determina se a migração para um modelo específico deve ser executada.
        """
        # Model CustomUser deve migrar apenas para 'user_data'
        if model_name == 'customuser':
            return db == 'user_data'
            
        # Conta de usuário deve migrar apenas para 'user_data'
        if app_label == 'accounts':
            return db == 'user_data'
            
        # Dados de jogo devem migrar apenas para 'game_data'
        if app_label == 'game':
            return db == 'game_data'
            
        # Para outros apps, use o banco de dados padrão
        return db == 'default'