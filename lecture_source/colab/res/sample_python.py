class MyAgent:
    def __init__(self, model):
        self.model = model

    def run(self, query: str) -> str:
        """
        This is a long docstring for the run method.
        It explains what the method does in great detail.
        It takes a query and returns a response from the model.
        """
        print("Running the agent with the query...")
        response = self.model.predict(query)
        return f"Model response: {response}"

def helper_function(text: str):
    # This is a simple helper function.
    # It just prints the text.
    print(text)