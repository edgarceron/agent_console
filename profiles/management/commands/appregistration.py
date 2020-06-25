"""
    Commmand for register App for permission check
    Each App must contain in its webservices and views file a
    get_actions function which will define each action that
    requires permission validation.
    This command requires thet profile module installed and migrated
"""
import importlib
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.conf import settings
from profiles.models import Action, App, Profile, ProfilePermissions
from profiles.serializers import ActionSerializer, AppSerializer
from users.models import User


class Command(BaseCommand):
    """Deletes unused app and actions and create new apps and actions in the db"""
    def create_apps(self):
        """Create the apps for each module installed in WEB APPS"""
        labels = settings.WEB_APPS_LABELS
        for app in settings.WEB_APPS:
            app_serializer = AppSerializer(data={"name":app, "label":labels[app]})
            if app_serializer.is_valid():
                app_serializer.save()
                self.stdout.write("Se creo la App " + app)
            else:
                self.stdout.write("Ya existe la app " + app)

    def delete_removed_apps(self, registered_apps):
        """Check if the app is still present in setting.py if not it'll be delete"""
        for app in registered_apps:
            setted = False

            for setted_app in settings.WEB_APPS:
                if app.name == setted_app:
                    setted = True

            if not setted:
                self.stdout.write("Se elimino la app " + app.name + " y todas sus acciones")
                app.delete()

    @staticmethod
    def get_actions(app_name, file_name):
        """ Gets the actions from a given file module, usually view or webservices"""
        try:
            file = importlib.import_module(app_name + "." + file_name)
            actions = file.get_actions()
        except:
            actions = []
        
        return actions
    
    def delete_removed_actions(self, registered_actions, app_id, app_name):
        """Checks the database and delete the actions that are not longer used"""
        setted_actions = Action.objects.filter(app = app_id)

        for action in setted_actions:
            setted = False

            for registered_action in registered_actions:
                if registered_action["name"] == action.name:
                    setted = True
                    break

            if not setted:
                self.stdout.write("Se elimino la acción " + action.name + " de la app " + app_name)
                action.delete()

    def create_actions(self, registered_actions, app_id, app_name):
        """Creates a column in the database for each new action given"""
        for action in registered_actions:
            data = {"name": action["name"], "label": action["label"], "app": app_id}
            action_serializer = ActionSerializer(data=data)
            if action_serializer.is_valid():
                action_serializer.save()
                self.stdout.write(
                    "Se creo la acción " + action["name"] + " para el modulo " + app_name)
            else:
                self.stdout.write(
                    "Ya existe la acción " + action["name"] + " para el modulo " + app_name)

    @staticmethod
    def create_admin_profile():
        try:
            admin_profile = Profile.objects.get(name="ADMINISTRADOR")
        except Profile.DoesNotExist:
            admin_profile = Profile()
            admin_profile.name = "ADMINISTRADOR"
            admin_profile.active = True
            admin_profile.save()

        actions = Action.objects.all()
        for action in actions:
            try:
                permission = ProfilePermissions.objects.get(
                    profile=admin_profile.id,
                    action=action.id
                )
            except ProfilePermissions.DoesNotExist:
                permission = ProfilePermissions()
                permission.profile = admin_profile
                permission.action = action

            permission.permission = True
            permission.save()
        Command.create_admin_user(admin_profile)

    @staticmethod
    def create_admin_user(profile):
        try:
            admin = User.objects.get(username="admin@agent.console")
        except User.DoesNotExist:
            admin = User()
            admin.username = "admin@agent.console"
            hasher = PBKDF2PasswordHasher()
            password = hasher.encode("admin", "Wake Up, Girls!")
            admin.password = password
            admin.active = True
            admin.profile = profile
            admin.name = "ADMINISTRADOR"
            admin.lastname = "SISTEMA"
            admin.need_password = False
            admin.save()

    def handle(self, *args, **options):
        registered_apps = App.objects.all()
        self.delete_removed_apps(registered_apps)
        self.create_apps()
        registered_apps = App.objects.all()

        for app in registered_apps:
            app_id             = app.id
            app_name           = app.name
            views              = Command.get_actions(app_name, 'views')
            webservices        = Command.get_actions(app_name, 'webservices')
            registered_actions = views + webservices

            self.delete_removed_actions(registered_actions, app_id, app_name)
            self.create_actions(registered_actions, app_id, app_name)
            self.create_admin_profile()
    