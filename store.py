import uuid
from typing import List, Dict, Set
from schemas import Agent, AgentCreate, UsageLog

class DataStore:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.usage_logs: List[UsageLog] = []
        self.processed_request_ids: Set[str] = set()

    def add_agent(self, agent_data: AgentCreate) -> Agent:
        agent_id = str(uuid.uuid4())
        tags = self._extract_keywords(agent_data.description)
        new_agent = Agent(
            id=agent_id,
            name=agent_data.name,
            description=agent_data.description,
            endpoint=agent_data.endpoint,
            tags=tags
        )
        self.agents[agent_id] = new_agent
        return new_agent

    def get_all_agents(self) -> List[Agent]:
        return list(self.agents.values())

    def search_agents(self, query: str) -> List[Agent]:
        query = query.lower()
        results = []
        for agent in self.agents.values():
            if query in agent.name.lower() or query in agent.description.lower():
                results.append(agent)
        return results

    def log_usage(self, log: UsageLog):
        # Validation: Check if target agent exists by name
        target_exists = any(a.name == log.target for a in self.agents.values())
        if not target_exists:
            raise ValueError(f"Target agent '{log.target}' not found.")

        # Idempotency check
        if log.request_id in self.processed_request_ids:
            return  # Ignore duplicate request_id

        self.usage_logs.append(log)
        self.processed_request_ids.add(log.request_id)

    def get_usage_summary(self) -> Dict[str, int]:
        summary = {}
        for log in self.usage_logs:
            summary[log.target] = summary.get(log.target, 0) + log.units
        return summary

    def _extract_keywords(self, text: str) -> List[str]:
        # Simple keyword extraction (Option B)
        # Filters out common stop words and returns unique words >= 3 chars
        stop_words = {"and", "the", "for", "with", "from", "extracts", "structured", "data"}
        words = text.lower().replace(",", "").replace(".", "").split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return list(set(keywords))

# Global store instance
store = DataStore()
