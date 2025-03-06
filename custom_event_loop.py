from collections import defaultdict

frames_passed = 0
scheduled_events = defaultdict(list)

def scheduled_event(func: callable, delay: int):
    scheduled_events[frames_passed+delay].append(func)
