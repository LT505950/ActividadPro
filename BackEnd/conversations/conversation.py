from datetime import datetime
import uuid

class Conversation:
    MAX_USER_TURNS = 2  # 🔴 límite

    def __init__(self, agent: str):
        self.test_id = f"test-activpro-{uuid.uuid4().hex[:6]}"
        self.agent = agent
        self.created_at = datetime.utcnow().isoformat() + "Z"
        self.turns = []
        self.user_turns = 0
        self.conversation_complete = False
        self.completion_reason = None
        self.evaluation = None

    def add_user_turn(self, content: str):
        self.user_turns += 1
        self.add_turn("user", content)

    def add_turn(self, role: str, content: str, metadata=None):
        turn = {
            "turn_id": len(self.turns) + 1,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        if metadata:
            turn["metadata"] = metadata
        self.turns.append(turn)

    def reached_max_turns(self) -> bool:
        return self.user_turns >= self.MAX_USER_TURNS

    def to_dict(self):
        return {
            "test_id": self.test_id,
            "agent": self.agent,
            "created_at": self.created_at,
            "conversation_complete": self.conversation_complete,
            "completion_reason": self.completion_reason,
            "turns": self.turns,
            "evaluation": self.evaluation
        }