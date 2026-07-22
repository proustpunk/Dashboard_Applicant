import asyncio


class EventManager:
    def __init__(self):
        self.listeners = {}

    async def subscribe(self, candidate_id: int):
        queue = asyncio.Queue()

        if candidate_id not in self.listeners:
            self.listeners[candidate_id] = []

        self.listeners[candidate_id].append(queue)

        return queue

    async def unsubscribe(self, candidate_id: int, queue):
        if candidate_id in self.listeners:
            self.listeners[candidate_id].remove(queue)

            if len(self.listeners[candidate_id]) == 0:
                del self.listeners[candidate_id]

    async def publish(self, candidate_id: int, message: dict):
        for queue in self.listeners.get(candidate_id, []):
            await queue.put(message)


event_manager = EventManager()