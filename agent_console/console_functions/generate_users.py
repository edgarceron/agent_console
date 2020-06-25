"""Generate users from call_center.agent table"""
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from users.models import User
from profiles.models import Profile
from agent_console.models import Agent, UserAgent

class GenerateUsers():
    """Class for user automatic creation from agents"""
    @staticmethod
    def create_profile():
        """Creates a new profile for the agents"""
        try:
            profile = Profile.objects.get(name="Agente")
        except Profile.DoesNotExist:
            profile = Profile()
            profile.name = "Agente"
            profile.active = True
            profile.save()
        return profile

    @staticmethod
    def create_user_agent(user, id_agent):
        """Creates an UserAgent model with given user and agent ids"""
        try:
            user_agent = UserAgent.objects.get(user=user.id)
        except UserAgent.DoesNotExist:
            user_agent = UserAgent()
            user_agent.user = user
            user_agent.agent = id_agent
            user_agent.save()
        return user_agent

    @staticmethod
    def create_user(number, name, profile):
        """Creates a new User model for the agent if doesn't exist already"""
        try:
            username = number + "@call.center"
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User()
            user.username = number + "@call.center"
            user.name = name
            user.lastname = "Generado automaticamente"
            user.profile = profile
            user.active = True
            user.need_password = False
            hasher = PBKDF2PasswordHasher()
            password = hasher.encode(number, "Wake Up, Girls!")
            user.password = password
            user.save()
        return user

    @staticmethod
    def bulk_create_users():
        """Create the profile, users and user_agents for every agent if doesn't exist already"""
        profile = GenerateUsers.create_profile()
        agents = Agent.objects.all()
        for agent in agents:
            number = agent.number
            name = agent.name
            user = GenerateUsers.create_user(number, name, profile)
            GenerateUsers.create_user_agent(user, agent.id)
        print("Usuarios generados con exito")
