# TODO 1: Impement planning_agent

def planning_agent(user_input: str, has_image: bool) -> str:

  if has_image:
      return "image_analysis"
  else:
      return "chat"