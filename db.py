from storytypes import Story, Leaf, Tree

def create_story(chat_id, name) -> Story:
  story = Story(chat_id = chat_id, name = name)
  story.save()
  return story

def create_voice_leaf(voice_id) -> Leaf:
  leaf = Leaf(leaf_type='voice', content=str(voice_id))
  leaf.save()
  return leaf

def add_leaf(story_id: int, parent_id: int, child_id: int) -> Tree:
  pass

def get_stories(chat_id) -> [Story]:
  return Story.get()