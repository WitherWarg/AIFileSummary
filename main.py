from sample_ai import generate_prompt

while True:
    try:
        message = input("Chat:\n\t")
    except KeyboardInterrupt:
        print()
        break

    print(generate_prompt(message))