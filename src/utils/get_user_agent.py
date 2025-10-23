import requests
import random

url = "https://gist.githubusercontent.com/OlguD/ba89737bc8933aabdd76172e4f185d8a/raw/b7ba4572073f55f296a734f7d1e8f31648891689/UserAgentList.json"
def get_random_user_agent():
    gist = requests.get(url).json()
    user_agents = gist["user_agents"]
    random_user_agent_number = random.randint(0, len(user_agents))
    
    return user_agents[random_user_agent_number]