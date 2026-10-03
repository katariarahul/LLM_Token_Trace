import json

def print_message(message, indent=""):
    """Print a LangChain message in a readable form."""
    msg_type = type(message).__name__

    print(f"{indent}{msg_type}")

    if getattr(message, "name", None):
        print(f"{indent}Name: {message.name}")

    if getattr(message, "content", None):
        print(f"{indent}Content:")
        print(message.content)

    if getattr(message, "tool_calls", None):
        print(f"{indent}Tool calls:")
        for tc in message.tool_calls:
            print(f"{indent}  Tool: {tc['name']}")
            print(
                f"{indent}  Args: "
                f"{json.dumps(tc['args'], indent=2, default=str)}"
            )


def print_agent_trace(result):
    messages = result["messages"]

    llm_call = 0
    total_input = 0
    total_output = 0
    total_tokens = 0

    print("\n" + "=" * 100)
    print("                         AGENT EXECUTION TRACE")
    print("=" * 100)

    for message in messages:

        # ---------------------------------------------------------
        # USER MESSAGE
        # ---------------------------------------------------------
        if type(message).__name__ == "HumanMessage":

            print("\n" + "=" * 100)
            print("USER REQUEST")
            print("=" * 100)
            print(message.content)

        # ---------------------------------------------------------
        # LLM MESSAGE
        # ---------------------------------------------------------
        elif type(message).__name__ == "AIMessage":

            usage = getattr(message, "usage_metadata", {}) or {}

            # Only count actual LLM responses that have usage data
            if usage:

                llm_call += 1

                input_tokens = usage.get("input_tokens", 0)
                output_tokens = usage.get("output_tokens", 0)
                call_total = usage.get("total_tokens", 0)

                total_input += input_tokens
                total_output += output_tokens
                total_tokens += call_total

                print("\n" + "#" * 100)
                print(f"                         LLM CALL #{llm_call}")
                print("#" * 100)

                print("\nTOKEN ACCOUNTING")
                print("-" * 100)
                print(f"INPUT TOKENS : {input_tokens}")
                print(f"OUTPUT TOKENS: {output_tokens}")
                print(f"TOTAL TOKENS : {call_total}")

                # -------------------------------------------------
                # LLM OUTPUT
                # -------------------------------------------------
                print("\nLLM OUTPUT")
                print("-" * 100)

                if message.content:
                    print(message.content)
                else:
                    print("<no text output>")

                # -------------------------------------------------
                # TOOL CALLS
                # -------------------------------------------------
                if message.tool_calls:

                    print("\nLLM REQUESTED TOOL CALLS")
                    print("-" * 100)

                    for i, tc in enumerate(message.tool_calls, 1):

                        print(f"\nTool Call #{i}")
                        print(f"Tool: {tc['name']}")

                        print("Input:")
                        print(
                            json.dumps(
                                tc["args"],
                                indent=2,
                                default=str
                            )
                        )

                else:
                    print("\nNO TOOL CALLS")

        # ---------------------------------------------------------
        # TOOL RESULT
        # ---------------------------------------------------------
        elif type(message).__name__ == "ToolMessage":

            print("\n" + "~" * 100)
            print("                         TOOL EXECUTION")
            print("~" * 100)

            print(f"Tool: {message.name}")

            if getattr(message, "tool_call_id", None):
                print(f"Call ID: {message.tool_call_id}")

            print("\nTOOL OUTPUT")
            print("-" * 100)
            print(message.content)

            print("\nTOOL OUTPUT SIZE")
            print("-" * 100)
            print(f"Characters: {len(str(message.content))}")

    # -------------------------------------------------------------
    # FINAL SUMMARY
    # -------------------------------------------------------------

    print("\n" + "=" * 100)
    print("                         TOKEN SUMMARY")
    print("=" * 100)

    print(f"LLM CALLS          : {llm_call}")
    print(f"TOTAL INPUT TOKENS : {total_input}")
    print(f"TOTAL OUTPUT TOKENS: {total_output}")
    print(f"TOTAL LLM TOKENS   : {total_tokens}")

    print("\n" + "=" * 100)