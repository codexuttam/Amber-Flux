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
        # Validation: find target agent by name (case-insensitive)
        target_agent = next((a for a in self.agents.values() if a.name.lower() == log.target.lower()), None)
        if not target_agent:
            raise ValueError(f"Target agent '{log.target}' not found.")

        # Idempotency check
        if log.request_id in self.processed_request_ids:
            return  # Ignore duplicate request_id

        # Normalize target name to the registered canonical name to avoid case/alias issues
        normalized_log = UsageLog(
            caller=log.caller,
            target=target_agent.name,
            units=log.units,
            request_id=log.request_id
        )

        self.usage_logs.append(normalized_log)
        self.processed_request_ids.add(log.request_id)

    def get_usage_summary(self) -> Dict[str, int]:
        summary = {}
        for log in self.usage_logs:
            summary[log.target] = summary.get(log.target, 0) + log.units
        return summary

    def _extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """
        Improved simple keyword extractor (Option B):
        - tokenizes words
        - filters punctuation and stop words
        - returns top_n most frequent words
        """
        import re
        from collections import Counter

        if not text:
            return []

        # simple tokenization
        tokens = re.findall(r"\w+", text.lower())

        stop_words = {
            "and", "the", "for", "with", "from", "extracts", "structured",
            "data", "service", "services", "that", "this", "are", "a", "an", "of", "in"
        }

        filtered = [t for t in tokens if t not in stop_words and len(t) > 2]
        counts = Counter(filtered)
        most_common = [w for w, _ in counts.most_common(top_n)]
        return most_common

# Global store instance
store = DataStore()
