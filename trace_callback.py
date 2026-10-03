from langchain_core.callbacks import BaseCallbackHandler


class LLMTraceCallback(BaseCallbackHandler):

    def __init__(self):
        self.llm_call = 0

    def on_chat_model_start(
        self,
        serialized,
        messages,
        **kwargs
    ):
        self.llm_call += 1

        print("\n")
        print("=" * 100)
        print(f"                 ACTUAL LLM REQUEST #{self.llm_call}")
        print("=" * 100)

        print("\nSERIALIZED MODEL")
        print("-" * 100)
        print(serialized)

        print("\nMESSAGES SENT TO MODEL")
        print("-" * 100)

        for batch in messages:
            for message in batch:

                print("\nMESSAGE TYPE:", type(message).__name__)

                if hasattr(message, "content"):
                    print("CONTENT:")
                    print(message.content)

                if hasattr(message, "tool_calls") and message.tool_calls:
                    print("TOOL CALLS:")
                    print(message.tool_calls)

    def on_llm_end(self, response, **kwargs):

        print("\n")
        print("-" * 100)
        print(f"                 LLM RESPONSE #{self.llm_call}")
        print("-" * 100)

        print(response)