
class EnvironmentHistory:
    def __init__(self, base_query: str, start_info, memory: list[str], history: list[dict[str, str]] | None = None) -> None:
        self._cur_query: str = f"{_get_base_query(base_query, start_info, memory)}"
        self._history: list[dict[str, str]] = history if history is not None else []
        self._last_action: str = ""
        self._is_exhausted: bool = False

    def add(self, label: str, value: str) -> None:
        if label not in {"action", "observation", "human_edit"}:
            raise ValueError(f"Invalid label: {label}. Expected one of ['action', 'observation', 'human_edit']")
        self._history += [
            {
                "label": label,
                "value": value,
            }
        ]
        if label == "action":
            if value == self._last_action:
                self._is_exhausted = True
            else:
                self._last_action = value

    def check_is_exhausted(self) -> bool:
        return self._is_exhausted

    def reset(self) -> None:
        self._history = []

    def __str__(self) -> str:
        s: str = self._cur_query + "\n"
        for _i, item in enumerate(self._history):
            if item["label"] == "action":
                s += f"{item['value']}\n"
            elif item["label"] == "observation":
                s += f"Observation: {item['value']}\n\nAction: "
            elif item["label"] == "human_edit":
                s += f'[human edit]: {item["value"]}'
            # if i != len(self._history) - 1:
            #     s += '\nend.'
        return s


def _get_base_query(base_query: str, start_info: str, memory: list[str]) -> str:
    query = base_query

    # add memory if it exists
    if len(memory) > 0:
        query += "\nYour memory for the task below:"
        for i, m in enumerate(memory):
            query += f"\nTrial {i}:\n{m.strip()}"
    query += f"\nHere is the task:\n{start_info}"
    return query
